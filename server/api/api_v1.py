from fastapi import APIRouter
from api.user.router import router as user_router
from api.category.router import router as category_router
from api.article.router import router as article_router
from api.comment.router import router as comment_router
from api.vote.router import router as vote_router

api_router = APIRouter()
api_router.include_router(user_router, tags=['user'])
api_router.include_router(category_router, prefix='/category', tags=['category'])
api_router.include_router(article_router, prefix='/article', tags=['article'])
api_router.include_router(comment_router, prefix='/comment', tags=['comment'])
api_router.include_router(vote_router, prefix='/vote', tags=['vote'])