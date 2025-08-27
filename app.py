from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import random

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_ClbJig3do5Vj@ep-frosty-surf-ab59znp9-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class MovieBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    dima_rate = db.Column(db.Integer, default=0)
    deni_rate = db.Column(db.Integer, default=0)
    yura_rate = db.Column(db.Integer, default=0)
    ihor_rate = db.Column(db.Integer, default=0)
    date_created = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

class MovieToWatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    next_movie = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        next_movie = request.form['next_movie']
        new_movie = MovieToWatch(next_movie=next_movie)

        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/')
        except:
            return 'Помилка: не вдалось додати фiльм.'

    else:
        moviesToWatch = MovieToWatch.query.order_by(MovieToWatch.id.desc()).all()
        return render_template('add.html', movies=moviesToWatch)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        
        movie_content = request.form['content']
        movie_dima_rate = request.form['dima_rate']
        movie_deni_rate = request.form['deni_rate']
        movie_yura_rate = request.form['yura_rate']
        movie_ihor_rate = request.form['ihor_rate']
        movie_date_created = request.form['date_created']

        if movie_content == '':
            return 'Помилка: заголовок не повинен бути порожнiм.'
        
        if movie_dima_rate == "":
            movie_dima_rate = '0'
        if int(movie_dima_rate) > 11:
            movie_dima_rate = '10'
        if int(movie_dima_rate) < 0:
            movie_dima_rate = '0'
            
        if movie_deni_rate == "":
            movie_deni_rate = '0'
        if int(movie_deni_rate) > 11:
            movie_deni_rate = '10'
        if int(movie_deni_rate) < 0:
            movie_deni_rate = '0'

        if movie_yura_rate == "":
            movie_yura_rate = '0'
        if int(movie_yura_rate) > 11:
            movie_yura_rate = '10'
        if int(movie_yura_rate) < 0:
            movie_yura_rate = '0'

        if movie_ihor_rate == "":
            movie_ihor_rate = '0'
        if int(movie_ihor_rate) > 11:
            movie_ihor_rate = '10'
        if int(movie_ihor_rate) < 0:
            movie_ihor_rate = '0'
        
        new_movie = MovieBase(content=movie_content, dima_rate=movie_dima_rate, deni_rate=movie_deni_rate, yura_rate=movie_yura_rate, ihor_rate=movie_ihor_rate, date_created=movie_date_created)

        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/')
        except:
            return 'Помилка: не вдалось додати фiльм.'

    else:
        movies = MovieBase.query.order_by(MovieBase.id.desc()).all()
        moviesToWatch = MovieToWatch.query.order_by(MovieToWatch.id.desc()).all()

        return render_template('index.html', movies=movies, moviesToWatch=moviesToWatch)

@app.route('/delete/<int:id>')
def delete(id):
    movie_to_delete = MovieBase.query.get_or_404(id)

    try:
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Помилка: не вдалось видалити.'

@app.route('/deleteMovie/<int:id>')
def deleteMovie(id):
    movie_to_delete = MovieToWatch.query.get_or_404(id)

    try:
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Помилка: не вдалось видалити.'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    movie = MovieBase.query.get_or_404(id)

    if request.method == 'POST':
        movie.content = request.form['content']
        movie.dima_rate = request.form['dima_rate']
        movie.deni_rate = request.form['deni_rate']
        movie.yura_rate = request.form['yura_rate']
        movie.ihor_rate = request.form['ihor_rate']
        movie.date_created = request.form['date_created']

        if movie.content == '':
            return 'Помилка: заголовок не повинен бути порожнiм.'
        
        if movie.dima_rate == "":
            movie.dima_rate = '0'
        if int(movie.dima_rate) > 11:
            movie.dima_rate = '10'
        if int(movie.dima_rate) < 0:
            movie.dima_rate = '0'
            
        if movie.deni_rate == "":
            movie.deni_rate = '0'
        if int(movie.deni_rate) > 11:
            movie.deni_rate = '10'
        if int(movie.deni_rate) < 0:
            movie.deni_rate = '0'

        if movie.yura_rate == "":
            movie.yura_rate = '0'
        if int(movie.yura_rate) > 11:
            movie.yura_rate = '10'
        if int(movie.yura_rate) < 0:
            movie.yura_rate = '0'

        if movie.ihor_rate == "":
            movie.ihor_rate = '0'
        if int(movie.ihor_rate) > 11:
            movie.ihor_rate = '10'
        if int(movie.ihor_rate) < 0:
            movie.ihor_rate = '0'

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Помилка: не вдалось оновити.'

    else:
        return render_template('update.html', movie=movie)

@app.route('/random')
def randomMovie():
    moviesToWatch = MovieToWatch.query.order_by(MovieToWatch.date_created.desc()).all()
    if len(moviesToWatch) > 0:
        movie = random.choice(moviesToWatch)
        return render_template('random.html', movie=movie)
    else:
        return 'Список фільмів для вибору порожній'

if __name__ == "__main__":
    app.run(debug=True)

with app.app_context():
    db.create_all()