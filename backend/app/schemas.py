from pydantic import BaseModel, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    country: Optional[str] = "India"
    building_code: Optional[str] = "NBC-2016"

class ProjectResponse(BaseModel):
    id: UUID4
    name: str
    country: str
    building_code: str
    status: str
    created_at: datetime

class DrawingUploadResponse(BaseModel):
    id: UUID4
    filename: str
    status: str

class EntityResponse(BaseModel):
    id: UUID4
    entity_type: str
    layer: str
    geometry: Dict
    properties: Dict

class DetectedObjectResponse(BaseModel):
    id: UUID4
    object_type: str
    confidence: float
    geometry: Dict
    properties: Dict
    verified: bool

class QuantityResponse(BaseModel):
    item_type: str
    gross: float
    deduction: float
    net: float
    unit: str

class BOQItemResponse(BaseModel):
    id: UUID4
    description: str
    quantity: float
    unit: str
    rate: float
    amount: float
    category: str