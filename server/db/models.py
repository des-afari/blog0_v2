from db.base import Base, engine
from api.user.model import User
from api.jti.model import JsonTokenId
from api.category.model import Category
from api.article.model import Article, association_table
from api.comment.model import Comment
from api.vote.model import Vote

Base.metadata.create_all(engine)