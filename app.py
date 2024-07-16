from flask import Flask, render_template, request, redirect, url_for
from models import db, Post, User
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()

def generate_random_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if not user:
            user_id = generate_random_id()
            user = User(id=user_id, username=username)
            db.session.add(user)
            db.session.commit()

        post = Post(user_id=user.id, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))

    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if not user:
            user_id = generate_random_id()
            user = User(id=user_id, username=username)
            db.session.add(user)
            db.session.commit()

        post = Post(user_id=user.id, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('post_form.html')

@app.route('/user/<username>/edit', methods=['GET', 'POST'])
def edit_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if request.method == 'POST':
        new_username = request.form['new_username']
        user.username = new_username
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_user.html', user=user)

@app.route('/admin', methods=['GET'])
def admin():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('admin.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)