import json
import traceback
from flask_login import current_user, login_required
import jsonschema
from flask import Blueprint, current_app, jsonify, request
from web.apis.make_slug import make_slug
from web.models import db, Path, Course
from web.extensions import csrf
from web.utils.uploader import uploader

x_path_bp = Blueprint('x_path_api', __name__)

def handle_response(message=None, alert=None, data=None):
    response_data = {
        'message': message,
    }
    if alert:
        response_data['alert'] = alert

    if data:
        response_data['data'] = data

    return response_data

""" _schemas = {
    'save-data': {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "desc": {"type": "string"},
            "image": {"type": "string", "format": "uri"},
            "fee": {"type": "number"},
            "rating": {"type": "number"},
            "duration": {"type": "integer"},
            "course_ids": {"type": "array", "items": {"type": "integer"}}
        },
        "required": ["title", "desc"]
    },
} """

schemas = {
    'save-data':{
    "type": "object",
    "properties": {
        "fee": {
            "type": ["string", "null"],
            "description": "The fee for the path."
        },
        #"fee": {"type": "number"},
        "title": { "type": "string" },
        "desc": { "type": "string" },
        "image": {"type": "string", "format": "uri"},
        "course_ids": {
            "type": "array",
            "items": { "type": "integer" }
        },
        "duration": { "type": "string" },
        "level": { "type": "string" },
        "rating": { "type": ["string", "null"] },
        "path_id": { "string": "integer" }
    },
    "required": ["title", "desc"]
}

}

# Creates a Path
@x_path_bp.route('/create_path', methods=['POST'])
@csrf.exempt
# @login_required
def create_path():
    try:
        if not db.session.is_active:
            db.session.begin()

        data = request.get_json()
        image = request.files.get('image')  # Get the uploaded image file
        
        # Validate data
        valid_schema = schemas.get('save-data')
        jsonschema.validate(instance=data, schema=valid_schema)
        print(data)

        # Create new Path
        new_path = Path(
            title=data['title'],
            slug=make_slug(data['title']),
            desc=data['desc'],
            fee=data.get('fee', 0.0),
            rating=data.get('rating'),
            duration=data.get('duration')
        )

        # Associate courses with the path
        course_ids = data.get('course_ids', [])
        for course_id in course_ids:
            course = Course.query.get_or_404(course_id)
            new_path.courses.append(course)

        db.session.add(new_path)
        db.session.commit()
        db.session.refresh(new_path)

        return jsonify({'success':True, 'message': f'Path {new_path.title} created successfully'}), 201

    except jsonschema.exceptions.ValidationError as e:
        return jsonify({'success':False, 'error': f'{e}'})
    
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'success':False, 'error': f'{e}'})

""" # Updates a Path
@x_path_bp.route('/update_path/<int:path_id>', methods=['PUT'])
@csrf.exempt
@login_required
def update_path(path_id):
    try:
        if not db.session.is_active:
            db.session.begin()

        data = request.get_json()

        # Validate data
        valid_schema = schemas.get('save-data')
        jsonschema.validate(instance=data, schema=valid_schema)

        # Fetch the existing Path
        path = Path.query.get_or_404(path_id)

        # Update Path attributes
        path.title = data['title']
        path.desc = data['desc']
        path.fee = data.get('fee', path.fee)
        path.rating = data.get('rating', path.rating)
        path.duration = data.get('duration', path.duration)

        # Update course associations
        path.courses.clear()
        course_ids = data.get('course_ids', [])
        for course_id in course_ids:
            course = Course.query.get_or_404(course_id)
            path.courses.append(course)

        db.session.commit()

        return jsonify({'message': f'Path({path.title}) updated successfully'})

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'success':False, 'error': f'{e}'})
        # return jsonify(handle_response(message=str(e), alert='alert-danger'))
        # return jsonify(handle_response(message=str(e), alert='alert-danger')), 400 """

