

import json, traceback, jsonschema
from flask_login import current_user, login_required
from flask import Blueprint, jsonify, request
from web.models import db, Course, Category
from web.utils.uploader import uploader
from web.apis.make_slug import make_slug
from web.extensions import csrf

x_course_bp = Blueprint('x_course_api', __name__)

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
            "course_id": { "type": "integer" },
            "image": { "type": "string" }
        },

        },
}

@x_course_bp.route('/more')
def loadmore():
    offset = int(request.args.get('offset') or 0)
    limit = int(4)
    all = Course.query.all()
    course = all[ offset : offset + limit ]
    #course = all[ offset : offset + limit ]
    #total = len(all)
    return jsonify( [ { 'title': c.title, 'image': c.image, 'slug': c.slug, 'fee': c.fee,'id': c.id } for c in course  ] ) 
    
@x_course_bp.route('/create_course', methods=['POST'])
#@db_session_management
@csrf.exempt
def create_course():
    try:
        if not db.session.is_active:
            db.session.begin()

        #get-data
        data = request.get_json()

        #print(f"Titled-Slug: {make_slug(data.get('title'))}" )
        #return jsonify({'message': str(data) }), 201
        
        #validate-data
        valid_schema = _schemas.get('save-data')
        jsonschema.validate(instance=data, schema=valid_schema)

        # Check if the category exists
        category_id = data.get('category_id')  # Assuming category_id is selected in the form
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Invalid category'}), 400
        
        course_image = request.files.get('image')
        # Save the uploaded photo
        if course_image:
            course_image_name = uploader(course_image)
        else:
            course_image_name = 'default.webp'
            #update the uploaded course image name
            data['image'] = course_image_name


        data['slug'] = make_slug(data['title'])

        data['desc'] = json.dumps(data['desc'])

        #save-data
        new_course = Course(**data, category=[category]) 
        
        db.session.add(new_course)
        db.session.commit()
        
        return jsonify({'message': f'Course({new_course.title}) created successfully'}), 201
    
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

@x_course_bp.route('/update_course/<int:course_id>', methods=['PUT'])
@csrf.exempt
def update_course(course_id):
    try:
        if not db.session.is_active:
            db.session.begin()

        #get-data
        data = request.get_json()

        #validate-data
        valid_schema = _schemas.get('save-data')
        jsonschema.validate(instance=data, schema=valid_schema)

        # Check if the course exists
        course = Course.query.get_or_404(course_id)
        if not course:
            return jsonify({'error': 'Invalid Course'}), 400

        # Check if the category exists
        category_id = data.get('category_id')  # Assuming category_id is selected in the form
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Invalid category'}), 400
        
        course_image = request.files.get('image')
        # Save the uploaded photo
        if course_image:
            course_image_name = uploader(course_image)
        else:
            course_image_name = 'default.webp'
            #update the uploaded course image name
            data['image'] = course_image_name

        #data['slug'] = make_slug(data['title']) """ DO NOT UPDATE SLUG-URL EVERYTIME """

        data['desc'] = json.dumps(data['desc'])

        # Update the course attributes
        for key, value in data.items():
            setattr(course, key, value)
        
        db.session.commit()
        
        return jsonify({'message': 'Course updated successfully'})
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

@x_course_bp.route('/delete_course/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    
    return jsonify({'message': 'Course deleted successfully'})

""" @x_course_bp.route('/get_courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    course_list = [{'id': course.id, 'title': course.title, 'fee': course.fee, 'desc': course.desc} for course in courses]
    return jsonify(course_list) """


""" @x_course_bp.route('/get_course_/<string:course_slug>', methods=['GET'])
def get_course_(course_slug):
    # Retrieve course information based on the slug
    course = Course.query.filter_by(slug=course_slug).first_or_404()
    
    # Convert course information to a dictionary for JSON response
    course_data = {
        'id': course.id,
        'image': course.image,
        'title': course.title,
        'desc': course.desc,
        'video': course.video,
        'material': course.material,
        'fee': course.fee,
        'lang': course.lang,
        'duration': course.duration,
        'level': course.level,
        'views': course.views,
        'comment': course.comment,
        'rating': course.rating,
        'completedby': course.completedby,
        'status': course.status,
        'slug': course.slug,
        'user': course.user,
        'created': course.created,
        'updated': course.updated,
        'deleted': course.deleted,
        'active': course.active,
    }
    
    # Check if lessons should be included
    include_lessons = request.args.get('include_lessons')
    if include_lessons == 'true':
        # Fetch lessons related to the course
        lessons = [lesson.serialize() for lesson in course.lessons]
        course_data['lessons'] = lessons
    
    # Check if topics should be included
    include_topics = request.args.get('include_topics')
    if include_topics == 'true':
        # Fetch topics related to the course
        topics = [topic.serialize() for topic in course.topics]
        course_data['topics'] = topics
    
    return jsonify(course_data)

 """

""" ================================== """

# Route to get all courses
@x_course_bp.route('/get_courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    # Serialize each course and create a list of serialized course data
    course_list = [course.serialize() for course in courses]
    return jsonify(course_list)

# Route to get a specific course by slug
@x_course_bp.route('/get_course/<string:course_slug>', methods=['GET'])
#@login_required
def get_course(course_slug):
    # Retrieve course information based on the slug
    course = Course.query.filter_by(slug=course_slug).first_or_404()
    
    # Serialize the course data, optionally including lessons and topics
    include_lessons = request.args.get('include_lessons') == 'true'
    include_topics = request.args.get('include_topics') == 'true'
    course_data = course.serialize(
        include_lessons=include_lessons, include_topics=include_topics, 
        current_user=current_user or None
        )
    
    return jsonify(course_data)

@x_course_bp.route('/x_course_api.loadmore', methods=['GET'])
def load_more_courses():
    offset = int(request.args.get('offset', 0))
    selected_categories = request.args.getlist('categories')  # Update this line

    print("selected_categories:", selected_categories)
    
    query = Course.query
    if selected_categories:
        query = query.filter(Course.category_id.in_(selected_categories))
    
    courses = query.offset(offset).limit(10).all()
    # print([{x.title, x.category_id} for x in courses])
    # print("Total is:", len(courses))
    include_only = ['id', 'fee', 'category_id', 'image', 'title', 'rating', 'slug']
    return jsonify([course.serialize(include_only=include_only) for course in courses])


