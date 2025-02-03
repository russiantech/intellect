# web/decorators.py
import requests
from flask import flash, redirect, request, url_for, jsonify
from functools import wraps
from flask_login import current_user
from web.models import Path, db, Course, Enrollment, Payment
from web.apis.errors import handle_response

from os import getenv
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

def confirm_email(func):
    '''Check if email has been confirmed'''
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        if current_user.is_authenticated and not current_user.verified :
            flash(f' You\'re Yet To Verify Your Account!', 'danger')
            return redirect(url_for('auth_api.unverified'))
        return func(*args, **kwargs)
    return wrapper_function

from sqlalchemy import or_, and_

def enrollment_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        slug = kwargs.get('slug')
        if slug is None:
            flash('Course ID is missing', 'error')
            return handle_response(message='Course Not Found', alert='alert-danger')

        if current_user.is_authenticated:
            course = Course.query.filter(Course.slug == slug).first()
            if course is None:
                return redirect(request.referrer or url_for('main.welcome'))

            # Check if the user is enrolled in the course directly or via a path
            enrollment = Enrollment.query.filter(
                Enrollment.user_id == current_user.id,
                Enrollment.deleted == False,
                or_(
                    Enrollment.course_id == course.id,
                    and_(
                        Enrollment.path_id.isnot(None),
                        Enrollment.path.has(Path.courses.any(id=course.id))
                    )
                )
            ).first()

            # Ensure enrollment is not None before accessing its attributes
            if enrollment is not None or current_user.is_admin_dev():
                # Check if there's a successful payment for the course or path
                successful_payment = Payment.query.filter(
                    Payment.user_id == current_user.id,
                    Payment.deleted == False,
                    Payment.tx_status == 'successful',
                    or_(
                        Payment.course_id == course.id,
                        (enrollment is not None and Payment.path_id == enrollment.path_id)  # Check if enrollment is not None
                    )
                ).first()

                if successful_payment or current_user.is_admin_dev():
                    return func(*args, **kwargs)

                return jsonify({"success": False, 'error': 'Kindly process your enrollment & payments for the course to continue.'})
            
            # return handle_response(message='You are not enrolled in this course', alert='alert-danger')
            return jsonify({"success": False, 'error': 'You are not enrolled in this course'})
        else:
            return handle_response(message='You need to log in to access this course', alert='alert-danger')

    return decorated_function
