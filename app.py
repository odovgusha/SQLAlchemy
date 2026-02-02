from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

from data_models import db, Author, Book

import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)


@app.route('/add_author', methods=['GET','POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birthday = request.form['birthday']
        date_of_birth = request.form['date_of_birth']

        author = Author(
            name=name,
            birthday=birthday,
            date_of_birth=date_of_birth or None
        )
        db.session.add(author)
        db.session.commit()

        return render_template('add_author.html',success = True)


@app.route('/add_book', methods=['GET','POST'])
def add_book():
    authors = Author.query.all()
    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']

        book = Book(title=title, author_id=author_id)
        db.session.add(book)
        db.session.commit()

        return render_template('add_book.html',success = True)

    return render_template('add_book.html',authors = authors)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)