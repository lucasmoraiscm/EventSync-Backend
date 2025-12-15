from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class EventStatus(str, Enum):
    RASCUNHO = "rascunho"
    PUBLICADO = "publicado"
    INSCRICOES_ABERTAS = "inscricoes_abertas"
    INSCRICOES_ENCERRADAS = "inscricoes_encerradas"
    FINALIZADO = "finalizado"
    CANCELADO = "cancelado"

class RegistrationStatus(str, Enum):
    PENDENTE = "pendente"
    APROVADA = "aprovada"
    RECUSADA = "recusada"
    AGUARDANDO_PAGAMENTO = "aguardando_pagamento"

class FriendshipStatus(str, Enum):
    PENDENTE = "pendente"
    ACEITO = "aceito"
    RECUSADO = "recusado"

class UserCreate(BaseModel):
    nome: str
    email: str
    senha: str
    cidade: str
    foto_url: str
    role: str = "participante" # organizador/participante

class UserResponse(BaseModel):
    id: int
    nome: str
    email: str
    cidade: str
    foto_url: str
    visibilidade_participacao: bool
    rating_organizador: float
    role: str
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    cidade: Optional[str] = None
    foto_url: Optional[str] = None
    visibilidade_participacao: Optional[bool] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class EventCreate(BaseModel):
    titulo: str
    descricao: str
    local: str
    local_url: Optional[str] = None
    data_inicio: datetime
    data_fim: datetime
    tipo: str = "gratuito" # gratuito/pago
    preco: float = 0.0
    exige_aprovacao: bool = False
    max_inscricoes: Optional[int] = None
    n_checkins_permitidos: int = 1
    carga_horaria: Optional[int] = None
    banner_url: Optional[str] = None

class EventResponse(EventCreate):
    id: int
    organizador_id: int
    status: EventStatus
    organizador: Optional[UserResponse] = None
    class Config:
        from_attributes = True

class EventUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    local: Optional[str] = None
    local_url: Optional[str] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    tipo: Optional[str] = None
    preco: Optional[float] = None
    exige_aprovacao: Optional[bool] = None
    max_inscricoes: Optional[int] = None
    n_checkins_permitidos: Optional[int] = None
    carga_horaria: Optional[int] = None
    banner_url: Optional[str] = None
    status: Optional[EventStatus] = None

class CheckinRequest(BaseModel):
    user_id: int

class CheckinResponse(BaseModel):
    id: int
    timestamp: datetime
    metodo: str
    class Config:
        from_attributes = True

class RegistrationResponse(BaseModel):
    id: int
    event_id: int
    user_id: int
    status: RegistrationStatus
    created_at: datetime
    event: Optional[EventResponse] = None
    user: Optional[UserResponse] = None
    checkins: List[CheckinResponse] = []
    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    nota: int = Field(..., ge=1, le=5)
    comentario: Optional[str] = None

class ReviewResponse(ReviewCreate):
    id: int
    event_id: int
    user_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class FriendshipCreate(BaseModel):
    destinatario_id: int

class FriendshipResponse(BaseModel):
    id: int
    solicitante_id: int
    destinatario_id: int
    status: FriendshipStatus
    created_at: datetime
    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    destinatario_id: int
    titulo: str
    conteudo: str

class MessageResponse(BaseModel):
    id: int
    remetente_id: int
    destinatario_id: int
    titulo: str
    conteudo: str
    timestamp: datetime
    class Config:
        from_attributes = True
