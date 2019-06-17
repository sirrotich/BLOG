from .import auth
from flask import render_template,redirect,url_for, flash,request
from ..models import User
from flask_login import login_user,logout_user,login_required
from .forms import LoginForm,RegistrationForm,RequestResetForm,ResetPasswordForm
from ..import db
from ..email import mail_message

@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)   
            
        db.session.add(user)
        db.session.commit()
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

        
        flash('you can login')
    return render_template('auth/register.html',registration_form = registration_form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


########RESET PASSWORD###########

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Password', sender='rotichtitus12@gmail.com', recipients=[user.email])
    msg.body = f'''To reset visit the link: 
    {url_for('auth.reset_token', token=token, _external=True)}

    '''

@auth.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if User.is_authenticated:
        return redirect(url_for('main.index'))
        form = RequestResetForm()
        if form.validate_on_submit():
            user = User.query.filter_by(form.email.data).first()
            send_reset_email(user)
            flash('An email as been sent')
            return redirect(url_for('login'))
        return render_template('auth/reset_request.html',reset_request_form=reset_request_form)

@auth.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if login_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Token is invalid or expired', 'warning')
        return redirect(url_for('auth.reset_request'))
        form =  ResetPasswordForm()
        if registration_form.validate_on_submit():
        
        #user.password = hashed_password
            db.session.add(user)
            db.session.commit()
            flash('Your pass has been updated')
            
            return redirect(url_for("auth.login"))
        return render_template('auth/reset_token.html', form=form)