from flask import render_template, flash, redirect, url_for, request, session
from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm, PasswordResetRequestForm, PasswordResetForm
from app.auth.utils import confirm_email, reset_password_email
from app import db
from app.models import User, UserDetail
import uuid
from flask_login import login_user, logout_user, login_required, current_user

@auth.before_request
def before_request():
    pass

@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    ''' check if user is loggedin already '''
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):

            login_user(user, remember=True)
            db.session.commit()

            next = request.args.get('next')
            if next is None:
                next = url_for('main.home')
            
            return redirect(next)

        flash('Invalid username or password ', 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    
    ''' check if user is logged in '''
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegisterForm()
    if form.validate_on_submit():
        unique_id = uuid.uuid4().int & (1<<29)-1
        user = User(username=form.username.data, 
            uuid = unique_id,
            email=form.email.data)
        details = UserDetail(user_uuid=unique_id,
            login_type=1) 
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.add(details)
        db.session.commit()

        newuser = User.query.filter_by(uuid = unique_id).first()
        login_user(newuser, remember=True)

        token = newuser.generate_confirmation_token()
        confirm_email(user=newuser, token=token)
    
        next = url_for('main.home')
            
        return redirect(next)
        
    return render_template('register.html', form=form)

@auth.route('/password_reset_request', methods=['POST', 'GET'])
def password_reset_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            reset_password_email(user=user, token=token)
        flash('Instruction with password reset has been sent to you', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('account/password_reset_request.html', form=form)

@auth.route('/reset-password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            flash('Password changed. Use it to login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.home'))

    return render_template('account/reset_password.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):

    if current_user.confirm(token):
        db.session.commit()
    else:
        flash('Confirmation email invalid or expired', 'info')
    return redirect(url_for('main.home'))


@auth.route('/resend_confirmation')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token() #generates a unique token.
    send_email(user=current_user, token=token)
    flash('Email successfully resent.', 'warning')
    return redirect(url_for('auth.confirm_account'))