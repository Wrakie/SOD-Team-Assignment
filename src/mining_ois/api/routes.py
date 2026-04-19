from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi import Request

from mining_ois.core.models import (
    DashboardSummary,
    IncidentCreate,
    IncidentStatusUpdate,
    InventoryItemCreate,
    LoginRequest,
    ProductionLogCreate,
    StockMovementCreate,
    WorkOrderCreate,
    WorkOrderStatusUpdate,
)
from mining_ois.core import services
from mining_ois.db.database import get_connection, hash_password

router = APIRouter()


def _current_user(request: Request) -> dict:
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not logged in")
    return user


def _require_roles(request: Request, allowed_roles: set[str]) -> dict:
    user = _current_user(request)
    role = user.get("role")
    if role not in allowed_roles:
        raise HTTPException(status_code=403, detail="You are not allowed to perform this action")
    return user


@router.post("/auth/login")
def login(payload: LoginRequest, request: Request) -> dict[str, str]:
    username = payload.username
    password = payload.password

    with get_connection() as conn:
        user = conn.execute(
            "SELECT username, full_name, role, password_hash, is_active FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if user is None or not user["is_active"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user["password_hash"] != hash_password(password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    request.session["user"] = {
        "username": user["username"],
        "full_name": user["full_name"],
        "role": user["role"],
    }
    return {"message": "Login successful", "user": user["full_name"], "role": user["role"]}


@router.post("/auth/logout")
def logout(request: Request) -> dict[str, str]:
    request.session.pop("user", None)
    return {"message": "Logged out"}


@router.get("/auth/me")
def me(request: Request) -> dict:
    return _current_user(request)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/sites")
def get_sites(request: Request) -> list[dict]:
    _current_user(request)
    return services.list_sites()


@router.get("/equipment")
def get_equipment(request: Request) -> list[dict]:
    _current_user(request)
    return services.list_equipment()


@router.post("/production-logs", status_code=201)
def create_production_log(payload: ProductionLogCreate, request: Request) -> dict[str, int]:
    _require_roles(request, {"Manager"})
    try:
        row_id = services.create_production_log(payload.model_dump())
        return {"id": row_id}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/production-logs")
def get_production_logs(request: Request) -> list[dict]:
    _current_user(request)
    return services.list_production_logs()


@router.post("/work-orders", status_code=201)
def create_work_order(payload: WorkOrderCreate, request: Request) -> dict[str, int]:
    _require_roles(request, {"Manager"})
    try:
        row_id = services.create_work_order(payload.model_dump())
        return {"id": row_id}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.patch("/work-orders/{work_order_id}/status")
def patch_work_order_status(work_order_id: int, payload: WorkOrderStatusUpdate, request: Request) -> dict[str, str]:
    _require_roles(request, {"Manager"})
    try:
        services.update_work_order_status(work_order_id, payload.status)
        return {"message": "Work order status updated"}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/work-orders/open")
def get_open_work_orders(request: Request) -> list[dict]:
    _current_user(request)
    return services.list_open_work_orders()


@router.post("/incidents", status_code=201)
def create_incident(payload: IncidentCreate, request: Request) -> dict[str, int]:
    _require_roles(request, {"Manager", "Safety"})
    try:
        row_id = services.create_incident(payload.model_dump())
        return {"id": row_id}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.patch("/incidents/{incident_id}/status")
def patch_incident_status(incident_id: int, payload: IncidentStatusUpdate, request: Request) -> dict[str, str]:
    _require_roles(request, {"Manager", "Safety"})
    try:
        services.update_incident_status(incident_id, payload.status)
        return {"message": "Incident status updated"}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/incidents/open")
def get_open_incidents(request: Request) -> list[dict]:
    _current_user(request)
    return services.list_open_incidents()


@router.post("/inventory-items", status_code=201)
def create_inventory_item(payload: InventoryItemCreate, request: Request) -> dict[str, int]:
    _require_roles(request, {"Manager", "Inventory"})
    try:
        row_id = services.create_inventory_item(payload.model_dump())
        return {"id": row_id}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/inventory-items")
def get_inventory_items(request: Request) -> list[dict]:
    _current_user(request)
    return services.list_inventory_items()


@router.post("/inventory-movements", status_code=201)
def create_stock_movement(payload: StockMovementCreate, request: Request) -> dict[str, int]:
    _require_roles(request, {"Manager", "Inventory"})
    try:
        row_id = services.record_stock_movement(payload.model_dump())
        return {"id": row_id}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/inventory/low-stock")
def get_low_stock(request: Request) -> list[dict]:
    _current_user(request)
    return services.list_low_stock()


@router.get("/dashboard/summary", response_model=DashboardSummary)
def get_dashboard_summary(request: Request) -> DashboardSummary:
    _current_user(request)
    return DashboardSummary.model_validate(services.get_operational_summary())
