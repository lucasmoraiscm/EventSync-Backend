from fastapi import FastAPI

from src.infra.storage.database import Base, engine
from src.presentation.routes import auth, events, users, registrations, friends, messages

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EventSync API", version="1.0.0")

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(users.router)
app.include_router(registrations.router)
app.include_router(friends.router)
app.include_router(messages.router)

@app.get("/")
def root():
    return {"message": "EventSync API is running"}
