from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.category.model import Category
from api.comment.model import Comment
from api.vote.model import Vote
from .model import Article
from .schemas import ArticleSchema, ArticleResponse, ArticleUpdateSchema
from utils.session import get_db
from api.user.oauth2 import get_user
from secrets import token_urlsafe

router = APIRouter()


@router.post('/create', status_code=201, response_model=ArticleResponse)
async def create_article(schema: ArticleSchema, db: Session = Depends(get_db), user = Depends(get_user)):
    if not user.role == 'admin':
        raise HTTPException(403, detail='Operation not allowed')
    
    schema.title = schema.title.lower().replace(' ', '-')

    if db.query(Article).filter(Article.title == schema.title).first():
        raise HTTPException(409, detail='Article already exists')
    
    article = Article(
        id=token_urlsafe(16),
        user_id=user.id,
        img_url=schema.img_url,
        title=schema.title,
        description=schema.description,
        content=schema.content
    )

    categories = db.query(Category).filter(Category.name.in_(schema.categories)).all()
    comments = db.query(Comment).filter(Comment.article_id == article.id).all()
    votes = db.query(Vote).filter(Vote.article_id == article.id).all()

    if not len(schema.categories) == len(categories):
        raise HTTPException(400, detail='Invalid categories')

 
    article.categories = categories
    article.comments = comments
    article.votes = votes

    db.add(article)
    db.commit()

    return article


@router.get('/{title}', status_code=200, response_model=ArticleResponse)
async def get_article(title: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.title == title).first()

    if not article:
        raise HTTPException(404, detail='Article not found')
    
    return article


@router.put('/{id}/update', status_code=200, response_model=ArticleResponse)
async def update_article(
    id: str, schema: ArticleUpdateSchema, db: Session = Depends(get_db), user = Depends(get_user)
):
    if not user.role == 'admin':
        raise HTTPException(403, detail='Operation not allowed')

    article = db.query(Article).get(id)

    if not article:
        raise HTTPException(404, detail='Article not found')
    
    if not article.user_id == user.id:
        raise HTTPException(403, detail='Operation not allowed')
    
    schema.title = schema.title.lower().replace(' ', '-')

    if db.query(Article).filter(Article.title == schema.title).filter(Article.title != article.title).first():
        raise HTTPException(400, detail='Article already exists')
   
    article.title = schema.title
    article.description = schema.description
    article.img_url = schema.img_url
    article.content = schema.content

    db.commit()
    db.refresh(article)

    return article


@router.delete('/{id}/delete', status_code=204)
async def delete_article(id: str, db: Session = Depends(get_db), user = Depends(get_user)):
    if not user.role == 'admin':
        raise HTTPException(403, detail='Operation not allowed')
    
    article = db.query(Article).get(id)

    if not article:
        raise HTTPException(404, detail='Article not found')
    
    if not article.user_id == user.id or user.role != 'admin':
        raise HTTPException(403, detail='Operation not allowed')
    
    db.delete(article)
    db.commit()
