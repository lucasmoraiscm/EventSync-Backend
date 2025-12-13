from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from src.infra.storage.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    foto_url = Column(String, nullable=False)
    visibilidade_participacao = Column(Boolean, default=True)
    rating_organizador = Column(Float, default=0.0)
    role = Column(String, default="participante")
    
    registrations = relationship("Registration", back_populates="user")
    events_created = relationship("Event", back_populates="organizador")
    
    friendships_sent = relationship("Friendship", foreign_keys="Friendship.solicitante_id", back_populates="solicitante")
    friendships_received = relationship("Friendship", foreign_keys="Friendship.destinatario_id", back_populates="destinatario")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    organizador_id = Column(Integer, ForeignKey("users.id"))
    titulo = Column(String, nullable=False)
    descricao = Column(Text)
    local = Column(String)
    local_url = Column(String, nullable=True)
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    tipo = Column(String)
    preco = Column(Float, default=0.0)
    exige_aprovacao = Column(Boolean, default=False)
    status = Column(String, default="rascunho") 
    n_checkins_permitidos = Column(Integer, default=1)
    max_inscricoes = Column(Integer, nullable=True)
    carga_horaria = Column(Integer, nullable=True)
    banner_url = Column(String, nullable=True)
    
    organizador = relationship("User", back_populates="events_created")
    registrations = relationship("Registration", back_populates="event")
    reviews = relationship("Review", back_populates="event")

class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    status = Column(String, default="pendente") 
    created_at = Column(DateTime, default=datetime.utcnow)
    certificado_emitido = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")
    checkins = relationship("Checkin", back_populates="registration")

class Checkin(Base):
    __tablename__ = "checkins"
    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, ForeignKey("registrations.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    metodo = Column(String, default="manual")
    
    registration = relationship("Registration", back_populates="checkins")

class Friendship(Base):
    __tablename__ = "friendships"
    id = Column(Integer, primary_key=True, index=True)
    solicitante_id = Column(Integer, ForeignKey("users.id"))
    destinatario_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pendente")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    solicitante = relationship("User", foreign_keys=[solicitante_id], back_populates="friendships_sent")
    destinatario = relationship("User", foreign_keys=[destinatario_id], back_populates="friendships_received")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    nota = Column(Integer)
    comentario = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    event = relationship("Event", back_populates="reviews")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    remetente_id = Column(Integer, ForeignKey("users.id"))
    destinatario_id = Column(Integer, ForeignKey("users.id"))
    titulo = Column(String, nullable=False)
    conteudo = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    remetente = relationship("User", foreign_keys=[remetente_id])
    destinatario = relationship("User", foreign_keys=[destinatario_id])
