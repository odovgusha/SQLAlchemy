import random
from datetime import date
from app import app
from data_models import db, Author, Book


BOOKS_DATA = {
    "Charles Dickens": [
        ("Great Expectations", "9780141439563"),
        ("Oliver Twist", "9780141439747"),
        ("David Copperfield", "9780140439441"),
        ("A Tale of Two Cities", "9780141439600"),
        ("Bleak House", "9780141439723"),
    ],
    "Jane Austen": [
        ("Pride and Prejudice", "9780141439518"),
        ("Sense and Sensibility", "9780141439662"),
        ("Emma", "9780141439587"),
        ("Mansfield Park", "9780141439808"),
        ("Persuasion", "9780141439686"),
    ],
    "George Orwell": [
        ("1984", "9780451524935"),
        ("Animal Farm", "9780451526342"),
        ("Homage to Catalonia", "9780156421171"),
        ("Burmese Days", "9780140187419"),
        ("Coming Up for Air", "9780156196253"),
    ],
    "Mark Twain": [
        ("Adventures of Huckleberry Finn", "9780143107323"),
        ("The Adventures of Tom Sawyer", "9780143039563"),
        ("A Connecticut Yankee in King Arthur's Court", "9780140430646"),
        ("The Prince and the Pauper", "9780140436693"),
        ("Life on the Mississippi", "9780143105954"),
    ],
    "Virginia Woolf": [
        ("Mrs Dalloway", "9780156628709"),
        ("To the Lighthouse", "9780156907392"),
        ("Orlando", "9780156701600"),
        ("The Waves", "9780156949606"),
        ("A Room of One’s Own", "9780156787338"),
    ],
    "Leo Tolstoy": [
        ("War and Peace", "9780199232765"),
        ("Anna Karenina", "9780143035008"),
        ("The Death of Ivan Ilyich", "9780140447934"),
        ("Resurrection", "9780140444612"),
        ("Childhood, Boyhood, Youth", "9780140440492"),
    ],
    "Fyodor Dostoevsky": [
        ("Crime and Punishment", "9780140449136"),
        ("The Brothers Karamazov", "9780140449242"),
        ("The Idiot", "9780140447927"),
        ("Notes from Underground", "9780140444148"),
        ("Demons", "9780141441412"),
    ],
    "Ernest Hemingway": [
        ("The Old Man and the Sea", "9780684801223"),
        ("A Farewell to Arms", "9780684801469"),
        ("For Whom the Bell Tolls", "9780684803357"),
        ("The Sun Also Rises", "9780743297332"),
        ("The Snows of Kilimanjaro", "9780684803340"),
    ],
    "Franz Kafka": [
        ("The Metamorphosis", "9780553213690"),
        ("The Trial", "9780805210408"),
        ("The Castle", "9780805211061"),
        ("Amerika", "9780805210644"),
        ("Letters to Milena", "9780805211818"),
    ],
    "Haruki Murakami": [
        ("Norwegian Wood", "9780375704024"),
        ("Kafka on the Shore", "9781400079278"),
        ("1Q84", "9780307593313"),
        ("The Wind-Up Bird Chronicle", "9780679775430"),
        ("Sputnik Sweetheart", "9780375704062"),
    ],
    "J.K. Rowling": [
        ("Harry Potter and the Sorcerer's Stone", "9780545582889"),
        ("Harry Potter and the Chamber of Secrets", "9780439064873"),
        ("Harry Potter and the Prisoner of Azkaban", "9780439136365"),
        ("Harry Potter and the Goblet of Fire", "9780439139601"),
        ("Harry Potter and the Order of the Phoenix", "9780439358071"),
    ],
    "J.R.R. Tolkien": [
        ("The Hobbit", "9780547928227"),
        ("The Fellowship of the Ring", "9780547928210"),
        ("The Two Towers", "9780547928203"),
        ("The Return of the King", "9780547928197"),
        ("The Silmarillion", "9780618391110"),
    ],
    "Agatha Christie": [
        ("Murder on the Orient Express", "9780062693662"),
        ("And Then There Were None", "9780062073488"),
        ("The Murder of Roger Ackroyd", "9780062073563"),
        ("Death on the Nile", "9780062073556"),
        ("The ABC Murders", "9780062073694"),
    ],
    "Isaac Asimov": [
        ("Foundation", "9780553293357"),
        ("Foundation and Empire", "9780553293371"),
        ("Second Foundation", "9780553293364"),
        ("I, Robot", "9780553294385"),
        ("The Caves of Steel", "9780553293401"),
    ],
    "Arthur C. Clarke": [
        ("2001: A Space Odyssey", "9780451457998"),
        ("Childhood's End", "9780345347954"),
        ("Rendezvous with Rama", "9780553287899"),
        ("The City and the Stars", "9780156306300"),
        ("The Fountains of Paradise", "9780156027328"),
    ],
    "Stephen King": [
        ("The Shining", "9780307743657"),
        ("It", "9781501142970"),
        ("Misery", "9780450417399"),
        ("Carrie", "9780307743664"),
        ("Pet Sematary", "9781501156700"),
    ],
    "Ursula K. Le Guin": [
        ("A Wizard of Earthsea", "9780547773742"),
        ("The Left Hand of Darkness", "9780441478125"),
        ("The Dispossessed", "9780060512750"),
        ("The Tombs of Atuan", "9780689845369"),
        ("Tehanu", "9780689845376"),
    ],
    "Margaret Atwood": [
        ("The Handmaid's Tale", "9780385490818"),
        ("Oryx and Crake", "9780385721677"),
        ("The Blind Assassin", "9780385720953"),
        ("Alias Grace", "9780385490443"),
        ("The Testaments", "9780385543781"),
    ],
    "Neil Gaiman": [
        ("American Gods", "9780062572233"),
        ("Coraline", "9780380807345"),
        ("Good Omens", "9780060853983"),
        ("Neverwhere", "9780060557812"),
        ("The Graveyard Book", "9780060530921"),
    ],
    "Albert Camus": [
        ("The Stranger", "9780679720201"),
        ("The Plague", "9780679720218"),
        ("The Fall", "9780679732563"),
        ("The Myth of Sisyphus", "9780679733737"),
        ("Exile and the Kingdom", "9780679733843"),
    ],
}


with app.app_context():

    if Author.query.first():
        print("Database already seeded. Exiting.")
        exit()

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

    authors = {}
    for name, born, died in authors_data:
        author = Author(name=name, birth_date=born, date_of_death=died)
        db.session.add(author)
        authors[name] = author

    db.session.commit()
    print("20 authors added.")

    seen_isbns = set()
    books = []

    for author_name, books_list in BOOKS_DATA.items():
        author = authors[author_name]
        for title, isbn in books_list:
            if isbn in seen_isbns:
                continue
            seen_isbns.add(isbn)
            books.append(Book(
                title=title,
                isbn=isbn,
                publication_year=random.randint(1850, 2022),
                author_id=author.id
            ))

    db.session.add_all(books)
    db.session.commit()
    print(f"{len(books)} unique books added.")
