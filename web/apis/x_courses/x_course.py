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

""" _schemas = {
    'save-data': {
        "type": "object",
        "properties": {
            "title": { "type": "string" },
            "desc": { "type": "string" },
            "course_id": { "type": "integer" },
            "image": { "type": "string" }
        },

        },
} """
_schemas = {
    'save-data': {
        "type": "object",
        "properties": {
            "title": { "type": "string" },
            "desc": { "type": "string" },
            "course_id": { "type": "integer" },
            "image": { "type": "string" },
            "category_ids": {
                "type": "array",
                "items": {
                    "type": "integer"
                }
            }
        },
        "required": ["title", "desc", "course_id", "category_ids"],  # Required fields
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

""" @x_course_bp.route('/update_course/<int:course_id>', methods=['PUT'])
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

        #data['slug'] = make_slug(data['title']) // DO NOT UPDATE SLUG-URL EVERYTIME 

        data['desc'] = json.dumps(data['desc'])

        # Update the course attributes
        for key, value in data.items():
            setattr(course, key, value)
        
        db.session.commit()
        
        return jsonify({'message': 'Course updated successfully'})
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger') """
    

@x_course_bp.route('/update_course/<int:course_id>', methods=['PUT'])
@csrf.exempt
def update_course(course_id):
    try:
        if not db.session.is_active:
            db.session.begin()

        # Get data from the request
        data = request.get_json()

        # Validate data (assuming a schema is used)
        valid_schema = _schemas.get('save-data')
        jsonschema.validate(instance=data, schema=valid_schema)

        # Check if the course exists
        course = Course.query.get_or_404(course_id)
        if not course:
            return jsonify({'error': 'Invalid Course'}), 400

        # Check for multiple category IDs
        category_ids = data.get('category_ids', [])  # Expecting a list of category IDs

        # Validate that the provided category IDs exist in the database
        valid_categories = Category.query.filter(Category.id.in_(category_ids)).all()

        if not valid_categories:
            return jsonify({'error': 'Invalid categories'}), 400

        # Update course image if provided
        course_image = request.files.get('image')
        if course_image:
            course_image_name = uploader(course_image)
        else:
            course_image_name = 'default.webp'
        data['image'] = course_image_name

        # Do not update slug every time
        # data['slug'] = make_slug(data['title']) 

        # Update the course description and other attributes
        data['desc'] = json.dumps(data['desc'])
        for key, value in data.items():
            setattr(course, key, value)

        # Update the categories (many-to-many)
        course.categories = valid_categories

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Course updated successfully'})
    
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

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
""" @x_course_bp.route('/get_course/<string:course_slug>', methods=['GET'])
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
    
    return jsonify(course_data) """

@x_course_bp.route('/get_course/<string:course_slug>', methods=['GET'])
def get_course(course_slug):
    # Retrieve course information based on the slug
    course = Course.query.filter_by(slug=course_slug).first_or_404()
    
    # Optionally include lessons and topics
    include_lessons = request.args.get('include_lessons') == 'true'
    include_topics = request.args.get('include_topics') == 'true'
    
    # Check if category dict should be returned
    return_category_dict = request.args.get('return_category_dict') == 'true'
    
    course_data = course.serialize(
        include_lessons=include_lessons, include_topics=include_topics, 
        current_user=current_user or None, return_category_dict=return_category_dict
    )
    
    return jsonify(course_data)

""" @x_course_bp.route('/fetch-by-categories', methods=['GET'])
def fetch_by_categories():
    category_ids = request.args.get('categories')  # Example: '1,2,3'
    if category_ids:
        category_ids = [int(cid) for cid in category_ids.split(',')]  # Convert to list of integers
        courses = Course.query.filter(Course.categories.any(Category.id.in_(category_ids))).all()
    else:
        courses = Course.query.all()  # Return all courses if no category is selected
    
    # Serialize and return the courses as JSON
    courses_data = [course.serialize() for course in courses]
    return jsonify(courses_data) """

@x_course_bp.route('/fetch-by-categories', methods=['GET'])
def fetch_by_categories():
    """
        Explanations:
        Limit and Offset:
        limit = request.args.get('limit', type=int): This allows you to specify how many courses to return. 
        If the limit is provided in the query parameters, it will apply to the query. Otherwise, no limit will be applied.
        offset = request.args.get('offset', type=int, default=0): The offset parameter is used to skip a specific number of records, 
        allowing for pagination. By default, the offset is set to 0 (i.e., start from the first record).
        Example Usage:
        Fetch all courses in categories 1, 2, and 3: /fetch-by-categories?categories=1,2,3
        Fetch only 5 courses in categories 1, 2, and 3: /fetch-by-categories?categories=1,2,3&limit=5
        Fetch 5 courses, skipping the first 10: /fetch-by-categories?categories=1,2,3&limit=5&offset=10
        This setup allows flexibility for pagination and result limiting when fetching the courses. 
    """
    try:
        # Get the category IDs from the query parameter
        category_ids = request.args.get('categories')  # Example: '1,2,3'
        
        # Get additional parameters for limit and offset
        limit = request.args.get('limit', type=int)  # Default is None if not provided
        offset = request.args.get('offset', type=int, default=0)  # Default to 0 if not provided
        
        # Start query for courses
        query = Course.query
        
        if category_ids:
            try:
                category_ids = [int(cid) for cid in category_ids.split(',')]  # Convert to list of integers
            except ValueError:
                return jsonify({"error": "Invalid category IDs"}), 400  # Return a bad request response if parsing fails
            
            # Filter courses by the provided category IDs
            query = query.filter(Course.categories.any(Category.id.in_(category_ids)))
        
        # Apply limit and offset if provided
        if limit:
            query = query.limit(limit)
        
        if offset:
            query = query.offset(offset)
        
        # Execute the query and fetch the courses
        courses = query.all()
        
        # Serialize and return the courses as JSON
        courses_data = [course.serialize() for course in courses]
        return jsonify(courses_data)
    
    except Exception as e:
        # Catch any unexpected errors and return a 500 error with the exception message
        return jsonify( {"success":False, "error": str(e)} ), 500


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


