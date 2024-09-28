from flask import Blueprint, jsonify, request, current_app
from web.models import Course

x_recommend_bp = Blueprint('x_recommend_api', __name__)

from web.extensions import openai_client

# Fetch similar courses based on OpenAI recommendation
def fetch_similar_courses_from_db(recommendation):
    query = Course.query.filter(
        (Course.title.ilike(f'%{recommendation}%')) |
        (Course.category.ilike(f'%{recommendation}%')) |
        (Course.desc.ilike(f'%{recommendation}%'))
    ).all()
    return query

def get_openai_recommendations(interactions):
    # completion = await openai_client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])
    # Construct a message list for ChatGPT
    print("interactions:", interactions)
    messages = [
        
        {"role": "system", "content": "You are a helpful assistant who recommends courses based on user interactions."},
        {"role": "user", "content": interactions }
    ]
    
    # response = openai.ChatCompletion.create(
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=200
    )
    
    recommendations = response.choices[0].message

    print("Openai-recommendations: ", recommendations)
    return recommendations
    


# Endpoint to handle user interactions and provide recommendations
from web.extensions import csrf
@x_recommend_bp.route('/recommendations', methods=['POST'])
@csrf.exempt
def get_recommendations():
    try:

        # Ensure we are within an application context
        with current_app.app_context():
            # openai.api_key = current_app.config['OPENAI_API_KEY']
            pass

        interaction = request.json.get('interaction')

        if not interaction:
            return jsonify({"error": "No interactions provided"}), 400

        print("interaction", interaction)
        
        # Step 1: Get recommendations from OpenAI
        openai_recommendations = get_openai_recommendations("what is coding")

        # Step 2: Fetch matching courses from the database
        recommended_courses = []
        for recommendation in openai_recommendations:
            similar_courses = fetch_similar_courses_from_db(recommendation)
            recommended_courses.extend(similar_courses)

        # Return the list of recommended courses
        return jsonify([{
            "title": course.name,
            "slug": course.id,  # or use any unique identifier
            "image": course.image,
            "fee": course.fee,
            "rating": course.rating,
            "desc": course.description
        } for course in recommended_courses])
    
    except Exception as e:
        # Silencing the error by catching it and returning None
        print("openai exceptions silenced, here at web/apis/x_courses/x_recommend_bak.py:81")
        return jsonify({"success":False, "error": f"{e}"})


