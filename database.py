from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ensure tables are created if they don't exist
def initialize_database():
    """
    Initialize the database by creating all tables defined in models
    if they don't already exist.
    """
    from models import Base  # Import Base from models to register all models
    Base.metadata.create_all(bind=engine)