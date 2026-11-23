import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.config.settings import settings
from app.config.database import Base, engine
from app.exceptions.custom_exceptions import AppException
from app.exceptions.handlers import app_exception_handler, validation_exception_handler

# Import Routers
from app.controllers.auth_controller import router as auth_router
from app.controllers.train_controller import router as train_router
from app.controllers.train_class_controller import router as class_router
from app.controllers.passenger_controller import router as passenger_router
from app.controllers.ticket_controller import router as ticket_router
from app.controllers.payment_controller import router as payment_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def init_db():
    """Initializes tables in database."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified.")
    except Exception as e:
        logger.warning(f"Database connection note: {e}")


app = FastAPI(
    title=settings.APP_NAME,
    description="Production-grade RESTful API for RailBook Pro Train Ticket Booking System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)

# Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for easy local development & mobile access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


# Mount Routers under API_V1_PREFIX (/api/v1)
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(train_router, prefix=settings.API_V1_PREFIX)
app.include_router(class_router, prefix=settings.API_V1_PREFIX)
app.include_router(passenger_router, prefix=settings.API_V1_PREFIX)
app.include_router(ticket_router, prefix=settings.API_V1_PREFIX)
app.include_router(payment_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint to verify backend service status."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": str(engine.url),
    }


@app.get("/", tags=["Root"])
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API. Visit /docs for Swagger documentation."
    }
