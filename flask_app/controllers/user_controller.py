from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user_model

@app.route('/')
def main_page():
    return render_template('register_login.html')

@app.route('/register', methods=['post'])
def registration_check():
    # check if info in form is valid
    if not user_model.Users.registration_check(request.form):
        return redirect('/')
    id = user_model.Users.save(request.form)
    session['id'] = id
    return redirect('/dashboard')

@app.route('/login', methods=['post'])
def login_check():
    if not user_model.Users.login_check(request.form):
        return redirect('/')
    id = user_model.Users.get_one_email(request.form).id
    session['id'] = id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')