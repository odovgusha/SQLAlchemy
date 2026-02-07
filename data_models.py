from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)  # primary key
    name = db.Column(db.String(100), nullable=False, unique=True)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)  # Optional

    books = db.relationship("Book", backref="author", lazy=True)

    def __repr__(self):
        return f"<Author id={self.id} name='{self.name}'>"

    def __str__(self):
        lifespan = (
            f"{self.birth_date} – {self.date_of_death}"
            if self.date_of_death else f"born {self.birth_date}"
        )
        return f"{self.name} ({lifespan})"


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    #Foreign Key
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)

    def __repr__(self):
        return f"<Book id={self.id} title='{self.title}'>"

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
