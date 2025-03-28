import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import routes as llm_routes
from app.api.v1 import employees, earning_rates
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="API for payroll management with AI assistance",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logging.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
    
    return response

# Include routers
app.include_router(llm_routes.router, prefix="/api/v1")
app.include_router(employees.router, prefix="/api/v1")
app.include_router(earning_rates.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to the AI-Powered Payroll API",
        "docs": "/docs",
        "redoc": "/redoc"
    }