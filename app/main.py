from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, child, answers, prediction_result
from app.routes import auth
from app.routes import child as child_router
from app.routes import questionnaire
from app.routes import prediction
from app.routes import password_reset
from fastapi.middleware.cors import CORSMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ ADD CORS MIDDLEWARE HERE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (OK for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(child_router.router)
app.include_router(questionnaire.router)
app.include_router(prediction.router)
app.include_router(password_reset.router)

@app.get("/")
def root():
    return {"status": "Backend running"}
