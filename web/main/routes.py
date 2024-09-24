from flask import jsonify, render_template, Blueprint, request, url_for
from flask_login import current_user, login_required

from web.utils.decorators import enrollment_required

from web.models import db, Brand, User, Course, Topic, Enrollment

main = Blueprint('main', __name__)

@main.route('/explore')
@main.route('/welcome/<int:offset>', methods=['post', 'get'])
@main.route('/welcome', methods=['post', 'get'])
def index(v=None):

    page = request.args.get('page', 1, type=int)

    match v:
        case 'latest':
            course = Course.query.order_by(Course.created.desc()).paginate(page=page, per_page=8)
        case 'oldest':
            course = Course.query.order_by(Course.created.asc()).paginate(page=page, per_page=8)
        case 'asc':
            course = Course.query.order_by(Course.title.asc()).paginate(page=page, per_page=8)
        case 'desc':
            course = Course.query.order_by(Course.title.desc()).paginate(page=page, per_page=8)
        case 'cat':
            cat = v.cat
            course = Course.query.filter(Course.cat.in_([c for c in cat]) ).all()
        case 'time':
            time = v.time
            course = Course.query.filter(Course.duration.in_([ t for t in time]) ).all()
        case 'price':
            min = v.min
            max = v.max
            course = Course.query.filter(Course.price >= min).filter(Course.price <= max) or \
                Course.query.filter(Course.price.in_(range(min, max)) ).all()
        case 'kword':
            kword = v.kword
            course = Course.query.msearch(kword, fields=['title','desc'] , limit=8)
        case 'rate':
            rate = v.rate
            course = Course.query.filter(Course.rating >= rate).all()
        case 'more':
            course = Course.query.order_by(Course.id.asc()).offset(5).all()
        case _:
            all = Course.query.all()
            course = all[0 : 16 ]
            total = len(all)
        
    brand = Brand.query.filter_by(id=2).first()

    context = { 
        'brand': brand, 
        'course': course, 
        'total' : total,
        'time' : "duration_choice" }

    return render_template("welcome/welcome.html", **context)

@main.route("/us")
def us():
    brand = Brand.query.filter_by(id=2).first()
    support_amount = "30, 40, 50, 70, 80, 90, 100, 200, 300, 400, 500"
    support_interval = "daily, weekly, monthly, quarterly, yearly"
    context = {
        "brand":brand, 
        "title" :'Us . Intellect',
        "support_amount" : support_amount, 
        "support_interval" : support_interval, 
    }
    return render_template('welcome/us.html', **context)

@main.route("/us-x")
def us_x():
    brand = Brand.query.filter_by(id=2).first()
    support_amount = "30, 40, 50, 70, 80, 90, 100, 200, 300, 400, 500"
    support_interval = "daily, weekly, monthly, quarterly, yearly"
    context = {
        "brand":brand, 
        "title" :'Us . Intellect',
        "support_amount" : support_amount, 
        "support_interval" : support_interval, 
    }
    return render_template('welcome/us_x.html', **context)

 
@main.route("/")
@login_required
#@confirm_email
def user():

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
        serialized_course['percent_complete'] = completion_percentage

        # Append the serialized course to the response data
        response_data.append(serialized_course)

    # Return the response as JSON
    progress_data = response_data
    #print(progress_data)
    context = {
        'progress_data': progress_data
    }

    return render_template('index.html', **context )

