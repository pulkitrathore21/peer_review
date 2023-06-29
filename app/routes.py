from app.models import db, Book, book_schema, books_schema

#
from flask import Blueprint, request, url_for
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert as upsert


book_api = Blueprint("book", __name__, url_prefix="/books")

# "id": 4,
# "author_id": 2,
# "title": "IT",
# "cover_image": "",
# "pages": 500,
# "releaseDate": "2017",
# "isbn": "yu098"


class UserError(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code


@book_api.errorhandler(UserError)
def handle_error(e):
    return {"message": e.message, "error": "authur already exist"}, e.code


class AlreadyExist(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code


@book_api.errorhandler(AlreadyExist)
def handle_error(e):
    return {"message": e.message, "error": "authur already exist"}, e.code


class BookNotFound(Exception):
    def __init__(self, message, code=204):
        self.message = message
        self.code = code


@book_api.errorhandler(BookNotFound)
def handle_error(e):
    return {
        "message": e.message,
    }, e.code


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
        db.session.add(book)
        db.session.commit()
    except IntegrityError as e:
        return {"success": False, "error": "Some error in sqlalchemy"}
    return {
        "success": True,
        "message": "data added successfully",
    }


@book_api.route("/book", methods=["GET"])
@book_api.route("/<int:book_id>", methods=["GET"])
def get_book(book_id=None):
    argue = request.args
    sort = argue.get("sort", "id")
    order = argue.get("order", "asc")
    page_limit = argue.get("page_limit", 1, type=int)
    page_ = argue.get("page", 1, type=int)
    search = argue.get("search")
    search_column = argue.get("search_column")

    int_column = ("id", "authur_id", "pages")
    str_column = ("title", "cover_image", "releasedate", "isbn")

    books = Book.query
    if book_id:
        one_book = books.filter(id == book_id)
        if not one_book:
            raise BookNotFound()
        return {
            "success": True,
            "message": "book find successfuly",
            "book": book_schema.dump(one_book),
        }, 200

    if not sort:
        raise UserError("User not given argument for sort")
    if order:
        order = order.lower()
        if order not in ("asc", "desc"):
            raise UserError("invalid order argument only allowed 'asc','desc'")
    if search:
        if search_column in int_column:
            book = books.filter(getattr(Book, search_column) == search)
        elif search_column in str_column:
            book = books.filter(getattr(Book.search_column).ilike(f"%{search}"))
        else:
            raise UserError("invalid search column")
    book = books.order_by(getattr(getattr(Book, sort), order)())
    book = book.paginate(page=page_, per_page=page_limit, error_out=False)
    records = book.items
    if len(records) == 0:
        raise UserError("Mo records found", 200)

    if book.has_next:
        print(book.has_next)
        next_url = url_for("book.get_book", page=book.next_num)
        print(next_url)
    else:
        next_url = None
    serialized = books_schema.dump(book)

    return {
        "success": True,
        "all_Books": serialized,
        "current_page": book.page,
        "total_page": book.pages,
        "next_page": next_url,
        "total": book.total,
        "order": order,
        "sort": sort,
    }


@book_api.route("/", methods=["PUT"])
@book_api.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id=None):
    if book_id:
        book = request.json
        books[id] = book_id
        books = [book]
    else:
        books = request.json.get("items")
    books_ = []
    for book in books:
        book_id = book.get("id")
        book = Book.query.filter_by(id=book_id).first()
        book = book_schema.dump(book)
        book.update(book)
        books_.append(book)

    try:
        query = upsert(Book).values(books_)
        query = query.on_conflict_do_update(
            index_elements=[Book.id],
            set_=dict(
                authur_id=query.excluded.authur_id,
                title=query.excluded.title,
                cover_image=query.exlude.cover_image,
                pages=query.excluded.pages,
                releasedate=query.excluded.releasedate,
                isbn=query.excluded.isbn,
            ),
        )
        db.session.execute(query)
        db.session.commit()

    except Exception as e:
        return {"error": str(e)}
    return {"success": True, "message": "updated successfully"}, 200


@book_api.route("/", methods=["DELETE"])
@book_api.route("/<int:books_id>", methods=["DELETE"])
def delete_book(books_id=None):
    # print(request.json.get("items"))
    if books_id:
        books_ = (books_id,)

    else:
        books_ = request.json.get("items")
        print(books_)
        for item in books_:
            print(item)
            books = Book.query.filter(Book.id == item).first()
            print(books)
            if books:
                db.session.delete(books)
                db.session.commit()
                return {
                    "success": True,
                    "pokemon": books,
                    "message": f"deleted successfully with{item}",
                }
        else:
            raise UserError("Not deleted", 204)
