from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID  # Remove this if not used
from sqlalchemy.orm import relationship
from .database import Base
import uuid
from datetime import datetime

# UUID ને બદલે String(36) વાપરો
class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Project(Base):
    __tablename__ = "projects"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    name = Column(String, nullable=False)
    country = Column(String, default="India")
    building_code = Column(String, default="NBC-2016")
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    drawings = relationship("Drawing", back_populates="project")

class Drawing(Base):
    __tablename__ = "drawings"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"))
    filename = Column(String)
    filepath = Column(String)
    status = Column(String, default="uploaded")
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="drawings")
    entities = relationship("DrawingEntity", back_populates="drawing")
    objects = relationship("DetectedObject", back_populates="drawing")

class DrawingEntity(Base):
    __tablename__ = "drawing_entities"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    drawing_id = Column(String(36), ForeignKey("drawings.id"))
    entity_type = Column(String)
    layer = Column(String)
    geometry = Column(JSON)
    properties = Column(JSON)
    drawing = relationship("Drawing", back_populates="entities")

class DetectedObject(Base):
    __tablename__ = "detected_objects"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    drawing_id = Column(String(36), ForeignKey("drawings.id"))
    object_type = Column(String)
    confidence = Column(Float)
    geometry = Column(JSON)
    properties = Column(JSON)
    verified = Column(Boolean, default=False)
    drawing = relationship("Drawing", back_populates="objects")

class Quantity(Base):
    __tablename__ = "quantities"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"))
    item_type = Column(String)
    gross = Column(Float)
    deduction = Column(Float, default=0)
    net = Column(Float)
    unit = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class BOQItem(Base):
    __tablename__ = "boq_items"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"))
    description = Column(String)
    quantity = Column(Float)
    unit = Column(String)
    rate = Column(Float)
    amount = Column(Float)
    category = Column(String)