from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductionLogCreate(BaseModel):
    site_id: int = Field(gt=0)
    shift_date: date
    tonnes_processed: float = Field(ge=0)
    downtime_minutes: int = Field(ge=0)
    notes: Optional[str] = None


class WorkOrderCreate(BaseModel):
    equipment_id: int = Field(gt=0)
    title: str = Field(min_length=3, max_length=120)
    priority: str
    due_date: Optional[date] = None


class WorkOrderStatusUpdate(BaseModel):
    status: str


class IncidentCreate(BaseModel):
    site_id: int = Field(gt=0)
    severity: str
    description: str = Field(min_length=5)
    lost_time_injuries: bool = False


class IncidentStatusUpdate(BaseModel):
    status: str


class InventoryItemCreate(BaseModel):
    sku: str = Field(min_length=2, max_length=40)
    name: str = Field(min_length=2, max_length=120)
    unit: str = Field(min_length=1, max_length=12)
    current_stock: float = Field(ge=0)
    reorder_level: float = Field(ge=0)
    site_id: int = Field(gt=0)


class StockMovementCreate(BaseModel):
    item_id: int = Field(gt=0)
    movement_type: str
    quantity: float = Field(gt=0)
    reference: Optional[str] = None


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=100)


class DashboardSummary(BaseModel):
    open_work_orders: int
    open_incidents: int
    low_stock_items: int
    total_tonnes_processed: float
    generated_at: datetime
