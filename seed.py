import random
from datetime import date
from app import app
from data_models import db, Author, Book

with app.app_context():
    # -------- Check if database already seeded --------
    if Author.query.first():
        print("Database already seeded. Exiting.")
    else:
        # -------- 20 Authors --------
        authors_data = [
            ("Charles Dickens", date(1812, 2, 7), date(1870, 6, 9)),
            ("Jane Austen", date(1775, 12, 16), date(1817, 7, 18)),
            ("George Orwell", date(1903, 6, 25), date(1950, 1, 21)),
            ("Mark Twain", date(1835, 11, 30), date(1910, 4, 21)),
            ("Virginia Woolf", date(1882, 1, 25), date(1941, 3, 28)),
            ("Leo Tolstoy", date(1828, 9, 9), date(1910, 11, 20)),
            ("Fyodor Dostoevsky", date(1821, 11, 11), date(1881, 2, 9)),
            ("Ernest Hemingway", date(1899, 7, 21), date(1961, 7, 2)),
            ("Franz Kafka", date(1883, 7, 3), date(1924, 6, 3)),
            ("Haruki Murakami", date(1949, 1, 12), None),
            ("J.K. Rowling", date(1965, 7, 31), None),
            ("J.R.R. Tolkien", date(1892, 1, 3), date(1973, 9, 2)),
            ("Agatha Christie", date(1890, 9, 15), date(1976, 1, 12)),
            ("Isaac Asimov", date(1920, 1, 2), date(1992, 4, 6)),
            ("Arthur C. Clarke", date(1917, 12, 16), date(2008, 3, 19)),
            ("Stephen King", date(1947, 9, 21), None),
            ("Ursula K. Le Guin", date(1929, 10, 21), date(2018, 1, 22)),
            ("Margaret Atwood", date(1939, 11, 18), None),
            ("Neil Gaiman", date(1960, 11, 10), None),
            ("Albert Camus", date(1913, 11, 7), date(1960, 1, 4)),
        ]

        authors = []
        for name, born, died in authors_data:
            author = Author(
                name=name,
                birth_date=born,
                date_of_death=died
            )
            authors.append(author)

        db.session.add_all(authors)
        db.session.commit()
        print(" 20 authors added.")

        # -------- 100 Books --------
        books = []
        for i in range(1, 101):
            author = random.choice(authors)
            book = Book(
                title=f"Book #{i} by {author.name}",
                isbn=f"9780000000{i:03}",  # unique ISBNs
                publication_year=random.randint(1850, 2022),
                author_id=author.id
            )
            books.append(book)

        db.session.add_all(books)
        db.session.commit()
        print(" 100 books added.")
