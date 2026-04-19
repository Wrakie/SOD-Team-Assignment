from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Optional

from mining_ois.db.database import get_connection

PRIORITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
WORK_ORDER_STATUSES = {"OPEN", "IN_PROGRESS", "COMPLETED", "CANCELLED"}
INCIDENT_STATUSES = {"OPEN", "INVESTIGATING", "CLOSED"}
SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
MOVEMENT_TYPES = {"IN", "OUT"}


def _require_exists(conn, table: str, entity_id: int) -> None:
    row = conn.execute(f"SELECT id FROM {table} WHERE id = ?", (entity_id,)).fetchone()
    if row is None:
        raise ValueError(f"{table[:-1].capitalize()} with id {entity_id} not found")


def create_production_log(payload: dict[str, Any], db_path: Optional[str] = None) -> int:
    with get_connection(db_path) as conn:
        _require_exists(conn, "sites", payload["site_id"])
        cur = conn.execute(
            """
            INSERT INTO production_logs (site_id, shift_date, tonnes_processed, downtime_minutes, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                payload["site_id"],
                str(payload["shift_date"]),
                payload["tonnes_processed"],
                payload["downtime_minutes"],
                payload.get("notes"),
            ),
        )
        return int(cur.lastrowid)


def list_production_logs(db_path: Optional[str] = None) -> list[dict[str, Any]]:
    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT p.id, p.shift_date, p.tonnes_processed, p.downtime_minutes, p.notes,
                   s.id AS site_id, s.name AS site_name
            FROM production_logs p
            JOIN sites s ON s.id = p.site_id
            ORDER BY p.shift_date DESC, p.id DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]


def list_sites(db_path: Optional[str] = None) -> list[dict[str, Any]]:
    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT id, name, location, status
            FROM sites
            ORDER BY name
            """
        ).fetchall()
        return [dict(r) for r in rows]


def list_equipment(db_path: Optional[str] = None) -> list[dict[str, Any]]:
    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT e.id, e.code, e.type, e.status, e.hours_runtime, e.site_id, s.name AS site_name
            FROM equipment e
            JOIN sites s ON s.id = e.site_id
            ORDER BY e.code
            """
        ).fetchall()
        return [dict(r) for r in rows]


def create_work_order(payload: dict[str, Any], db_path: Optional[str] = None) -> int:
    priority = payload["priority"].upper()
    if priority not in PRIORITIES:
        raise ValueError("Invalid priority")

    with get_connection(db_path) as conn:
        _require_exists(conn, "equipment", payload["equipment_id"])
        now = datetime.now(UTC).isoformat()
        cur = conn.execute(
            """
            INSERT INTO work_orders (equipment_id, title, priority, status, created_at, due_date)
            VALUES (?, ?, ?, 'OPEN', ?, ?)
            """,
            (
                payload["equipment_id"],
                payload["title"],
                priority,
                now,
                str(payload["due_date"]) if payload.get("due_date") else None,
            ),
        )
        return int(cur.lastrowid)


def update_work_order_status(work_order_id: int, status: str, db_path: Optional[str] = None) -> None:
    normalized = status.upper()
    if normalized not in WORK_ORDER_STATUSES:
        raise ValueError("Invalid work order status")

    with get_connection(db_path) as conn:
        _require_exists(conn, "work_orders", work_order_id)
        completed_at = datetime.now(UTC).isoformat() if normalized == "COMPLETED" else None
        conn.execute(
            "UPDATE work_orders SET status = ?, completed_at = ? WHERE id = ?",
            (normalized, completed_at, work_order_id),
        )


def list_open_work_orders(db_path: Optional[str] = None) -> list[dict[str, Any]]:
    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT w.id, w.title, w.priority, w.status, w.created_at, w.due_date,
                   e.code AS equipment_code, e.type AS equipment_type
            FROM work_orders w
            JOIN equipment e ON e.id = w.equipment_id
            WHERE w.status IN ('OPEN', 'IN_PROGRESS')
            ORDER BY
                CASE w.priority
                    WHEN 'CRITICAL' THEN 1
                    WHEN 'HIGH' THEN 2
                    WHEN 'MEDIUM' THEN 3
                    ELSE 4
                END,
                w.created_at
            """
        ).fetchall()
        return [dict(r) for r in rows]


def create_incident(payload: dict[str, Any], db_path: Optional[str] = None) -> int:
    severity = payload["severity"].upper()
    if severity not in SEVERITIES:
        raise ValueError("Invalid incident severity")

    with get_connection(db_path) as conn:
        _require_exists(conn, "sites", payload["site_id"])
        cur = conn.execute(
            """
            INSERT INTO incidents (site_id, severity, description, reported_at, status, lost_time_injuries)
            VALUES (?, ?, ?, ?, 'OPEN', ?)
            """,
            (
                payload["site_id"],
                severity,
                payload["description"],
                datetime.now(UTC).isoformat(),
                1 if payload.get("lost_time_injuries") else 0,
            ),
        )
        return int(cur.lastrowid)