#-> Preview Here
@main.route('/prev_/<string:slug>')
def prev_(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()
    course.views += 1
    db.session.commit()

    topiq = Topic.query.filter(Topic.course_id == course.id).first()

    #return f'{course.__dict__}'

    context = {
        'course': course,
        'topiq': topiq.title if topiq else '0-topic',
        #'data': course.__dict__  # Convert Course object to a dictionary
        'data': test_course.course_data  
    }
    #print(context['data'])
    return render_template('courses/prev.html', **context)

@main.route('/learn_/<string:slug>')
def learn_(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()
    _chapt = [c for c in course.lessons]
    _topiq = [ t for t in course.topics]
    context = {
        '_chapt': _chapt, '_topic':_topiq,
        'data': course,
    }

    # return render_template("courses/learn3.html", **context)
    return render_template("courses/material.html", course=course, **context)
    # return render_template("courses/prevv.html", course=course, **context)

@main.route("/blog")
def blog():
    return render_template('blog.html')

@main.route('/school')
@login_required
#@confirm_email
def school():
    return render_template("school.html")

#quiz
@main.route('/quiz')
@login_required
#@confirm_email
def quiz():
    return render_template("quiz/quiz.html")
    
@main.route('/qdetail', defaults={'one':'one'})
@main.route('/qdetail/<string:one>', defaults={'one':'one'})
@login_required
#@confirm_email
def qdetails(one):
    return render_template("quiz/qdetail.html")

@main.route('/qresult')
@login_required
#@confirm_email
def qresult():
    return render_template("quiz/qresult.html")

#path
@main.route('/paths')
@login_required
#@confirm_email
def path():
    return render_template("path/path.html")

@main.route('/path', defaults={'one':'one'})
@main.route('/path-of/<string:coding>', defaults={'coding':'coding'})
def path_of():
    return render_template("path/path-of.html")


#instructors
@main.route('/tutors')
@login_required
#@confirm_email
def tutor_list():
    return render_template("instructor/tutors.html", tutors = 't')

@main.route('/tutor', defaults={'t':'t'})
@main.route('/tutor/<string:t>', defaults={'t':'t'})
@login_required
#@confirm_email
def tut(t):
    return render_template("instructor/tutor.html", tutor = tutor.info )

@main.route('/play')
@login_required
#@confirm_email
def player():
    return render_template("misc/play.html")

@main.route('/materi')
@login_required
#@confirm_email
def materi():
    return render_template("misc/material.html")

@main.route('/syllabus')
@login_required
#@confirm_email
def syllabus():
    return render_template("misc/syllabus.html")

@main.route('/../json/search.json')
@main.route('/json/search.json')
def search():
    r = [
    {
        "title": "settings",
        "url": f"/{current_user.username}/update" if current_user.is_authenticated else url_for('auth_api.signin')
    },
    {
        "title": "dashboards > elearning",
        "url": "/"
    },
    {
        "title": "dashboards > School",
        "url": "/school"
    },
    ]
  
    c = Course.query.all() 
    return jsonify([ { 'label': c.title, 'url': url_for('main.prev', slug=str(c.slug) ) } for c in c] ) 

""" ========================================================================== """

# Actual learning interface
#-> Preview Here
@main.route('/prev/<string:slug>')
def prev(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()
    course.views += 1
    db.session.commit()

    return render_template('xcourse/prev.html')

@main.route('/learn/<string:slug>')
@login_required
# @enrollment_required
def learn(slug):
    return render_template("xcourse/learn.html")

# Course insertion interface
@main.route('/x-insert')
def x_insert():
    return render_template("xcourse/x_insert.html")

# Course update interface
@main.route('/x-update')
def x_update():
    return render_template("xcourse/x_update.html")

# Lesson insertion interface
@main.route('/x-insert/lesson')
def x_insert_lesson():
    return render_template("xcourse/x_insert_lesson.html")

# Lesson update interface
@main.route('/x-update/lesson')
def x_update_lesson():
    return render_template("xcourse/x_update_lesson.html")

# Topic insertion interface
@main.route('/x-insert/topic')
def x_insert_topic():
    return render_template("xcourse/x_insert_topic.html")

# Topic update interface
@main.route('/x-update/topic')
def x_update_topic():
    return render_template("xcourse/x_update_topic.html")

# Path insert interface
@main.route('/x-insert/path')
def x_insert_path():
    return render_template("xcourse/x_insert_path.html")

# Topic update interface
@main.route('/x-update/path')
def x_update_path():
    return render_template("xcourse/x_update_path.html")
