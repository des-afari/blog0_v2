from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .model import Category
from .schemas import CategorySchema, CategoryResponse
from api.article.schemas import ArticleResponse
from api.article.model import Article
from utils.session import get_db
from api.user.oauth2 import get_user
from typing import List

router = APIRouter()


@router.post('/create', status_code=201, response_model=CategoryResponse)
async def create_category(schema: CategorySchema, db: Session = Depends(get_db), user = Depends(get_user)):
    if not user.role == 'admin':
        raise HTTPException(403, detail='Operation not allowed')
    
    if db.query(Category).filter(Category.name == schema.name).first():
        raise HTTPException(409, detail='Category already exists')
    
    category = Category(**schema.model_dump())
    category.set_slug()

    db.add(category)
    db.commit()

    return category


@router.delete('/{id}/delete', status_code=204)
async def delete_category(id: int, db: Session = Depends(get_db), user = Depends(get_user)):
    if not user.role == 'admin':
        raise HTTPException(403, detail='Operation not allowed')

    category = db.query(Category).get(id)

    if not category:
        raise HTTPException(404, detail='Category not found')

    db.delete(category) 
    db.commit()


@router.get('/{name}', status_code=200, response_model=List[ArticleResponse])
async def get_articles_by_tag(name: str, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(Article.categories.any(name=name)).all()
        
    if not articles:
        raise HTTPException(404, detail='Articles not found')

    return articles