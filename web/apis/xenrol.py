import traceback
import jsonschema
from flask import Blueprint, jsonify, request, abort
from web.models import db, User, Enrollment, Course
from web.apis.auth import token_auth
from web.apis.errors import bad_request
from web.utils import notifyer
from web.extensions import db  # Import necessary extensions

xenrol_bp = Blueprint('xenrol_api', __name__)
mandatory_dt = ['name', 'email', 'phone', 'course'] #optional-> comment

def handle_response(message=None, alert=None, data=None):
    """ only success response should have data and be set to True. And  """
    response_data = {
        'message': message,
    }
    if data:
        response_data['alert'] = alert

    if data:
        response_data['data'] = data

    return response_data

_schemas = {
    'save-data': {
        "type": "object",
        "properties": {
            "name": { "type": "string" },
            "email": { "type": "string" },
            "phone": { "type": "string" },
            "course_id": { "type": "integer" },
            "comment": { "type": "string" }
        },

        },
}

@xenrol_bp.route('/x-enrol', methods=['POST'])
#@db_session_management
def save(data=None):
    try:

        if not db.session.is_active:
            db.session.begin()

        """ convert to dict - identify the corresponding schema - validate connected-user - check user existence - save chat - notify connected user(s) """
        #data = json.loads(data) if data is not None else {} #without this, you get str object have no attr .get() cos `data` will be loaded as str
        data = request.get_json()
        #print("Raw request data:", request.get_data())
        event_schema = _schemas.get('save-data')

        jsonschema.validate(instance=data, schema=event_schema)

        data = {
            'name': data.get('name', None),
            'email': data.get('email', None),
            'phone': data.get('phone', None),
            'course_id': data.get('course_id', None),
            'comment': data.get('comment', None),
        }

        # Check for duplicate of phone number/email before insertion
        existing_enrollment = Enrollment.query.filter(
            (Enrollment.phone == data['phone']) | (Enrollment.email == data['email'])
        ).first()

        if existing_enrollment:
            # Handle the case where a record with the same phone number or email already exists
            return handle_response(message='Phone number / Email already exists', alert='alert-danger')

        if data.get('course_id') != None:
            course = Course.query.get(data.get('course_id'))
            if not course:
                return handle_response(message='Invalid course selected', alert='alert-danger')
            
        save_new_data = Enrollment(**data)
        save_new_data.course = course

        db.session.add(save_new_data)
        db.session.commit()
        db.session.flush()
        db.session.refresh(save_new_data)

        data = save_new_data.to_dict()
        

        """ msg = f"Hi Dunis Technologies. \
        Kindly refer to this incoming enrollment request from \
        {data['name']} | {data['email']} | {data['phone']}  for {data['course']['name']} "
        #notifyer_phone = notifyer.send_sms(data.phone, msg)
        user = User(username=data['name'], email=data['email'], course=data['course']['name'])
        notifyer_email = notifyer.xenrol_email(user) """

        """ notifyer_email = notifyer.send_email(
                subject="Incoming Enrollment Request",
                sender={data['email']},
                recipients=["info@dunistech.ng"],
                text_body=msg,
                html_body="email_template.html",
                #username=f"{data['name']}"
            ) """

        """ notifyer_email_1 = notifyer.send_email(
                subject="Incoming Enrollment Request",
                sender="info@dunistech.ng",
                recipients={data['email']},
                text_body=msg,
                html_body="email_template.html",
                #username=f"{data['name']}"
            ) """
        
        # Assuming data is a dictionary with keys 'name', 'email', and 'course'
        user_data = {
            'username': data.get('name', ''),
            'email': data.get('email', ''),
        }

        user = User(**user_data)

        # Add a temporary 'course' attribute to the User object
        selected_course = data.get('course', {}).get('name', '')
        setattr(user, 'course', selected_course)

        notifyer_email = notifyer.xenrol_email(user)

        #if not notifyer_phone or not notifyer_email:
        if not notifyer_email:
            return handle_response(message='Successful submission but admin will be informed later.', \
            data=data, alert='alert-success')

        return handle_response(message='Your submission was successful', data=data, alert='alert-success')

    except jsonschema.exceptions.ValidationError as e:
        db.session.rollback()
        # Handle the validation error here
        return handle_response(message=str(e), alert='alert-danger')

    except Exception as e:
        db.session.rollback()
        # Print the traceback
        traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

@xenrol_bp.route('/listings/<int:id>', methods=['GET'])
@token_auth.login_required
def get_listing(id):
    return jsonify(Listing.query.get_or_404(id).to_dict())

@xenrol_bp.route('/listings', methods=['GET'])
#@token_auth.login_required
def get_listings():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Listing.to_collection_dict(Listing.query, page, per_page, 'xenrol_api.get_listings')
    return jsonify(data)

@xenrol_bp.route('/listings/<int:id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    user = Listing.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Listing.to_collection_dict(user.followers, page, per_page,
                                   'xenrol_api.get_followers', id=id)
    return jsonify(data)

@xenrol_bp.route('/listings/<int:id>/followed', methods=['GET'])
@token_auth.login_required
def get_followed(id):
    user = Listing.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Listing.to_collection_dict(user.followed, page, per_page,
                                   'xenrol_api.get_followed', id=id)
    return jsonify(data)

@xenrol_bp.route('/listings/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_listing(id):
    if token_auth.current_user().id != id:
        abort(403)
    listing = Listing.query.get_or_404(id)
    data = request.get_json() or {}

    if any(key not in data for key in mandatory_dt):
        return bad_request('Missing required information for updating this listing')
    """ if 'images' in data and data['images'] != user.username and \
            Listing.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            Listing.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address') """
    listing.from_dict(data, new_listing=False)
    db.session.commit()
    return jsonify(listing.to_dict())
