from app.models import db, Book, book_schema
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

book_api = Blueprint("book", __name__, url_prefix="/books")

# "id": 4,
# "author_id": 2,
# "title": "IT",
# "cover_image": "",
# "pages": 500,
# "releaseDate": "2017",
# "isbn": "yu098"


class AlreadyExist(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code


@book_api.errorhandler(AlreadyExist)
def handle_error(e):
    return {"message": e.message, "error": "data already exist"}, e.code


@book_api.route("/new-book", methods=["POST"])
def new_book():
    authur_id = request.json.get("authur_id")
    if authur_id:
        match_authur = Book.query.filter(authur_id == authur_id)
        if match_authur:
            raise AlreadyExist()
    title = request.json.get("title")
    cover_page = request.json.get("cover_page")
    pages = request.json.get("pages")
    releasedate = request.json.get("releasedate")
    isbn = request.json.get("isbn")
    try:
        book = Book(
            authur_id=authur_id,
            title=title,
            cover_image=cover_page,
            pages=pages,
            releasedate=releasedate,
            isbn=isbn,
        )
        db.session.commit()
    except IntegrityError as e:
        return {"success": False, "error": "Some error in sqlalchemy"}
    return {
        "success": True,
        "message": "data added successfully",
        "data": book_schema.dump(book),
    }