# Updates a Path
@x_path_bp.route('/update_path/<int:path_id>', methods=['PUT'])
@csrf.exempt
# @login_required
def update_path(path_id):
    try:

        if not current_user.is_authenticated:
            return jsonify({'success':False, 'error': f'Kindly authenticate your-self to continue'})
        
        if not db.session.is_active:
            db.session.begin()

        # Fetch the existing Path
        path = Path.query.get_or_404(path_id)
        if not path:
            return jsonify({'success':False, 'error': 'requested path does not exist.'}), 400
        
        # Check if request is multipart (FormData)
        if request.content_type.startswith('multipart/form-data'):
            # Handling FormData submissions
            data = request.form.to_dict()  # Parse form fields
            path_image = request.files.get('image')  # Get the image file
            
            # Convert course_ids from JSON string to a Python list if it's included
            if 'course_ids' in data:
                data['course_ids'] = json.loads(data['course_ids'])

        elif request.content_type == 'application/json':
            # Handling JSON submissions
            data = request.get_json()  # Get the JSON data
            
        else:
            return jsonify({'success': False, 'error': 'Unsupported Media Type.'}), 415

        print(f"Incoming data: {data}")  # Debugging log

        # Validate data
        valid_schema = schemas.get('save-data')
        jsonschema.validate(instance=data, schema=valid_schema)

        path_image = request.files.get('image')
        # Save the uploaded photo
        if path_image:
            # path.image = uploader(path_image)
            # from os import path
            # path_image = uploader(path_image, custom_upload_path=path.join(current_app.root_path, 'static/img/course/path') )
            # path.image = path_image
            
            from os import path as os_path  # Rename the module reference to avoid conflicting with path object.
            path_image = uploader(path_image, custom_upload_path=os_path.join(current_app.root_path, 'static/img/course/path'))
            path.image = path_image

        else:
            # path_image_name = 'default.webp'
            #update the uploaded course image name
            # data['image'] = path_image_name
            path.image = None

        # Only update fields if they are provided in the request data, leave others unchanged
        if 'title' in data and data['title']:
            path.title = data['title']
        
        if 'desc' in data and data['desc']:
            path.desc = data['desc']

        if 'fee' in data:
            path.fee = int(data['fee']) if data['fee'] is not None else path.fee

        if 'rating' in data:
            path.rating = int(data['rating']) if data['rating'] is not None else path.rating

        if 'duration' in data:
            path.duration = int(data['duration']) if data['duration'] is not None else path.duration

        # Update course associations if provided
        if 'course_ids' in data:
            path.courses.clear()  # Remove current courses
            course_ids = data.get('course_ids', [])
            for course_id in course_ids:
                course = Course.query.get_or_404(course_id)
                path.courses.append(course)

        # Commit the changes to the database
        db.session.commit()
        db.session.refresh(path)
        
        # print(f"Updated path title: {path.title}")  # Debugging log
        
        return jsonify({'success':True, 'message': f'{path.title} path updated successfully'})

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'{e}, {path_image, data }'})


# Deletes a Path
@x_path_bp.route('/delete_path/<int:path_id>', methods=['DELETE'])
@csrf.exempt
# @login_required
def delete_path(path_id):
    try:
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'Kindly authenticate yourself to continue'})

        if not db.session.is_active:
            db.session.begin()

        # Fetch the path to delete
        path = Path.query.get_or_404(path_id)

        # Clear the path-course associations (without affecting the actual courses or lessons)
        path.courses.clear()  # This will clear the association in the junction/association table

        # Delete the path itself
        db.session.delete(path)
        db.session.commit()

        return jsonify({'success': True, 'message': f"{request.get_json()['title']} deleted successfully"})

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'{e}'})


# Fetches all Paths
@x_path_bp.route('/get_paths', methods=['GET'])
# @login_required
@csrf.exempt
def get_paths():
    try:

        # if not current_user.is_authenticated:
        #     return jsonify({'success':False, 'error': f'Kindly authenticate your-self to continue'})
        
        paths = Path.query.all()
        path_list = [path.serialize() for path in paths]
        return jsonify(path_list)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify(handle_response(message=str(e), alert='alert-danger')), 400

# Fetches a single Path by slug
@x_path_bp.route('/get_path/<slug>', methods=['GET'])
# @login_required
@csrf.exempt
def get_path(slug):
    try:
        if not current_user.is_authenticated:
            
            return jsonify({'success':False, 'error': f'Kindly authenticate your-self to continue'})
        
        path = Path.query.filter_by(slug=slug).first_or_404()
        
        return jsonify(path.serialize())
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success":False, "error":str(e), "alert":'alert-danger'}), 400

# by id
@x_path_bp.route('/get_path/<int:path_id>', methods=['GET'])
# @login_required
@csrf.exempt
def get_path_by_id(path_id):
    try:

        if not current_user.is_authenticated:
            return jsonify({'success':False, 'error': f'Kindly authenticate your-self to continue'})
        
        path = Path.query.get_or_404(path_id)
        return jsonify(path.to_dict())
    except Exception as e:
        traceback.print_exc()
        return jsonify(handle_response(message=str(e), alert='alert-danger')), 400
