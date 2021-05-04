from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'i will encode this later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///net.db'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    content = db.Column(db.Text)

class PostForm(FlaskForm):
    title = StringField('Type in the tile', validators=[DataRequired()])
    subtitle = StringField('Type in the subtitle', validators=[DataRequired()])
    author = StringField('Post author', validators=[DataRequired()])
    content = TextAreaField('Type in your post content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AnotherForm(FlaskForm):
    submit = SubmitField('Click to add post')
    
@app.route('/', methods = ['GET','POST'])
def index():

    addform = AnotherForm()
    if addform.validate_on_submit():
        return redirect(url_for('add'))

    return render_template('index.html', addform=addform)

@app.route('/add', methods = ['GET','POST'])
def add():

    form = PostForm()
    if form.validate_on_submit():
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        author = request.form.get('author')
        content = request.form.get('content')

        new_post = Post(title=title, subtitle=subtitle, author=author, content=content)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('show'))

    return render_template('add.html', form=form)

@app.route('/show', methods = ['GET','POST'])
def show():

    sh_posts = Post.query.all()

    return render_template('show.html',sh_posts=sh_posts)

if __name__ == '__main__':
    app.run(debug=True)