from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskblog.users.forms import (
    RegistrationForm, 
    LoginForm, 
    UpdateUserForm,
    RequestResetForm, 
    ResetPasswordForm
)
from flaskblog.models import User, Post
from flaskblog import bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_image, send_reset_email

users = Blueprint('users', __name__)



@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already logged in.', 'success')
        return redirect(url_for('main.home'))

    users = User.query.all()

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created successfully.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Registration Page', form=form, users=users)



@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'You are already logged in.', 'success')
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You have been logged in successfully.', 'success')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))

            # Ternary Condition for example
            #return redirect(next_page) if next_page else redirect(url_for('home'))
                
        else:
            flash(f'Login unsuccessfull. Please check your email and password again.', 'danger')
    return render_template('login.html', title='Login Page', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route("/my_account", methods=['GET', 'POST'])
@login_required
def my_account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            profile_picture = save_image(form.picture.data)
            current_user.profile_image = profile_picture
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated successfully', 'success')
        return redirect(url_for('users.my_account'))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='My Account page', form=form)



@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_created.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)



@users.route("/reset_request", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        flash(f'You are already logged in.', 'success')
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to your mail.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)



@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        flash(f'You are already logged in.', 'success')
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('The token is invalid or expired.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash(f'Your password has been updated.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)