from sqlalchemy import Column, String, Integer, TIMESTAMP, TEXT, ForeignKey, func, Table
from sqlalchemy.orm import relationship
from db.base import Base


association_table = Table(
    'article_category_association',
    Base.metadata,
    Column('article_id', String(255), ForeignKey('articles.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


class Article(Base):
    __tablename__ = 'articles'

    id = Column(String(255), primary_key=True, nullable=False)
    user_id = Column(String(255), ForeignKey('users.id' ))
    img_url = Column(String(1000), nullable=False)
    title = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(String(1000))
    content = Column(TEXT, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    categories = relationship('Category', secondary=association_table, backref='article')
    comments = relationship('Comment', backref='article', cascade='all, delete-orphan')
    votes = relationship('Vote', backref='article', cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Article id={self.id} title={self.title} />"
