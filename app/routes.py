from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm, CommentForm
from app.models import User, Post, Comment
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home Page', posts=posts)

# methods override the default for login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # False with GET request, True with POST if also valid
    # add error message later when validation fails
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome to Brightblog ' + form.username.data + '!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    return render_template('post.html', title='Make a Post', form=form)

@app.route('/showpost/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    form = CommentForm()
    post = Post.query.get(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.asc())
    if post is not None:
        if form.validate_on_submit():
            comment = Comment(text=form.comment.data, author=current_user, post_id=post_id)
            comment.save()
            flash('Your comment has been posted!')
            return redirect(url_for('show_post', post_id=post.id))
        return render_template('showpost.html', title=post.title, form=form, post=post, comments=comments)
    else:
        return render_template('404.html', title='Page not found.')