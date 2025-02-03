from datetime import datetime
from flask import abort, session, jsonify, render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
#from utils.time_ago import timeAgo
from web.models import db, User, Notification

from web.utils import save_image, email, time_ago, ip_adrs
from web.auth.forms import (SignupForm, SigninForm, UpdateMeForm, ForgotForm, ResetForm)
from web.extensions import csrf, bcrypt

auth_bp = Blueprint('auth_api', __name__)

#oauth implimentations
import secrets, requests
from urllib.parse import urlencode
from web.utils.providers import oauth2providers
# This route initializes authentication
@auth_bp.route('/authorize/<provider>')
def oauth2_authorize(provider):

    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))

    provider_data = oauth2providers.get(provider)

    if provider_data is None:
        abort(404)

    # Generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # Create a query string with all the required OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('auth_api.oauth2_callback', provider=provider, _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),  # Scope: info or data you want, e.g., email, photo, etc.
        'state': session['oauth2_state'],
    })

    # Redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['authorize_url'] + '?' + qs)


@auth_bp.route('/callback/<provider>')
# @db_session_management
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))

    provider_data = oauth2providers.get(provider)
    if provider_data is None:
        abort(404)

    # if there was an authentication error, flash the error messages and exit
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                print(f'{k}: {v}')
        return redirect(url_for('main.index'))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    # make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('auth_api.oauth2_callback', provider=provider, _external=True),
        }, 
    
    headers={'Accept': 'application/json'})

    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    # use the access token to get the user's email address
    response = requests.get(
        provider_data['userinfo']['url'], 
        headers={'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })

    if response.status_code != 200:
        abort(401)
        
    email = provider_data['userinfo']['email'](response.json())

    # find or create the user in the database
    user = db.session.scalar(db.select(User).where(User.email == email))
    if user is None:
        user = User(email=email, username=email.split('@')[0], src=provider)
        user.set_password(secrets.token_urlsafe(5))
        db.session.add(user)
        db.session.commit()
        #//flush & refresh to get pdated user_id
        db.session.flush()
        db.session.refresh(user)
    # log the user in
    login_user(user)
    # Emit the signal when a user is authenticated
    #user_authenticated.send(current_app._get_current_object(), user_id=user.id, socket_id=request.sid)

    return redirect(url_for('main.index'))

@auth_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,  ip =ip_adrs.user_ip())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        email.confirm_email(user) if user else flash('Undefined User.', 'info')
        flash('Your Account Has Been Created! You Are Now Able To Log In', 'success')
        return redirect(url_for('auth_api.signin'))
    return render_template('auth/signup.html', title='Sign-up', form=form)

""" ======================================================================================== """
import sqlalchemy as sa, traceback
from jsonschema import validate, ValidationError

#oauth implimentations
auth_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "remember": {"type": "boolean"}
    },
    "required": ["username", "password"]
}

signup_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "phone": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["username", "email", "password"]
}

update_user_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "number"},
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string"},
        "withdrawal_password": {"type": "string"},
        "phone": {"type": "string"},
        "name": {"type": "string"},
        "gender": {"type": "string"},
        "membership": {"type": "string"},
        "balance": {"type": "number"},
        "about": {"type": "string"},
        "verified": {"type": "boolean"},
        "ip": {"type": "string"},
        "image": {"type": ["string", "null"]}
    },
    "required": ["username", "email", "password"]
}

import re

# Define regular expressions for validation
USERNAME_REGEX = r'^[A-Za-z0-9_]+$'  # Alphanumeric characters and underscores only
PHONE_REGEX = r'^\+?1?\d{9,15}$'  # International format, e.g., +1234567890 or 10-15 digits
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'  # Basic email format

@auth_bp.route("/user", methods=['POST'])
@csrf.exempt
def create_user():
    
    if current_user.is_authenticated:
        return jsonify({"success": False, "message": "Already authenticated", "redirect": url_for('main.index')})

    if request.content_type != 'application/json':
        return jsonify({"success": False, "message": "Content-Type must be application/json"})

    data = request.get_json()

    # Validate the data against the schema
    try:
        validate(instance=data, schema=signup_schema)
    except ValidationError as e:
        return jsonify({"success": False, "error": e.message})

    # Ensure that no fields are empty
    if not all(data.get(key) for key in ('username', 'email', 'password', 'phone')):
        return jsonify({"success": False, "error": "Required field is empty"})

    # Perform additional validations

    # Validate username (no spaces or special characters)
    if not re.match(USERNAME_REGEX, data['username']):
        return jsonify({"success": False, "error": "Invalid username. Only alphanumeric characters and underscores are allowed."})

    # Validate email
    if not re.match(EMAIL_REGEX, data['email']):
        return jsonify({"success": False, "error": "Invalid email format."})

    # Validate phone number
    if not re.match(PHONE_REGEX, data['phone']):
        return jsonify({"success": False, "error": "Invalid phone number format. Please provide a valid phone number."})

    # Check for existing user with the same username, email, or phone number
    if db.session.scalar(sa.select(User).where(User.username == data['username'])):
        return jsonify({"success": False, "error": "That username is taken. Please use a different username."})

    if db.session.scalar(sa.select(User).where(User.email == data['email'])):
        return jsonify({"success": False, "error": "That email is used. Please use a different email address."})

    if db.session.scalar(sa.select(User).where(User.phone == data['phone'])):
        return jsonify({"success": False, "error": "That phone number is used. Please use a different phone number."})

    try:
        # Create and save the new user
        user = User(
            username=data['username'],
            email=data['email'],
            phone=data['phone'],
            ip=ip_adrs.user_ip()
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()

        # Send confirmation email
        # Generate confirmation token
        # token = user.make_token(token_type="verify_email")
        # Send confirmation email with both token and email
        # confirm_url = url_for('user_api.process_token', token=token, email=user.email, _external=True)
        # email.verify_email(user, confirm_url)
        email.verify_email(user)

        return jsonify({"success": True, "message": "Registration Successful", "redirect": url_for('auth_api.signin')})

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)})