def update_incident_status(incident_id: int, status: str, db_path: Optional[str] = None) -> None:
    normalized = status.upper()
    if normalized not in INCIDENT_STATUSES:
        raise ValueError("Invalid incident status")

    with get_connection(db_path) as conn:
        _require_exists(conn, "incidents", incident_id)
        conn.execute("UPDATE incidents SET status = ? WHERE id = ?", (normalized, incident_id))


def list_open_incidents(db_path: Optional[str] = None) -> list[dict[str, Any]]:
    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT i.id, i.severity, i.description, i.reported_at, i.status, i.lost_time_injuries,
                   s.name AS site_name
            FROM incidents i
            JOIN sites s ON s.id = i.site_id
            WHERE i.status IN ('OPEN', 'INVESTIGATING')
            ORDER BY
                CASE i.severity
                    WHEN 'CRITICAL' THEN 1
                    WHEN 'HIGH' THEN 2
                    WHEN 'MEDIUM' THEN 3
                    ELSE 4
                END,
                i.reported_at DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]


def create_inventory_item(payload: dict[str, Any], db_path: Optional[str] = None) -> int:
    with get_connection(db_path) as conn:
        _require_exists(conn, "sites", payload["site_id"])
        cur = conn.execute(
            """
            INSERT INTO inventory_items (sku, name, unit, current_stock, reorder_level, site_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                payload["sku"],
                payload["name"],
                payload["unit"],
                payload["current_stock"],
                payload["reorder_level"],
                payload["site_id"],
            ),
        )
        return int(cur.lastrowid)


def list_inventory_items(db_path: Optional[str] = None) -> list[dict[str, Any]]:
    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT i.id, i.sku, i.name, i.unit, i.current_stock, i.reorder_level, i.site_id,
                   s.name AS site_name
            FROM inventory_items i
            JOIN sites s ON s.id = i.site_id
            ORDER BY i.sku
            """
        ).fetchall()
        return [dict(r) for r in rows]


def record_stock_movement(payload: dict[str, Any], db_path: Optional[str] = None) -> int:
    movement_type = payload["movement_type"].upper()
    if movement_type not in MOVEMENT_TYPES:
        raise ValueError("Invalid movement type")

    with get_connection(db_path) as conn:
        _require_exists(conn, "inventory_items", payload["item_id"])

        row = conn.execute(
            "SELECT current_stock FROM inventory_items WHERE id = ?", (payload["item_id"],)
        ).fetchone()
        current = float(row["current_stock"])

        if movement_type == "IN":
            new_stock = current + float(payload["quantity"])
        else:
            new_stock = current - float(payload["quantity"])
            if new_stock < 0:
                raise ValueError("Insufficient stock for OUT movement")

        conn.execute(
            "UPDATE inventory_items SET current_stock = ? WHERE id = ?",
            (new_stock, payload["item_id"]),
        )

        cur = conn.execute(
            """
            INSERT INTO stock_movements (item_id, movement_type, quantity, reference, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                payload["item_id"],
                movement_type,
                payload["quantity"],
                payload.get("reference"),
                datetime.now(UTC).isoformat(),
            ),
        )
        return int(cur.lastrowid)


def list_low_stock(db_path: Optional[str] = None) -> list[dict[str, Any]]:
    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT i.id, i.sku, i.name, i.unit, i.current_stock, i.reorder_level, s.name AS site_name
            FROM inventory_items i
            JOIN sites s ON s.id = i.site_id
            WHERE i.current_stock <= i.reorder_level
            ORDER BY (i.current_stock - i.reorder_level) ASC
            """
        ).fetchall()
        return [dict(r) for r in rows]


def get_operational_summary(db_path: Optional[str] = None) -> dict[str, Any]:
    with get_connection(db_path) as conn:
        open_work_orders = conn.execute(
            "SELECT COUNT(*) AS c FROM work_orders WHERE status IN ('OPEN', 'IN_PROGRESS')"
        ).fetchone()["c"]

        open_incidents = conn.execute(
            "SELECT COUNT(*) AS c FROM incidents WHERE status IN ('OPEN', 'INVESTIGATING')"
        ).fetchone()["c"]

        low_stock = conn.execute(
            "SELECT COUNT(*) AS c FROM inventory_items WHERE current_stock <= reorder_level"
        ).fetchone()["c"]

        tonnes = conn.execute(
            "SELECT COALESCE(SUM(tonnes_processed), 0) AS t FROM production_logs"
        ).fetchone()["t"]

        return {
            "open_work_orders": int(open_work_orders),
            "open_incidents": int(open_incidents),
            "low_stock_items": int(low_stock),
            "total_tonnes_processed": float(tonnes),
            "generated_at": datetime.now(UTC),
        }
