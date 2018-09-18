from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog.posts.forms import CreatePostForm
from flaskblog.models import Post
from flaskblog import db
from flask_login import current_user, login_required 

posts = Blueprint('posts', __name__)



@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content= form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created successfully', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='Add New Post', form=form, legend='Create New Post')



@posts.route("/post/<int:post_id>")
def single_post(post_id):
    post = Post.query.get(post_id)
    return render_template('single_post.html', title=post.title, post=post)



@posts.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = CreatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated successfully', 'success')
        return redirect(url_for('main.home', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')



@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted successfully', 'success')
    return redirect(url_for('main.home'))   
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')