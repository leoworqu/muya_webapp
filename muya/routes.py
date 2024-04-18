import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from muya.forms import registrationForm, loginForm, accountUpdateForm, postForm, reviewForm
from muya.models import User, Service, Review
from muya import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required



# Function to save profile images
def save_images(form_picture):
    R_HEX = secrets.token_hex(8)  # Generate a random hex string
    _, f_ext =os.path.splitext(form_picture.filename)  # Extract file extension
    PIC_FN = R_HEX + f_ext  # Combine random hex and file extension to form filename
    picture_path = os.path.join(app.root_path, 'static/profile_images', PIC_FN)  # Define picture path
    
    output_size = (200, 200)  # Set output size for profile image
    i = Image.open(form_picture)  # Open the uploaded image
    i.thumbnail(output_size)  # Resize image
    i.save(picture_path)  # Save resized image

    return PIC_FN  # Return the filename

# Function to save service images
def save_image(form_picture):
    R_HEX = secrets.token_hex(8)  # Generate a random hex string
    _, f_ext =os.path.splitext(form_picture.filename)  # Extract file extension
    PIC_FN = R_HEX + f_ext  # Combine random hex and file extension to form filename
    picture_path = os.path.join(app.root_path, 'static/service_images', PIC_FN)  # Define picture path
    
    output_size = (500, 500)  # Set output size for service image
    i = Image.open(form_picture)  # Open the uploaded image
    i.thumbnail(output_size)  # Resize image
    i.save(picture_path)  # Save resized image

    return PIC_FN  # Return the filename


# Route for user registration
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = registrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Username already exists. Please use a different Username.', 'error')
            return redirect(url_for('register'))
        if existing_email:
            flash('Email address already exists. Please use a different email.', 'error')
            return redirect(url_for('register'))
        db.session.add(user)
        db.session.commit()
        flash(f'Account succesfully created for {form.username.data}, now you can log in!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


# Route for user login
@app.route("/login",  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Loggged in succesfully' , 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Log in attempt Unsuccesfully' , 'error')
            return redirect(url_for('login'))
    return render_template("login.html", form=form)


# Route for user logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


# Route for viewing a service
@app.route("/service/<int:service_id>", methods=['GET', 'POST'])
def service(service_id):
    form = reviewForm()
    service = Service.query.get_or_404(service_id)
    reviews = Review.query.filter_by(service_id=service_id).all()
    user_service = Service.query.filter_by(user_id=service.user_id).all()
    if form.validate_on_submit():
        userid = current_user.id
        post = Review(comment=form.comment.data, service_id=service_id, user_id=userid , like_or_dislike=form.like_or_dislike.data)
        db.session.add(post)
        db.session.commit()
        flash('Your review was posted!' , 'success')
        return redirect(url_for('service' , service_id=service.id))
    service_image = url_for('static', filename='service_images/' + service.image_files )
    return render_template("service.html", service=service,
                           service_image=service_image,
                           form=form, reviews=reviews, user_service=user_service)


# Route for creating a new service
@app.route("/new_service",  methods=['GET', 'POST'])
@login_required
def create_service():
    form = postForm()
    if form.validate_on_submit():
        if form.service_picture.data:
            picture_file = save_image(form.service_picture.data)
            post = Service(title=form.title.data, content=form.description.data, author=current_user, image_files=picture_file)
            db.session.add(post)
            db.session.commit()
            flash('Your service is created success' , 'success')
            return redirect(url_for('index'))
        else:
            post = Service(title=form.title.data, content=form.description.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your service is created succesfully' , 'success')
            return redirect(url_for('index'))
    return render_template("create_service.html", form=form)


# Route for updating a service
@app.route("/service/<int:service_id>/update", methods=['GET', 'POST'])
@login_required
def update_service(service_id):
    service = Service.query.get_or_404(service_id)
    if service.author != current_user:
        abort(403)
    form = postForm()
    if form.validate_on_submit():
        if form.service_picture.data:
            picture_file = save_image(form.service_picture.data)
            service.image_files = picture_file
            service.title = form.title.data
            service.content = form.description.data
        db.session.commit()
        flash('Your service is Updated succesfully' , 'success')
        return redirect(url_for('service', service_id=service.id))
    elif request.method == 'GET':
        form.title.data = service.title
        form.description.data = service.content
    return render_template("updateservice.html", service=service, form=form)


# Route for deleting a service
@app.route("/service/<int:service_id>/delete", methods=['POST'])
@login_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    if service.author != current_user:
        abort(403)
    db.session.delete(service)
    db.session.commit()
    flash('Your service is deleted succesfully' , 'success')
    return redirect(url_for('index'))


# Route for user account page
@app.route("/account",  methods=['GET', 'POST'])
@login_required
def account():
    form = accountUpdateForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_file = save_images(form.profile_picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated succesfully' , 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    user_service = Service.query.filter_by(user_id=current_user.id).all()
    profile_image = url_for('static', filename='profile_images/' + current_user.image_file )
    return render_template("account.html", profile_image=profile_image,
                           form=form, user_service=user_service, reviews=reviews)


# Route for the home page
@app.route("/")
def index():
    posts = Service.query.paginate(per_page=9, page=1)
    return render_template("home.html", posts=posts)
