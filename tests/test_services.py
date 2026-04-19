from __future__ import annotations

from pathlib import Path

import pytest

from mining_ois.core import services
from mining_ois.db.database import init_db, seed_demo_data


@pytest.fixture()
def db_path(tmp_path: Path) -> str:
    db_file = tmp_path / "test_ops.db"
    init_db(str(db_file))
    seed_demo_data(str(db_file))
    return str(db_file)


def test_out_movement_reduces_stock(db_path: str) -> None:
    low_stock_before = services.list_low_stock(db_path)

    movement_id = services.record_stock_movement(
        {
            "item_id": 1,
            "movement_type": "OUT",
            "quantity": 20,
            "reference": "WO-1001",
        },
        db_path,
    )

    assert movement_id > 0
    low_stock_after = services.list_low_stock(db_path)
    assert len(low_stock_after) == len(low_stock_before)


def test_out_movement_cannot_go_negative(db_path: str) -> None:
    with pytest.raises(ValueError):
        services.record_stock_movement(
            {
                "item_id": 2,
                "movement_type": "OUT",
                "quantity": 1000,
                "reference": "BAD-REQ",
            },
            db_path,
        )


def test_dashboard_reflects_new_records(db_path: str) -> None:
    services.create_production_log(
        {
            "site_id": 1,
            "shift_date": "2026-04-16",
            "tonnes_processed": 9000,
            "downtime_minutes": 15,
            "notes": "Nominal shift",
        },
        db_path,
    )

    wo_id = services.create_work_order(
        {
            "equipment_id": 1,
            "title": "Replace hydraulic hose",
            "priority": "HIGH",
            "due_date": "2026-04-18",
        },
        db_path,
    )

    services.create_incident(
        {
            "site_id": 1,
            "severity": "MEDIUM",
            "description": "Slip hazard near workshop",
            "lost_time_injuries": False,
        },
        db_path,
    )

    summary = services.get_operational_summary(db_path)

    assert summary["open_work_orders"] >= 1
    assert summary["open_incidents"] >= 1
    assert summary["total_tonnes_processed"] >= 9000

    services.update_work_order_status(wo_id, "COMPLETED", db_path)
    summary_after = services.get_operational_summary(db_path)
    assert summary_after["open_work_orders"] == summary["open_work_orders"] - 1
