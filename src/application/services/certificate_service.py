from sqlalchemy.orm import Session
from fastapi import HTTPException
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from src.domain import schemas
from src.persistence.repositories import event_repo, registration_repo

class CertificateService:
    def __init__(self, db: Session):
        self.db = db

    def generate_certificate_pdf(self, event_id: int, user_id: int) -> BytesIO:
        event = event_repo.get_event_by_id(self.db, event_id)
        registration = registration_repo.get_registration(self.db, user_id, event_id)

        if not event or event.status != schemas.EventStatus.FINALIZADO:
             raise HTTPException(status_code=400, detail="Certificado disponível apenas após o fim do evento")
        
        if not registration or not registration.checkins:
             raise HTTPException(status_code=400, detail="Necessário check-in para emitir certificado")

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        p.setFont("Helvetica-Bold", 24)
        p.drawCentredString(width / 2, height - 100, "CERTIFICADO DE PARTICIPAÇÃO")
        
        p.setFont("Helvetica", 14)
        p.drawCentredString(width / 2, height - 200, "Certificamos que")
        
        p.setFont("Helvetica-Bold", 18)
        p.drawCentredString(width / 2, height - 230, registration.user.nome.upper())
        
        p.setFont("Helvetica", 14)
        text = f"participou do evento '{event.titulo}' realizado em {event.data_inicio.strftime('%d/%m/%Y')}."
        p.drawCentredString(width / 2, height - 280, text)
        
        if event.carga_horaria:
            p.drawCentredString(width / 2, height - 310, f"Carga Horária: {event.carga_horaria} horas")

        p.setFont("Helvetica-Oblique", 10)
        p.drawCentredString(width / 2, height - 500, f"Hash de Validação: {registration.id}-{event.id}-EVENTSYNC")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return buffer
