from __future__ import annotations

import hashlib
import os
import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(os.getenv("OIS_DB_PATH", "operations.db"))


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    path = db_path or str(DB_PATH)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    with get_connection(db_path) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS sites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('ACTIVE', 'INACTIVE'))
            );

            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                type TEXT NOT NULL,
                site_id INTEGER NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('OPERATIONAL', 'DOWN', 'MAINTENANCE')),
                hours_runtime REAL NOT NULL DEFAULT 0,
                FOREIGN KEY (site_id) REFERENCES sites(id)
            );

            CREATE TABLE IF NOT EXISTS production_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_id INTEGER NOT NULL,
                shift_date TEXT NOT NULL,
                tonnes_processed REAL NOT NULL CHECK (tonnes_processed >= 0),
                downtime_minutes INTEGER NOT NULL CHECK (downtime_minutes >= 0),
                notes TEXT,
                FOREIGN KEY (site_id) REFERENCES sites(id)
            );

            CREATE TABLE IF NOT EXISTS work_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipment_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                priority TEXT NOT NULL CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
                status TEXT NOT NULL CHECK (status IN ('OPEN', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
                created_at TEXT NOT NULL,
                due_date TEXT,
                completed_at TEXT,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id)
            );

            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_id INTEGER NOT NULL,
                severity TEXT NOT NULL CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
                description TEXT NOT NULL,
                reported_at TEXT NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('OPEN', 'INVESTIGATING', 'CLOSED')),
                lost_time_injuries INTEGER NOT NULL DEFAULT 0 CHECK (lost_time_injuries IN (0,1)),
                FOREIGN KEY (site_id) REFERENCES sites(id)
            );

            CREATE TABLE IF NOT EXISTS inventory_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                unit TEXT NOT NULL,
                current_stock REAL NOT NULL CHECK (current_stock >= 0),
                reorder_level REAL NOT NULL CHECK (reorder_level >= 0),
                site_id INTEGER NOT NULL,
                FOREIGN KEY (site_id) REFERENCES sites(id)
            );

            CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                movement_type TEXT NOT NULL CHECK (movement_type IN ('IN', 'OUT')),
                quantity REAL NOT NULL CHECK (quantity > 0),
                reference TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (item_id) REFERENCES inventory_items(id)
            );

            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1))
            );
            """
        )


def seed_demo_data(db_path: Optional[str] = None) -> None:
    with get_connection(db_path) as conn:
        existing_sites = conn.execute("SELECT COUNT(*) AS c FROM sites").fetchone()["c"]
        if not existing_sites:
            conn.executemany(
                "INSERT INTO sites (name, location, status) VALUES (?, ?, ?)",
                [
                    ("Kansanshi", "Solwezi", "ACTIVE"),
                    ("Sentinel", "Kalumbila", "ACTIVE"),
                ],
            )

            conn.executemany(
                "INSERT INTO equipment (code, type, site_id, status, hours_runtime) VALUES (?, ?, ?, ?, ?)",
                [
                    ("EX-100", "Excavator", 1, "OPERATIONAL", 12200),
                    ("TR-220", "Haul Truck", 1, "MAINTENANCE", 18400),
                    ("CR-010", "Crusher", 2, "OPERATIONAL", 25100),
                ],
            )

            conn.executemany(
                "INSERT INTO inventory_items (sku, name, unit, current_stock, reorder_level, site_id) VALUES (?, ?, ?, ?, ?, ?)",
                [
                    ("LUBE-5W30", "Engine Oil 5W-30", "L", 520, 200, 1),
                    ("TYRE-797F", "Heavy Truck Tyre", "EA", 6, 8, 1),
                    ("BLAST-CAP", "Blasting Caps", "EA", 1200, 900, 2),
                ],
            )

        existing_users = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]
        if not existing_users:
            conn.executemany(
                "INSERT INTO users (username, full_name, role, password_hash, is_active) VALUES (?, ?, ?, ?, ?)",
                [
                    ("manager", "Operations Manager", "Manager", hash_password("manager123"), 1),
                    ("safety", "Safety Officer", "Safety", hash_password("safety123"), 1),
                    ("inventory", "Inventory Controller", "Inventory", hash_password("inventory123"), 1),
                ],
            )
