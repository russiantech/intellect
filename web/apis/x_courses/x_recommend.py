from flask import Blueprint, jsonify, request
from web.models import Course, Category, category_course_association
from sqlalchemy import desc as sqlalchemy_desc

x_recommend_bp = Blueprint('x_recommend_api', __name__)

import re
def sanitize_input(input_str):
    """Ensure input is a string and remove any potentially dangerous characters."""
    if not isinstance(input_str, str):
        input_str = str(input_str) if input_str is not None else ''
    return re.sub(r'[^a-zA-Z0-9\s]', '', input_str)

# Fetch similar courses based on title, category, or description
from sqlalchemy import cast, String
""" def fetch_similar_courses_from_db1(skeyword):
    try:
        keyword = sanitize_input(skeyword)
        print("keyword", keyword)
        query = Course.query.filter(
            Course.title.ilike(f'%{keyword}%') |
            cast(Course.category.title, String).ilike(f'%{keyword}%') |
            cast(Course.desc, String).ilike(f'%{keyword}%')
        ).all()
        return query
    except Exception as e:
            # Log the exception and SQL query for further inspection
            print(f"Error occurred: {e}") """

from sqlalchemy.orm import aliased
def fetch_similar_courses_from_db(keyword):
    # Sanitize the keyword to avoid SQL injection or syntax errors
    sanitized_keyword = sanitize_input(keyword)
    
    # Log the sanitized keyword and debug the query if necessary
    print(f"Sanitized Keyword: {sanitized_keyword}")

    category_alias = aliased(Category)
    
    try:
        query = Course.query.join(
            category_course_association, Course.id == category_course_association.c.course_id) \
            .join(category_alias, category_alias.id == category_course_association.c.category_id) \
            .filter(
                (Course.title.ilike(f'%{sanitized_keyword}%')) |
                (category_alias.title.ilike(f'%{sanitized_keyword}%')) |
                (cast(Course.desc, String).ilike(f'%{sanitized_keyword}%'))
            ).all()
        
        print(query)  # Optional: Debug the output query
        return query
    except Exception as e:
        # Log the exception and SQL query for further inspection
        print(f"Error occurred: {e}")
        return []



# Fetch top courses based on a particular interaction (e.g., most viewed)
def fetch_top_courses():
    return Course.query.order_by(sqlalchemy_desc(Course.title)).limit(5).all()

# Endpoint to handle user interactions and provide recommendations
from web.extensions import csrf
@x_recommend_bp.route('/recommendations', methods=['POST'])
@csrf.exempt
def get_recommendations():

    try:
        interactions = request.json.get('interactions', [])
        # print('interactions:', interactions)
        if not interactions:
            # Fallback to top courses if no interactions provided
            top_courses = fetch_top_courses()
            return jsonify([{
                "title": course.title,
                "slug": course.id,  # or use any unique identifier
                "image": course.image,
                "fee": course.fee,
                "rating": course.rating,
                "desc": course.desc  # Assuming `desc` is the correct attribute
            } for course in top_courses])

        # Step 1: Analyze interactions to extract relevant keywords or course IDs
        keywords = set()
        for interaction in interactions:
            course = Course.query.get(interaction['course_id'])
            if course:
                keywords.add(course.title)
                keywords.add(course.category)
                keywords.add(course.desc)  # Assuming `desc` is the correct attribute

        # Step 2: Fetch matching courses from the database
        recommended_courses = []
        for keyword in keywords:
            similar_courses = fetch_similar_courses_from_db(keyword)
            recommended_courses.extend(similar_courses)

        # Remove duplicates
        recommended_courses = list({course.id: course for course in recommended_courses}.values())

        # Step 3: If no recommendations, fallback to top courses
        if not recommended_courses:
            recommended_courses = fetch_top_courses()

        # Return the list of recommended courses
        return jsonify([{
            "title": course.title,
            "slug": course.id,  # or use any unique identifier
            "image": course.image,
            "fee": course.fee,
            "rating": course.rating,
            "desc": course.desc  # Assuming `desc` is the correct attribute
        } for course in recommended_courses])
    
    except Exception as e:
        # Silencing the error by catching it and returning None
        print("openai exceptions sienced, here at web/apis/x_courses/x_recommend_bak.py:81")
        return jsonify({"success":False, "error": f"{e}"})
