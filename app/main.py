from fastapi import FastAPI
from app.api.v1.routes import router as v1_router
import logging
from app.config import OPENAI_API_KEY

app = FastAPI()

app.include_router(v1_router, prefix="/api/v1")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log environment variable status at startup
logger.info("Application starting with environment variables:")
logger.info(f"OPENAI_API_KEY set: {'Yes' if OPENAI_API_KEY else 'No'}")

@app.get("/")
def read_root():
    return {"message": "Dwelio A.I. is up and running."}