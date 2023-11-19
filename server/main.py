from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.session import get_db
from api.api_v1 import api_router
from typing import List, Optional
from api.category.model import Category
from api.category.schemas import CategoryResponse
from api.article.model import Article
from api.article.schemas import ArticleResponse
from fastapi.middleware.cors import CORSMiddleware # REMOVE IN PRODUCTION


app = FastAPI()

origins = [
    'http://localhost',
    'http://localhost:5173'
] # REMOVE IN PRODUCTION

# REMOVE IN PRODUCTION
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/', status_code=200)
async def root():
    return {"message": "connection established"}


@app.get('/api/v1/categories', status_code=200, response_model=List[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()

    if not categories:
        raise HTTPException(404, detail='Categories not found')
    
    return categories

@app.get('/api/v1/articles', status_code=200, response_model=List[ArticleResponse])
async def get_articles(
    db: Session = Depends(get_db), limit: int = 30, skip: int = 0, query: Optional[str] = ""
):
    query = query.lower().replace(' ', '-')

    articles = db.query(Article).filter(Article.title.contains(query)).limit(limit).offset(skip).all()

    if not articles:
        raise HTTPException(404, detail='Articles not found')

    return articles

app.include_router(api_router, prefix='/api/v1')