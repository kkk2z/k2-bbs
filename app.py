from flask import Flask, render_template, request, redirect, url_for
from models import db, Post
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

def generate_random_id(password):
    hash_object = generate_password_hash(password, method='sha256')
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        password = request.form['password']
        post_id = generate_random_id(password)

        new_post = Post(id=post_id, name=name, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))

    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        password = request.form['password']
        post_id = generate_random_id(password)

        new_post = Post(id=post_id, name=name, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('post_form.html')

if __name__ == '__main__':
    app.run(debug=True)
