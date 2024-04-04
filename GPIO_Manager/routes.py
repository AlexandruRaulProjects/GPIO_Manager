from flask import render_template, flash, redirect, url_for, request
from Flask_GPIO_Manager.GPIO_Manager.forms import RegistrationForm, LoginForm, AddPinForm
from Flask_GPIO_Manager.GPIO_Manager import app, bcrypt
from Flask_GPIO_Manager.GPIO_Manager.model import db, User, Pin
from flask_login import login_user, logout_user, current_user, login_required

logs = [
    {
        'user': 'Batman11111',
        'action': 'enabled Led 17'
    },
    {
        'user': 'Superman',
        'action': 'enabled Led 19'
    }
]
title = "Some random title"


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', title=title)


@app.route('/audit-logs')
def audit():
    return render_template('audit.html', logs=logs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Wrong email or password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='account')


@app.route('/gpio', methods=['GET', 'POST'])
def gpio():
    form = AddPinForm()
    if form.validate_on_submit():
        pin = Pin(name=form.name.data, number=form.number.data, user_id=current_user.id)
        db.session.add(pin)
        db.session.commit()
        flash(f'A pin has been added successfully!', 'success')
        return redirect(url_for('gpio'))
    pins = Pin.query.filter_by(user_id=current_user.id).all()
    return render_template('gpio.html', title='gpio', form=form, pins=pins)
