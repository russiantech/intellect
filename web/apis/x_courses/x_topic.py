

import traceback
from flask_login import current_user, login_required
import jsonschema, json
from flask import Blueprint, jsonify, request
from web.models import db, User, Lesson, Topic, Enrollment
from web.utils.uploader import uploader
from web.apis.make_slug import make_slug
from web.extensions import csrf

x_topic_bp = Blueprint('x_topic_api', __name__)

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
            "topic_id": { "type": "integer" },
            "image": { "type": "string" }
        },

        },
}

# Creates a topic under a given lesson (Auth & Admin)
@x_topic_bp.route('/create_topic', methods=['POST'])
@csrf.exempt
@login_required
#@db_session_management
@csrf.exempt
def create_topic():
    try:
        if not db.session.is_active:
            db.session.begin()

        #get-data
        data = request.get_json()

        #validate-data
        valid_schema = _schemas.get('save-data')
        jsonschema.validate(instance=data, schema=valid_schema)
        
         # Assuming 'lesson_id' is included in the data received
        lesson_id = data.get('lesson_id')

        # Check if the lesson_id is valid
        lesson = Lesson.query.get_or_404(lesson_id)

        data['course_id'] = lesson.course.id #bcos `course_id` is a required column/attribute of Topic() model

        #print(lesson.course.id)
        data['slug'] = make_slug(data['title'])

        data['desc'] = json.dumps(data['desc'])

        # Create a new topic and associate it with the course
        new_topic = Topic(**data, lessons=lesson)
        
        db.session.add(new_topic)
        db.session.commit()
        
        return jsonify({'message': f'Topic({new_topic.title}) created successfully'}), 201
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

# Updates a topic (Auth & Admin)
@x_topic_bp.route('/update_topic/<int:topic_id>', methods=['PUT'])
@csrf.exempt
@login_required
def update_topic(topic_id):
    try:
        if not db.session.is_active:
            db.session.begin()

        #get-data
        data = request.get_json()

        #validate-data
        valid_schema = _schemas.get('save-data')
        jsonschema.validate(instance=data, schema=valid_schema)

        topic = Topic.query.get_or_404(topic_id)
        if not topic:
            return jsonify({'success':False, 'error': 'Invalid Topic'}), 400
        
        topic_image = request.files.get('image')
        # Save the uploaded photo
        if topic_image:
            topic_image_name = uploader(topic_image)
        else:
            topic_image_name = 'default.webp'
            #update the uploaded course image name
            data['image'] = topic_image_name

        #data['slug'] = make_slug(data['title']) """ DO NOT UPDATE SLUG-URL EVERYTIME """

        data['desc'] = json.dumps(data['desc'])

        # Update the topic attributes
        for key, value in data.items():
            setattr(topic, key, value)
        
        db.session.commit()
        
        return jsonify({'message': f'Topic {topic.title} of {topic.lessons.title} updated successfully.'})
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')
 
