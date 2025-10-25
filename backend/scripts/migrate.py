# backend/scripts/migrate.py
import argparse
from alembic.config import Config
from alembic import command
from app.core.logging import logger, setup_logging

def migrate(direction: str, revision: str = None):
    """Run database migrations"""
    # Setup logging
    setup_logging()
    
    # Load Alembic configuration
    alembic_cfg = Config("alembic.ini")
    
    try:
        if direction == "upgrade":
            if revision:
                command.upgrade(alembic_cfg, revision)
            else:
                command.upgrade(alembic_cfg, "head")
            logger.info(f"Database upgraded to revision: {revision or 'head'}")
        elif direction == "downgrade":
            if not revision:
                raise ValueError("Revision is required for downgrade")
            command.downgrade(alembic_cfg, revision)
            logger.info(f"Database downgraded to revision: {revision}")
        else:
            raise ValueError(f"Invalid migration direction: {direction}")
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run database migrations")
    parser.add_argument("direction", choices=["upgrade", "downgrade"], help="Migration direction")
    parser.add_argument("--revision", help="Target revision (required for downgrade)")
    args = parser.parse_args()
    
    migrate(args.direction, args.revision)
