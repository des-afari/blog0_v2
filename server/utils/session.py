from db.base import DB_LOCAL

def get_db():
    db = DB_LOCAL()
    
    try:
        yield db
    
    finally:
        db.close()