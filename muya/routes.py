import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from muya.forms import registrationForm, loginForm, accountUpdateForm, postForm
from muya.models import User, Service
from muya import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required







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



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route("/service/<int:service_id>")
def service(service_id):
    service = Service.query.get_or_404(service_id)
    return render_template("service.html", service=service)

@app.route("/new_service",  methods=['GET', 'POST'])
@login_required
def create_service():
    form = postForm()
    if form.validate_on_submit():
        post = Service(title=form.title.data, content=form.description.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your service is created succesfully' , 'success')
        return redirect(url_for('index'))
    return render_template("create_service.html", form=form)






def save_images(form_picture):
    R_HEX = secrets.token_hex(8)
    _, f_ext =os.path.splitext(form_picture.filename)
    PIC_FN = R_HEX + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_images', PIC_FN)
    
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return PIC_FN

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
    profile_image = url_for('static', filename='profile_images/' + current_user.image_file )
    return render_template("account.html", profile_image=profile_image, form=form)



@app.route("/")
def index():
    posts = Service.query.all()
    return render_template("home.html", posts=posts)