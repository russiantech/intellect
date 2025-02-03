

import jsonschema, json
from flask import Blueprint, jsonify, request
from web.models import db, Category

x_category_bp = Blueprint('x_category_api', __name__)

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
            "category_id": { "type": "integer" },
            "image": { "type": "string" }
        },

        },
}

# Creates a category under a given lesson
@x_category_bp.route('/create_category', methods=['POST'])
#@db_session_management
def create_category():
    try:
        if not db.session.is_active:
            db.session.begin()

        #get-data
        data = request.get_json()

        #validate-data
        valid_schema = _schemas.get('save-data')
        jsonschema.validate(instance=data, schema=valid_schema)

        # Create a new category and associate it with the course
        new_category = Category(**data)
        
        db.session.add(new_category)
        db.session.commit()
        
        return jsonify({'message': 'Category created successfully'}), 201
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

# Updates a category
@x_category_bp.route('/update_category/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    try:
        if not db.session.is_active:
            db.session.begin()

        #get-data
        data = request.get_json()

        #validate-data
        valid_schema = _schemas.get('save-data')
        jsonschema.validate(instance=data, schema=valid_schema)

        category = Category.query.get_or_404(category_id)

        # Update the category attributes
        for key, value in data.items():
            setattr(category, key, value)
        
        db.session.commit()
        
        return jsonify({'message': 'Category updated successfully'})
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

# Deletes a category
@x_category_bp.route('/delete_category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        if not db.session.is_active:
            db.session.begin()

        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
    
        return jsonify({'message': 'Category deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

# Returns * the different categories
@x_category_bp.route('/get_categories', methods=['GET'])
def get_categories():
    try:
        if not db.session.is_active:
            db.session.begin()

        categorys = Category.query.all()
        category_list = [{'id': category.id, 'title': category.title, 'desc': category.desc} for category in categorys]
        return jsonify(category_list)
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

# Returns categorys for a given lesson  
@x_category_bp.route('/get_categorys_for_lesson/<int:lesson_id>', methods=['GET'])
def get_categorys_for_lesson(lesson_id):
    try:
        if not db.session.is_active:
            db.session.begin()

        lesson = Lesson.query.get_or_404(lesson_id)

        # Extract categorys information for the lesson
        categorys_data = []
        for category in lesson.categorys:
            # Add the parsed desc to the category data
            category_data = {
                'id': category.id,
                'image': category.image,
                'title': category.title,
                'desc': category.desc,
                'created': category.created,
                'updated': category.updated,
                'deleted': category.deleted,
                'active': category.active,
            }

            categorys_data.append(category_data)

        return jsonify(categorys_data)
    
    except Exception as e:
            db.session.rollback()
            #traceback.print_exc()
            return handle_response(message=str(e), alert='alert-danger')

# Returns a single category details
@x_category_bp.route('/get_category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    try:
        if not db.session.is_active:
            db.session.begin()
        category = Category.query.get_or_404(category_id)

        # Convert category information to a dictionary for JSON response
        category_data = {
            'id': category.id,
            'image': category.image,
            'title': category.title,
            'desc': category.desc,
            'created': category.created,
            'updated': category.updated,
            'deleted': category.deleted,
            'active': category.active,
        }

        return jsonify(category_data)
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

# Flask route to insert categories
@x_category_bp.route('/insert_categories', methods=['GET'])
def insert_categories():
    categories = [
        {'title': 'All', 'desc': 'Explore a wide range of courses covering various topics from programming to design.'},
        {'title': 'Trending', 'desc': 'Discover the hottest and most popular courses trending in the e-learning community.'},
        {'title': 'New Courses', 'desc': 'Stay updated with the latest additions to our ever-growing course catalog.'},
        {'title': 'Data & Data Science', 'desc': 'Dive into the world of data, analytics, and data science with our specialized courses.'},
        {'title': 'Free Courses', 'desc': 'Access a collection of high-quality courses available for free to enhance your skills.'},
        {'title': 'Analytics', 'desc': 'Master the art of data analysis and gain insights with our analytics-focused courses.'},
        {'title': 'Mobile Development', 'desc': 'Learn to build innovative mobile applications with our comprehensive mobile development courses.'},
        {'title': 'Hacking', 'desc': 'Explore the exciting world of ethical hacking and cybersecurity to protect digital systems.'},
        {'title': 'Cyber Security', 'desc': 'Enhance your cybersecurity skills and stay ahead in the constantly evolving digital landscape.'},
        {'title': 'Programming', 'desc': 'Build a solid foundation in programming languages and become a proficient coder.'},
        {'title': 'Web Development', 'desc': 'Become a web development expert with our courses covering front-end and back-end technologies.'},
        {'title': 'Machine Learning', 'desc': 'Delve into the realm of machine learning and artificial intelligence with our specialized courses.'},
        {'title': 'Software Development', 'desc': 'Master the software development life cycle and refine your coding skills.'},
        {'title': 'Javascript', 'desc': 'Explore the versatile world of JavaScript and create dynamic and interactive web pages.'},
        {'title': 'Beginner', 'desc': 'Perfect for beginners, these courses provide a gentle introduction to various subjects.'},
        {'title': 'Advanced', 'desc': 'Challenge yourself with advanced courses designed for experienced learners.'},
        {'title': 'UI/UX Designs', 'desc': 'Learn the principles of user interface and user experience design for creating visually appealing applications.'},
        {'title': 'Digital Marketing', 'desc': 'Unlock the secrets of digital advertising and enhance your online presence.'},
        {'title': 'Internet Of Things', 'desc': 'Discover the fascinating world of IoT and build connected devices for the future.'},
        {'title': 'Full Stack Development', 'desc': 'Become a full-stack developer by mastering both front-end and back-end technologies.'},
        {'title': 'Artificial Intelligence', 'desc': 'Dive deep into the world of AI and explore its applications in various domains.'},
        {'title': 'Python', 'desc': 'Learn the popular programming language Python and its versatile applications.'},
        {'title': 'Game Development', 'desc': 'Create your own interactive games with our game development courses.'}
    ]

    for category_data in categories:
        new_category = Category(**category_data)
        db.session.add(new_category)

    db.session.commit()

    return jsonify({'message': 'Categories inserted successfully'}), 201
