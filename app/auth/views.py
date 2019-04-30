from .import auth
from flask import render_template,redirect,url_for, flash,request
from ..models import User
from flask_login import login_user,logout_user,login_required
from .forms import LoginForm,RegistrationForm
from ..import db
from ..email import mail_message


@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)   

            # redirect to the appropriate dashboard page
        return redirect(url_for('main.index'))

    flash('Invalid author or Password')

    title = "Titus's Blog login"
    return render_template('auth/login.html',login_form = login_form,title=title)

@auth.route('/ad_login',methods=['GET','POST'])
def ad_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = ad_login_form.email.data).first()
        if user is not None and user.verify_password(ad_login_form.password.data):
            ad_login_user(user,ad_login_form.remember.data)

            # redirect to the appropriate dashboard page
            if user.is_admin:
                return redirect(url_for('main.admin_dashboard'))
            else:

                return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid author or Password')

    title = "Titus's Blog login"
    return render_template('auth/ad_login.html',login_form = login_form,title=title)

@auth.route('/register',methods = ["GET","POST"])
def register():

    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        user = User(email = registration_form.email.data,author = registration_form.author.data,password = registration_form.password.data)

        db.session.add(user)
        db.session.commit()

        
        return redirect(url_for("auth.login"))
        title = "New Account"

        

    return render_template('auth/register.html',registration_form = registration_form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))