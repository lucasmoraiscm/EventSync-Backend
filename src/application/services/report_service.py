from sqlalchemy.orm import Session
from fastapi import HTTPException
import csv
import io

from src.domain import models
from src.persistence.repositories import event_repo, registration_repo


class ReportService:
    def __init__(self, db: Session):
        self.db = db


    def export_registrations_csv(self, event_id: int, user: models.User):
        event = event_repo.get_event_by_id(self.db, event_id)

        if not event:
            raise HTTPException(status_code=404, detail="Evento não encontrado")

        if event.organizador_id != user.id:
            raise HTTPException(status_code=403, detail="Apenas o organizador pode exportar a lista.")

        registrations = registration_repo.get_registrations_by_event(self.db, event_id)

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["ID Inscrição", "Nome", "Email", "Cidade", "Status", "Data Inscrição", "Check-ins"])

        for reg in registrations:
            writer.writerow([
                reg.id,
                reg.user.nome,
                reg.user.email,
                reg.user.cidade or "N/A",
                reg.status,
                reg.created_at.strftime("%d/%m/%Y %H:%M"),
                len(reg.checkins)
            ])

        output.seek(0)
        return output
    