from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from data_models import db, Author, Book
import os




app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"



db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():

    query = request.args.get("q", "")
    sort = request.args.get("sort", "title")

    books_query = Book.query.join(Author)

    if query:
        books_query = books_query.filter(
            db.or_(
                Book.title.ilike(f"%{query}%"),
                Author.name.ilike(f"%{query}%")
            )
        )

    books = books_query.order_by(Author.name).all() if sort=="author" else books_query.order_by(Book.title).all()

    return render_template("home.html", books=books)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        name = request.form.get("name")
        birthdate = datetime.strptime(request.form.get("birthdate"), "%Y-%m-%d").date()
        date_of_death = request.form.get("date_of_death")
        date_of_death = datetime.strptime(date_of_death, "%Y-%m-%d").date() if date_of_death else None

        author = Author(name=name, birth_date=birthdate, date_of_death=date_of_death)
        db.session.add(author)
        db.session.commit()

        return redirect(url_for("add_author"))

    return render_template("add_author.html")

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    authors = Author.query.order_by(Author.name).all()

    if request.method == "POST":
        title = request.form.get("title")
        isbn = request.form.get("isbn")
        publication_year = int(request.form.get("publication_year"))
        author_id = int(request.form.get("author_id"))

        book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
        db.session.add(book)
        db.session.commit()

        return redirect(url_for("add_book"))

    return render_template("add_book.html", authors=authors)

# ---------------- Delete Book ----------------
@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)
    db.session.commit()

    if not author.books:
        db.session.delete(author)
        db.session.commit()

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
