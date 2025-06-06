"""Database singleton module for managing database connections."""
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

class DatabaseSingleton:
    """Singleton class for managing database connections."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Create a new instance if one doesn't exist."""
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the database connection if not already initialized."""
        if not DatabaseSingleton._initialized:
            # Database configuration
            self.database_url = "sqlite:///./sport_store.db"
            self.engine = create_engine(
                self.database_url,
                connect_args={"check_same_thread": False}
            )
            self.session_local = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            self.base = declarative_base()
            DatabaseSingleton._initialized = True
            self._session: Optional[Session] = None
    
    @property
    def session(self) -> Session:
        """Get the current database session."""
        if self._session is None:
            self._session = self.session_local()
        return self._session
    
    def close(self) -> None:
        """Close the current database session."""
        if self._session is not None:
            self._session.close()
            self._session = None

    def create_tables(self):
        """Create all tables in the database."""
        self.base.metadata.create_all(bind=self.engine)

def get_db() -> Optional[Session]:
    """Dependency for FastAPI to get database session."""
    db = DatabaseSingleton().session
    try:
        return db
    finally:
        db.close() 