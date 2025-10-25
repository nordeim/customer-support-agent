# backend/scripts/init_db.py
from app.db.database import engine
from app.db.models import Base
from app.core.logging import logger, setup_logging

def init_db():
    """Initialize the database with all tables"""
    # Setup logging
    setup_logging()
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    logger.info("Database initialized successfully")

if __name__ == "__main__":
    init_db()
