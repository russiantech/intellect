from flask import Blueprint, jsonify, request, current_app
from web.models import Course

import openai
# openai.api_key = current_app.config['OPENAI_API_KEY']

x_recommend_bp = Blueprint('x_recommend_api', __name__)


from openai import OpenAI
openai_client = OpenAI()

completion = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)
print("Openai-recommendations: ", completion.choices[0].message)


# Fetch similar courses based on OpenAI recommendation
def fetch_similar_courses_from_db(recommendation):
    query = Course.query.filter(
        (Course.title.ilike(f'%{recommendation}%')) |
        (Course.category.ilike(f'%{recommendation}%')) |
        (Course.desc.ilike(f'%{recommendation}%'))
    ).all()
    return query

# Generate recommendations using OpenAI based on user interactions
def get_openai_recommendations0(interactions):
    prompt = "Based on the following user interactions, recommend courses: \n"
    for interaction in interactions:
        # prompt += f"{interaction['action']} {interaction['course_title']} {interaction['count']} times.\n"
        prompt += f"{interaction.get('action', 'view')} {interaction.get('course_title', 'tech-courses')} {interaction.get('count', 1)} times.\n"
    
    # response = openai.Completion.create(
    response = openai.chat.completions.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    
    recommendations = response.choices[0].text.strip().split("\n")
    return recommendations

def get_openai_recommendations(interactions):
    # completion = await openai_client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])
    # Construct a message list for ChatGPT
    messages = [
        {"role": "system", "content": "You are a helpful assistant who recommends courses based on user interactions."},
        {"role": "user", "content": "Based on the following user interactions, recommend courses:"}
    ]
    
    for interaction in interactions:
        course = Course.query.get(interaction['course_id'])
        course_name = course.title if course else 'Untitled Course'
        messages.append({"role": "user", "content": f"{interaction['action']} {course_name} {interaction['count']} times."})
    
    # response = openai.ChatCompletion.create(
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # You can use gpt-4 or another model as well
        # model="text-davinci-003",
        messages=messages,
        max_tokens=150
    )
    
    recommendations = response['choices'][0]['message']['content'].strip().split("\n")

    # Print top 5 recommendations
    print("Top 5 Recommendations:")
    for i, recommendation in enumerate(recommendations[:5]):
        print(f"{i+1}. {recommendation}")
        return recommendation

    return recommendations


# Endpoint to handle user interactions and provide recommendations
from web.extensions import csrf
@x_recommend_bp.route('/recommendations', methods=['POST'])
@csrf.exempt
def get_recommendations():

    # Ensure we are within an application context
    with current_app.app_context():
        openai.api_key = current_app.config['OPENAI_API_KEY']

    interactions = request.json.get('interactions', [])
    print('interactions:', interactions)
    if not interactions:
        return jsonify({"error": "No interactions provided"}), 400

    # Step 1: Get recommendations from OpenAI
    openai_recommendations = get_openai_recommendations(interactions)

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

# Initialize the database (run this once)
""" @app.before_first_request
def create_tables():
    db.create_all()
 """