# Deletes a topic
@x_topic_bp.route('/delete_topic/<string:topic_slug>', methods=['DELETE'])
def delete_topic(topic_slug):
    try:
        if not db.session.is_active:
            db.session.begin()

        # topic = Topic.query.get_or_404(topic_id) //deletion via id
        topic = Topic.query.filter_by(slug=topic_slug).first_or_404()
        db.session.delete(topic)
        db.session.commit()
    
        return jsonify({'message': 'Topic deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

# Returns topics for all different courses (Auth)
@x_topic_bp.route('/get_topics', methods=['GET'])
@csrf.exempt
@login_required
def get_topics():
    try:
        if not db.session.is_active:
            db.session.begin()

        topics = Topic.query.all()
        
        """ topic_list = [
            {'id': topic.id, 'course_id': topic.course.id, 'lesson_id': topic.lessons.id, 'title': topic.title, 'desc': topic.desc} for topic in topics if topics else None] """

        # Serialize the course data, optionally including lessons and topics
        include_desc = request.args.get('include_desc') == 'true'
        topic_list = [topic.serialize(include_desc=include_desc) for topic in topics ]
        
        #return jsonify(topic_data)

        return jsonify(topic_list)
    
    except Exception as e:
        db.session.rollback()
        #traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

# Returns topics for a given lesson (Auth & Enrollment)
@x_topic_bp.route('/get_topics_for_lesson/<int:lesson_id>', methods=['GET'])
@csrf.exempt
@login_required
def get_topics_for_lesson(lesson_id):
    try:
        if not db.session.is_active:
            db.session.begin()

        lesson = Lesson.query.get_or_404(lesson_id)

        # Extract topics information for the lesson
        topics_data = []
        for topic in lesson.topics:
            # Parse the JSON string to a Python object
            desc_json = json.loads(topic.desc)

            # Add the parsed desc to the topic data
            topic_data = {
                'id': topic.id,
                'image': topic.image,
                'title': topic.title,
                'desc': desc_json,
                'created': topic.created,
                'updated': topic.updated,
                'deleted': topic.deleted,
                'active': topic.active,
            }

            topics_data.append(topic_data)

        return jsonify(topics_data)
    
    except Exception as e:
            db.session.rollback()
            #traceback.print_exc()
            return handle_response(message=str(e), alert='alert-danger')

# Returns a single topic details(Auth)
@x_topic_bp.route('/get_topic_/<int:topic_id>', methods=['GET'])
@csrf.exempt
@login_required
def get_topic_(topic_id):
    try:
        if not db.session.is_active:
            db.session.begin()

        topic = Topic.query.get_or_404(topic_id)

        # Parse the JSON string to a Python object
        desc_json = json.loads(topic.desc)

        # Convert topic information to a dictionary for JSON response
        topic_data = {
            'id': topic.id,
            'image': topic.image,
            'title': topic.title,
            'desc': desc_json
        }

        return jsonify(topic_data)
    
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')

# Route to get a specific topic by slug
@x_topic_bp.route('/get_topic/<string:topic_slug>', methods=['GET'])
@csrf.exempt
@login_required
def get_topic(topic_slug):
    # Retrieve course information based on the slug
    topic = Topic.query.filter_by(slug=topic_slug).first_or_404()
    
    # Serialize the course data, optionally including lessons and topics
    include_desc = request.args.get('include_desc') == 'true'
    topic_data = topic.serialize(include_desc=include_desc)
    #print(topic_data)
    print(topic_data['desc']) if include_desc else print('include_desc is off, desc no follow')
    return jsonify(topic_data)

# Route to mark a topic as completed for a specific user
@x_topic_bp.route('/mark_completed', methods=['POST'])
@csrf.exempt
@login_required
def mark_completed():
    try:
        #return jsonify(request.json.get('topic_id'))
        
        with db.session.no_autoflush:
            # with db.session.no_autoflush: prevents premature flush
            # Begin a no_autoflush block-Perform multiple database operations-without triggering premature flushes
                
            if not db.session.is_active:
                db.session.begin()

            user_id = request.json.get('user_id') or current_user.id if current_user.is_authenticated else None

            topic_id = request.json.get('topic_id')

            user = User.query.get(user_id)
            topic = Topic.query.get(topic_id)

            if user and topic:
                # Check if the user has already completed this topic
                if topic in user.topic_progress:
                    return jsonify({'message': 'Topic already marked as completed for You'}) #, 400
                
                # Mark the topic as completed for the user
                user.topic_progress.append(topic)

                # Update the completed topics count in the Enrollment model
                enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=topic.lessons.course.id).first()
                if enrollment:
                    enrollment.completed_topics += 1
                    db.session.commit()
                    return jsonify({'message': 'Topic Marked As Completed For You'}), 200
                else:
                    # Handle the case where enrollment is None
                    return jsonify({'message': f'Topic Not marked Cos You\'re Not Currently Enrolled On {topic.course.title}'}), 200

            return jsonify({'message': f'User or topic not found {user_id, topic_id}'}) #, 404

    except Exception as e:
        db.session.rollback()
        print(e)
        traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger')
    

""" @x_topic_bp.route('/learning_progress_')
def learning_progress_():
    # Get the current user
    user = User.query.get(current_user.id)

    # Fetch all enrollments of the user
    enrollments = Enrollment.query.filter_by(user_id=user.id).all()

    # Prepare the response data
    response_data = []

    for enrollment in enrollments:
        # Get the course associated with the enrollment
        course = enrollment.course

        # Calculate the completion percentage for the course
        completion_percentage = course.calculate_completion_percentage(user)

        # Serialize the course data
        serialized_course = course.serialize(include_only= ['title', 'image', 'slug',])

        # Add completion percentage to the serialized course data
        serialized_course['progress'] = completion_percentage

        # Append the serialized course to the response data
        response_data.append(serialized_course)

    # Return the response as JSON
    #return jsonify({'user_courses': response_data})
    return jsonify([x:x[x] for x in response_data])
 """

@x_topic_bp.route('/learning_progress')
@csrf.exempt
@login_required
def learning_progress():
    # Get the current user
    user = User.query.get(current_user.id)

    # Fetch all enrollments of the user
    enrollments = Enrollment.query.filter_by(user_id=user.id).all()

    # Prepare the response data
    response_data = []

    for enrollment in enrollments:
        # Get the course associated with the enrollment
        course = enrollment.course

        # Calculate the completion percentage for the course
        completion_percentage = course.calculate_completion_percentage(user)

        # Serialize the course data
        serialized_course = course.serialize(include_only=['title', 'image', 'slug'])

        # Add completion percentage to the serialized course data
        serialized_course['progress'] = completion_percentage

        # Append the serialized course to the response data
        response_data.append(serialized_course)

    # Return the response as JSON
    return jsonify(response_data)

