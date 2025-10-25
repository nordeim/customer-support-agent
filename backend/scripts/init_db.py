#!/usr/bin/env python3
"""
 =============================================================================
 Customer Support AI Agent - Database Initialization Script
 =============================================================================

 This script initializes the database with all necessary tables and seed data.
 It supports both SQLite and PostgreSQL databases.

 Usage:
     python scripts/init_db.py [--force] [--seed] [--migrate]

 Options:
     --force     Drop existing tables before creating new ones
     --seed      Insert seed data after table creation
     --migrate   Run database migrations before initialization
     --verbose   Enable verbose logging
"""

import argparse
import logging
import sys
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.db.database import engine, SessionLocal, Base
from app.db.models import Session, Message, MemoryEntry, Attachment
from app.core.config import settings
from app.core.logging import setup_logging
from alembic.config import Config
from alembic import command

# Configure logging
logger = logging.getLogger(__name__)

class DatabaseInitializer:
    """Handles database initialization operations"""
    
    def __init__(self, force: bool = False, seed: bool = False, migrate: bool = False):
        self.force = force
        self.seed = seed
        self.migrate = migrate
        self.db_session = SessionLocal()
        
    def run_migrations(self) -> bool:
        """Run database migrations using Alembic"""
        try:
            logger.info("Running database migrations...")
            
            # Configure Alembic
            alembic_cfg = Config("alembic.ini")
            alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
            
            # Run migrations
            command.upgrade(alembic_cfg, "head")
            
            logger.info("Database migrations completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to run migrations: {str(e)}")
            return False
    
    def drop_tables(self) -> bool:
        """Drop all existing tables"""
        try:
            if self.force:
                logger.warning("Dropping all existing tables...")
                Base.metadata.drop_all(bind=engine)
                logger.info("All tables dropped successfully")
                return True
            else:
                logger.info("Skipping table drop (use --force to enable)")
                return True
                
        except Exception as e:
            logger.error(f"Failed to drop tables: {str(e)}")
            return False
    
    def create_tables(self) -> bool:
        """Create all database tables"""
        try:
            logger.info("Creating database tables...")
            
            # Create all tables
            Base.metadata.create_all(bind=engine)
            
            # Verify tables were created
            inspector = engine.dialect.get_inspector(engine)
            tables = inspector.get_table_names()
            
            logger.info(f"Created {len(tables)} tables: {', '.join(tables)}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create tables: {str(e)}")
            return False
    
    def insert_seed_data(self) -> bool:
        """Insert seed data into the database"""
        try:
            if not self.seed:
                logger.info("Skipping seed data insertion (use --seed to enable)")
                return True
            
            logger.info("Inserting seed data...")
            
            # Seed sessions
            self._seed_sessions()
            
            # Seed memory entries
            self._seed_memory_entries()
            
            # Seed messages
            self._seed_messages()
            
            logger.info("Seed data inserted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to insert seed data: {str(e)}")
            return False
    
    def _seed_sessions(self) -> None:
        """Seed sample sessions"""
        sample_sessions = [
            {
                "id": "demo-session-1",
                "user_id": "demo-user-1",
                "is_active": True
            },
            {
                "id": "demo-session-2",
                "user_id": "demo-user-2",
                "is_active": True
            }
        ]
        
        for session_data in sample_sessions:
            session = Session(**session_data)
            self.db_session.add(session)
        
        self.db_session.commit()
        logger.info(f"Created {len(sample_sessions)} sample sessions")
    
    def _seed_memory_entries(self) -> None:
        """Seed sample memory entries"""
        sample_memories = [
            {
                "session_id": "demo-session-1",
                "key": "user_preference",
                "value": "dark_mode"
            },
            {
                "session_id": "demo-session-1",
                "key": "user_name",
                "value": "John Doe"
            },
            {
                "session_id": "demo-session-2",
                "key": "user_preference",
                "value": "light_mode"
            }
        ]
        
        for memory_data in sample_memories:
            memory = MemoryEntry(**memory_data)
            self.db_session.add(memory)
        
        self.db_session.commit()
        logger.info(f"Created {len(sample_memories)} sample memory entries")
    
    def _seed_messages(self) -> None:
        """Seed sample messages"""
        sample_messages = [
            {
                "session_id": "demo-session-1",
                "content": "Hello, I need help with my order",
                "role": "user"
            },
            {
                "session_id": "demo-session-1",
                "content": "I'd be happy to help you with your order. Could you please provide your order number?",
                "role": "assistant"
            },
            {
                "session_id": "demo-session-2",
                "content": "How do I reset my password?",
                "role": "user"
            },
            {
                "session_id": "demo-session-2",
                "content": "To reset your password, click on the 'Forgot Password' link on the login page and follow the instructions.",
                "role": "assistant"
            }
        ]
        
        for message_data in sample_messages:
            message = Message(**message_data)
            self.db_session.add(message)
        
        self.db_session.commit()
        logger.info(f"Created {len(sample_messages)} sample messages")
    
    def verify_database(self) -> bool:
        """Verify database integrity"""
        try:
            logger.info("Verifying database integrity...")
            
            # Check if all tables exist
            inspector = engine.dialect.get_inspector(engine)
            expected_tables = ['sessions', 'messages', 'memory_entries', 'attachments']
            existing_tables = inspector.get_table_names()
            
            missing_tables = set(expected_tables) - set(existing_tables)
            if missing_tables:
                logger.error(f"Missing tables: {', '.join(missing_tables)}")
                return False
            
            # Check table counts
            session_count = self.db_session.query(Session).count()
            message_count = self.db_session.query(Message).count()
            memory_count = self.db_session.query(MemoryEntry).count()
            
            logger.info(f"Database verification passed:")
            logger.info(f"  - Sessions: {session_count}")
            logger.info(f"  - Messages: {message_count}")
            logger.info(f"  - Memory entries: {memory_count}")
            
            return True
            
        except Exception as e:
            logger.error(f"Database verification failed: {str(e)}")
            return False
    
    def initialize(self) -> bool:
        """Run the complete database initialization process"""
        logger.info("Starting database initialization...")
        logger.info(f"Database URL: {settings.database_url}")
        logger.info(f"Force mode: {self.force}")
        logger.info(f"Seed data: {self.seed}")
        logger.info(f"Run migrations: {self.migrate}")
        
        try:
            # Step 1: Run migrations if requested
            if self.migrate:
                if not self.run_migrations():
                    return False
            
            # Step 2: Drop existing tables if force mode
            if not self.drop_tables():
                return False
            
            # Step 3: Create tables
            if not self.create_tables():
                return False
            
            # Step 4: Insert seed data if requested
            if not self.insert_seed_data():
                return False
            
            # Step 5: Verify database
            if not self.verify_database():
                return False
            
            logger.info("Database initialization completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            return False
        
        finally:
            self.db_session.close()
    
    def cleanup(self) -> None:
        """Clean up resources"""
        if self.db_session:
            self.db_session.close()

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Initialize the Customer Support AI Agent database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/init_db.py                          # Basic initialization
    python scripts/init_db.py --force                  # Drop and recreate tables
    python scripts/init_db.py --seed                   # Initialize with seed data
    python scripts/init_db.py --migrate                # Run migrations first
    python scripts/init_db.py --force --seed --migrate  # Full initialization
        """
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Drop existing tables before creating new ones"
    )
    
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Insert seed data after table creation"
    )
    
    parser.add_argument(
        "--migrate",
        action="store_true",
        help="Run database migrations before initialization"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser.parse_args()

def main() -> int:
    """Main entry point"""
    # Parse arguments
    args = parse_arguments()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging()
    logging.getLogger().setLevel(log_level)
    
    # Create initializer
    initializer = DatabaseInitializer(
        force=args.force,
        seed=args.seed,
        migrate=args.migrate
    )
    
    try:
        # Run initialization
        success = initializer.initialize()
        
        if success:
            print("\n✅ Database initialization completed successfully!")
            return 0
        else:
            print("\n❌ Database initialization failed!")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Database initialization interrupted by user")
        print("\n⚠️  Database initialization interrupted")
        return 1
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\n❌ Unexpected error: {str(e)}")
        return 1
    
    finally:
        initializer.cleanup()

if __name__ == "__main__":
    sys.exit(main())
