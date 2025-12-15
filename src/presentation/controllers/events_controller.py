from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

from src.domain import models, schemas
from src.application.services.event_service import EventService
from src.application.services.registration_service import RegistrationService
from src.application.services.checkin_service import CheckinService
from src.application.services.friend_service import FriendService
from src.application.services.review_service import ReviewService
from src.application.services.certificate_service import CertificateService
from src.application.services.report_service import ReportService


class EventController:
    def __init__(self, db: Session):
        self.db = db


    def create_event(self, event: schemas.EventCreate, user: models.User):
        event_service = EventService(self.db)
        return event_service.create_event(event, user)
    
    
    def edit_event(self, event_id: int, event: schemas.EventUpdate, user: models.User):
        event_service = EventService(self.db)
        return event_service.update_event(event_id, event, user)
    

    def list_events(
        self, 
        skip: int, 
        limit: int,
        titulo: str = None,
        tipo: str = None,
        data_inicio: str = None,
        organizador_id: int = None
    ):
        event_service = EventService(self.db)
        return event_service.list_events(
            skip, 
            limit, 
            titulo, 
            tipo, 
            data_inicio,
            organizador_id
        )

    
    def get_event_details(self, event_id: int):
        event_service = EventService(self.db)
        return event_service.get_event_details(event_id)
    

    def open_inscriptions(self, event_id: int, user: models.User):
        event_service = EventService(self.db)
        return event_service.change_event_status(event_id, schemas.EventStatus.INSCRICOES_ABERTAS, user)
    

    def close_inscriptions(self, event_id: int, user: models.User):
        event_service = EventService(self.db)
        return event_service.change_event_status(event_id, schemas.EventStatus.INSCRICOES_ENCERRADAS, user)
    

    def publish_event(self, event_id: int, user: models.User):
        event_service = EventService(self.db)
        return event_service.change_event_status(event_id, schemas.EventStatus.PUBLICADO, user)
    

    def finish_event(self, event_id: int, user: models.User):
        event_service = EventService(self.db)
        return event_service.change_event_status(event_id, schemas.EventStatus.FINALIZADO, user)
    

    def register_in_event(self, event_id: int, user_id: int):
        registration_service = RegistrationService(self.db)
        return registration_service.register_user(event_id, user_id)
    

    def list_event_registrations(self, event_id: int, user: models.User):
        registration_service = RegistrationService(self.db)
        return registration_service.list_event_registrations(event_id, user)


    def checkin(self, event_id: int, user_id: int, user: models.User):
        checkin_service = CheckinService(self.db)
        result = checkin_service.perform_checkin(event_id, user_id, user)
        
        return {"message": "Check-in realizado com sucesso", "timestamp": result.timestamp}
    

    def send_friend_request(self, event_id: int, solicitante_id: int, destinatario_id: int):
        friend_service = FriendService(self.db)
        return friend_service.request_friendship(event_id, solicitante_id, destinatario_id)
    

    def review_event(self, event_id: int, user_id: int, review: schemas.ReviewCreate):
        review_service = ReviewService(self.db)
        return review_service.create_review(event_id, user_id, review)
    

    def download_certificate(self, event_id: int, user_id: int):
        certificate_service = CertificateService(self.db)
        pdf_buffer = certificate_service.generate_certificate_pdf(event_id, user_id)
        
        return StreamingResponse(
            pdf_buffer, 
            media_type="application/pdf", 
            headers={"Content-Disposition": f"attachment; filename=certificado_evento_{event_id}.pdf"}
        )
    

    def export_event_registrations(self, event_id: int, user: models.User):
        report_service = ReportService(self.db)
        csv_file = report_service.export_registrations_csv(event_id, user)
        
        filename = f"inscritos_evento_{event_id}.csv"
        
        return StreamingResponse(
            iter([csv_file.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
