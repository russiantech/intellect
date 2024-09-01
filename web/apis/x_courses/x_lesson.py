import json, traceback, jsonschema
from flask import Blueprint, jsonify, request
from web.models import db, Course, Lesson
from web.utils.uploader import uploader
from web.apis.make_slug import make_slug
from web.extensions import csrf
x_lesson_bp = Blueprint('x_lesson_api', __name__)

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
            "title": { "type": "string" },
            "desc": { "type": "string" },
            "lesson_id": { "type": "integer" },
            "image": { "type": "string" }
        },

        },
}

# Creates a lesson
@x_lesson_bp.route('/create_lesson', methods=['POST'])
#@db_session_management
@csrf.exempt
def create_lesson():
    try:

        if not db.session.is_active:
            db.session.begin()

        #get-data
        data = request.get_json()

        #validate-data
        valid_schema = _schemas.get('save-data')
        jsonschema.validate(instance=data, schema=valid_schema)
        
        # Assuming 'course_id' is included in the data received
        course_id = data.get('course_id')

        # Check if the course_id is valid
        #course = Course.query.get_or_404(course_id)
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'message': f'Invalid Course ({course_id})'} ) #400

        lesson_image = request.files.get('image')
        # Save the uploaded photo
        if lesson_image:
            lesson_image_name = uploader(lesson_image)
        else:
            lesson_image_name = 'default.png'
        
        #update the uploaded course image name
        data['image'] = lesson_image_name

        #print(lesson.course.id)
        data['slug'] = make_slug(data['title'])

        data['desc'] = json.dumps(data['desc'])
        
        # Create a new lesson and associate it with the course
        new_lesson = Lesson(**data, course=course)
        
        db.session.add(new_lesson)
        db.session.commit()
        
        return jsonify({'message': f'Lesson({new_lesson.title}) created successfully'}), 201
    
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

# Updates a particular lesson
@x_lesson_bp.route('/update_lesson/<int:lesson_id>', methods=['PUT'])
@csrf.exempt
def update_lesson(lesson_id):
    try:
        if not db.session.is_active:
            db.session.begin()

        #get-data
        data = request.get_json()

        #validate-data
        valid_schema = _schemas.get('save-data')
        jsonschema.validate(instance=data, schema=valid_schema)

        lesson = Lesson.query.get_or_404(lesson_id)
        if not lesson:
            return jsonify({'error': 'Invalid Lesson'}), 400
        
        lesson_image = request.files.get('image')
        # Save the uploaded photo
        if lesson_image:
            lesson_image_name = uploader(lesson_image)
        else:
            lesson_image_name = 'default.webp'
            #update the uploaded course image name
            data['image'] = lesson_image_name

        #data['slug'] = make_slug(data['title']) """ DO NOT UPDATE SLUG-URL EVERYTIME """

        data['desc'] = json.dumps(data['desc'])

        # Update the lesson attributes
        for key, value in data.items():
            setattr(lesson, key, value)
        
        db.session.commit()
        
        return jsonify({'message': f"Lesson({data['title']}) updated successfully for Lesson({lesson.course.title})"})
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

# Deletes a particular lesson
@x_lesson_bp.route('/delete_lesson/<int:lesson_id>', methods=['DELETE'])
def delete_lesson(lesson_id):
    try:

        if not db.session.is_active:
                db.session.begin()
        lesson = Lesson.query.get_or_404(lesson_id)
        db.session.delete(lesson)
        db.session.commit()
        
        return jsonify({'message': 'Lesson deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

# Returns all lessons/modules
@x_lesson_bp.route('/get_lessons', methods=['GET'])
def get_lessons():
    try:
        if not db.session.is_active:
            db.session.begin()

        lessons = Lesson.query.order_by(Lesson.created.desc()).all()
        lesson_list = [{'id': lesson.id, 'course_id': lesson.course.id, 'title': lesson.title, 'desc': lesson.desc} for lesson in lessons]
        return jsonify(lesson_list)


        """lessons = Lesson.queryorder_by(Lesson.created.desc()).all()
        lesson_list = [{'id': lesson.id, 'course_id': lesson.course.id, 'title': lesson.title, 'desc': lesson.desc} for lesson in lessons]
        return jsonify(lesson_list) """

    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

# Returns a single lesson details
@x_lesson_bp.route('/get_lesson/<int:lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    try:
        if not db.session.is_active:
            db.session.begin()

        lesson = Lesson.query.get_or_404(lesson_id)
        
        # Convert lesson information to a dictionary for JSON response
        lesson_data = {
            'id': lesson.id,
            'image': lesson.image,
            'title': lesson.title,
            'desc': lesson.desc,
            'created': lesson.created,
            'updated': lesson.updated,
            'deleted': lesson.deleted,
            'active': lesson.active,
        }

        return jsonify(lesson_data)
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')