@auth_bp.route("/auth", methods=['POST'])
@csrf.exempt
def auth():
    try:

        if  current_user.is_authenticated:
            return jsonify({"success": False, "error": "Already authenticated", "redirect": url_for('main.index')})

        # Check if the request content type is application/json
        if request.content_type != 'application/json':
            return jsonify({"success": False, "error": "Content-Type must be application/json"})

        # Parse JSON data from the request
        data = request.get_json()
        
        # Ensure that no fields are empty
        if not all(data.get(key) for key in ('username', 'password')):
            # print(data)
            return jsonify({"success": False, "error": f"All fields are required and must not be empty."})

        # Validate the data against the schema
        try:
            validate(instance=data, schema=auth_schema)
        except ValidationError as e:
            return jsonify({"success": False, "error": e})

        # Authentication logic
        user = User.query.filter(
            sa.or_(
                User.email == data['username'],
                User.phone == data['username'],
                User.username == data['username']
            )
        ).first()

        if user and bcrypt.check_password_hash(user.password, data['password']):
            if user.password.startswith("$2b$"):  # bcrypt hash prefix
                user.set_password(data['password'])
                db.session.commit()

            user.online = True
            user.last_seen = datetime.utcnow()
            user.ip = ip_adrs.user_ip()
            db.session.commit()
            login_user(user, remember=data.get('remember', False))
            return jsonify({"success": True, "message": "Authentication Successful", "redirect": url_for('main.index')})
        else:
            return jsonify({"success": False, "error": "Invalid Authentication"})

    except Exception as e:
        print(traceback.print_exc())
        return jsonify({'success': False, 'error': str(e)})

@auth_bp.route("/signin_0", methods=['GET', 'POST'])
def signin_0():
    # form = SigninForm()
    return render_template('auth/signin_0.html')

""" ==================================================================== """

