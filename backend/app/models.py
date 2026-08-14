from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Project(Base):
    __tablename__ = "projects"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(String, nullable=False)
    country = Column(String, default="India")
    building_code = Column(String, default="NBC-2016")
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    drawings = relationship("Drawing", back_populates="project")

class Drawing(Base):
    __tablename__ = "drawings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    filename = Column(String)
    filepath = Column(String)
    status = Column(String, default="uploaded")
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="drawings")
    entities = relationship("DrawingEntity", back_populates="drawing")
    objects = relationship("DetectedObject", back_populates="drawing")

class DrawingEntity(Base):
    __tablename__ = "drawing_entities"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    drawing_id = Column(UUID(as_uuid=True), ForeignKey("drawings.id"))
    entity_type = Column(String)
    layer = Column(String)
    geometry = Column(JSON)   # {start: [x,y], end: [x,y]} or vertices etc.
    properties = Column(JSON)
    drawing = relationship("Drawing", back_populates="entities")

class DetectedObject(Base):
    __tablename__ = "detected_objects"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    drawing_id = Column(UUID(as_uuid=True), ForeignKey("drawings.id"))
    object_type = Column(String)   # wall, door, window, room
    confidence = Column(Float)
    geometry = Column(JSON)
    properties = Column(JSON)
    verified = Column(Boolean, default=False)
    drawing = relationship("Drawing", back_populates="objects")

class Quantity(Base):
    __tablename__ = "quantities"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    item_type = Column(String)   # wall, floor, plaster, painting
    gross = Column(Float)
    deduction = Column(Float, default=0)
    net = Column(Float)
    unit = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class BOQItem(Base):
    __tablename__ = "boq_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    description = Column(String)
    quantity = Column(Float)
    unit = Column(String)
    rate = Column(Float)
    amount = Column(Float)
    category = Column(String)