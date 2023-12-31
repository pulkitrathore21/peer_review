# "id": 4,
# "author_id": 2,
# "title": "IT",
# "cover_image": "",
# "pages": 500,
# "releaseDate": "2017",
# "isbn": "yu098"
#   },
from dataclasses import dataclass
from app import db, ma
from flask_marshmallow import Schema, fields


@dataclass
class Book(db.Model):
    print()
    id: int = db.Column(db.Integer, primary_key=True)
    authur_id: int = db.Column(db.Integer, nullable=True)
    title: str = db.Column(db.TEXT, nullable=True)
    cover_image: str = db.Column(db.TEXT, nullable=True)
    pages: int = db.Column(db.Integer, nullable=True)
    releasedate: str = db.Column(db.TEXT, nullable=True)
    isbn: str = db.Column(db.TEXT, nullable=True)


class BookSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "authur_id",
            "title",
            "cover_image",
            "pages",
            "releasedate",
            "isbn",
        )
        # exclude=[]


book_schema = BookSchema()
books_schema = BookSchema(many=True)