@auth_bp.route("/signin", methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
        # if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Re-hash using scrypt if the password was hashed with bcrypt
            if user.password.startswith("$2b$"):  # bcrypt hash prefix
                user.set_password(form.password.data)
                db.session.commit()
            login_user(user, remember=form.remember.data)
            current_user.online = True
            current_user.last_seen = datetime.utcnow()
            current_user.ip = ip_adrs.user_ip()
            current_user.notify(f'unread', f'Recent Signin -> {time_ago.timeAgo(current_user.last_seen)}')
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.user'))
        else:
            flash('Invalid Login Details. Try Again', 'danger')
    return render_template('auth/signin.html', title='Sign In', form=form)

@auth_bp.route("/signout")
@login_required
def signout():
    current_user.online = False
    logout_user()
    db.session.commit()
    return redirect(url_for('main.index'))

@auth_bp.route("/<string:username>/update", methods=['GET', 'POST'])
@login_required
def update(username):
    user = User.query.filter_by(username=username).first_or_404()
    if ( (current_user.is_admin()) | (current_user.username == user.username) ):
        form = UpdateMeForm()
        if form.validate_on_submit(): 
            #user.photo = save_image.save_photo(form.photo.data) if form.photo.data else current_user.photo or 'default.svg'
            user.image = save_image.save_photo(form.image.data) or current_user.image or 'default.webp'
            user.name = form.name.data
            user.username = form.username.data
            user.email = form.email.data
            user.phone = form.phone.data
            user.gender = form.gender.data
            user.lang = form.lang.data
            user.city = form.city.data
            user.about = form.about.data
            user.duration = form.time.data or 0
            #user.socials = form.socials.data
            db.session.commit()
            flash('Your Account Has Been Updated!', 'success')
            return redirect(url_for('main.user'))
            
        elif request.method == 'GET':
            form.image.data = user.image
            form.name.data = user.name
            form.username.data = user.username
            form.email.data = user.email
            form.phone.data = user.phone
            form.gender.data = user.gender
            form.lang.data = user.lang
            form.city.data = user.city
            form.about.data = user.about
            form.time.data = user.duration or 0 #default
            #form.socials.data = user.socials
        return render_template('auth/update.html', photo=user.image, form=form)
    return redirect(url_for('auth_api.update', username=current_user.username))

@auth_bp.route("/forgot", methods=['GET', 'POST'])
def forgot():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ForgotForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        email.reset_email(user) if user else  None
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth_api.signin'))
    elif request.method == 'GET':
        form.email.data = request.args.get('e')
    return render_template('auth/forgot.html', form=form)

#->for unverified-users, notice use of 'POST' instead of 'post' before it works
@auth_bp.route("/unverified", methods=['post', 'get'])     
@login_required
def unverified():
    if request.method == 'POST':
        email.confirm_email(current_user)
        flash('Verication Emails Sent Again, Check You Mail Box', 'info')
    return render_template('auth/unverified.html')

#->for both verify/reset/forgot etc tokens
@auth_bp.route("/verify-email/<token>/<email>", methods=['GET', 'POST'])
def verify_email(token: str, email: str):

    if current_user.is_authenticated:
        # return redirect(url_for('main.index'))
        pass
    
    # Ensure token_type is present
    if not token or not email:
        print('<token & email> not found', 'warning')
        return redirect(url_for('main.index'))
    
    user = User.query.filter_by(email=email).first()
    # print(user)
    
    if not user:
        flash('User not found', 'warning')
        return redirect(url_for('main.index'))
    
    user = User.check_token(user, token)
    # print(user)
    # print(f"user.token_type2 = ", user.token_type)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('main.index'))

    # Ensure token_type is present
    if not hasattr(user, 'token_type'):
        flash('Token type not found', 'warning')
        print('Token type not found', 'warning')
        # return redirect(url_for('main.index'))
        return f"{user}"
    print(f"user.token_type = ", user.token_type)
    if user.token_type == 'verify_email':
        if user.verified:
            flash(f'You have already verified your email address, {user.username}.', 'success')
        else:
            user.verified = True
            db.session.commit()
            flash(f'Email address confirmed for {user.username}.', 'success')
        return redirect(url_for('auth_api.signin'))
    
    elif user.token_type == 'reset_password':
        form = ResetForm()
        print(f"form.password.data=", form.password.data)
        if form.validate_on_submit():
            try:
                new_password = form.password.data
                user.set_password(new_password)
                db.session.commit()
                flash('Your password has been updated!', 'success')
                return redirect(url_for('auth_api.signin'))
            except ValueError as e:
                flash(str(e), 'danger')

            print(f"user.password =", user.password)
            return redirect(url_for('auth_api.signin'))
        
        return render_template('auth/reset_password.html', form=form, user=user)
    
    return redirect(url_for('main.index'))

#->for both verify/reset/forgot etc tokens
@auth_bp.route("/confirm/<token>/<email>", methods=['GET', 'POST'])
def confirm(token: str, email: str):

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Ensure token_type is present
    if not token or not email:
        print('<token & email> not found', 'warning')
        return redirect(url_for('main.index'))
    
    user = User.query.filter_by(email=email).first()
    print(user)
    
    if not user:
        flash('User not found', 'warning')
        return redirect(url_for('main.index'))
    
    user = User.check_token(user, token)
    print(user)
    # print(f"user.token_type2 = ", user.token_type)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('main.index'))

    # Ensure token_type is present
    if not hasattr(user, 'token_type'):
        flash('Token type not found', 'warning')
        print('Token type not found', 'warning')
        # return redirect(url_for('main.index'))
        return f"{user}"
    print(f"user.token_type = ", user.token_type)
    if user.token_type == 'confirm_email':
        if user.verified:
            flash(f'You have already verified your email address, {user.username}.', 'success')
        else:
            user.verified = True
            db.session.commit()
            flash(f'Email address confirmed for {user.username}.', 'success')
        return redirect(url_for('auth_api.signin'))
    
    elif user.token_type == 'reset_password':
        form = ResetForm()
        print(f"form.password.data=", form.password.data)
        if form.validate_on_submit():
            try:
                new_password = form.password.data
                user.set_password(new_password)
                db.session.commit()
                flash('Your password has been updated!', 'success')
                return redirect(url_for('auth_api.signin'))
            except ValueError as e:
                flash(str(e), 'danger')

            print(f"user.password =", user.password)
            return redirect(url_for('auth_api.signin'))
        
        return render_template('auth/reset_password.html', form=form, user=user)
    
    return redirect(url_for('main.index'))

@auth_bp.route('/notify')
@login_required
def notify():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(Notification.created > since).order_by(Notification.created.asc())
    return jsonify([{ 'name': n.name, 'data': n.get_data(), 'timestamp': n.created } for n in notifications])

