from sqlalchemy import create_engine,engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_URL='sqlite:///./Product.db'
engine = create_engine(SQL_DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        print("db not there")
    
    finally:
        db.close()    