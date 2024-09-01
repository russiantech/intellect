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

            if enrollment:
                # Check if there's a successful payment for the course or path
                successful_payment = Payment.query.filter(
                    Payment.user_id == current_user.id,
                    Payment.deleted == False,
                    Payment.tx_status == 'successful',
                    or_(
                        Payment.course_id == course.id,
                        Payment.path_id == enrollment.path_id
                    )
                ).first()

                if successful_payment:
                    return func(*args, **kwargs)

                flash('Payment is required to access this course', 'error')
                return jsonify({"success": False, 'error': 'Kindly process your enrollment & payments for the course to continue.'})
            
            flash('You are not enrolled in this course', 'error')
            return handle_response(message='You are not enrolled in this course', alert='alert-danger')
        else:
            flash('You need to log in to access this course', 'error')
            return handle_response(message='You need to log in to access this course', alert='alert-danger')

    return decorated_function


def enrollment_required_04(func):
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

            enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id, deleted=False).first()
            if enrollment:
                payments = Payment.query.filter_by(user_id=current_user.id, course_id=course.id, deleted=False).all()

                successful_payment = any(payment.tx_status == 'successful' for payment in payments)
                if successful_payment:
                    return func(*args, **kwargs)

                # pending_payments = [payment for payment in payments if payment.tx_status == 'pending' and payment.user.id == current_user.id]
                pending_payments = [payment for payment in payments if payment.tx_status == 'pending']
                for payment in pending_payments:
                    headers = {"Authorization": f"Bearer {getenv('RAVE_SECRET_KEY')}"}
                    verify_by_txref_endpoint = f"https://api.flutterwave.com/v3/transactions/{payment.tx_ref}/verify"
                    response = requests.get(verify_by_txref_endpoint, headers=headers)

                    if response.status_code == 200:
                        response_data = response.json().get('data', {})
                        if (
                            response_data.get('status') == "successful"
                            and response_data.get('amount') >= payment.tx_amount
                            and response_data.get('currency') == payment.currency
                        ):
                            payment.tx_status = response_data['status']
                            payment.tx_id = response_data['id']
                            db.session.commit()

                            enrollment = Enrollment(
                                user=current_user, user_id=current_user.id, 
                                course=payment.course, course_id=payment.course.id
                            )
                            db.session.add(enrollment)
                            db.session.commit()
                            return func(*args, **kwargs)
                        else:
                            payment.deleted = True
                            db.session.commit()
                    else:
                        payment.deleted = True
                        db.session.commit()

                flash('Payment is required to access this course', 'error')
                return jsonify({"success": False, 'error': 'Kindly process your enrollment & payments for the course to continue.'})

            else:
                flash('You are not enrolled in this course', 'error')
                return handle_response(message='You are not enrolled in this course', alert='alert-danger')
        else:
            flash('You need to log in to access this course', 'error')
            return handle_response(message='You need to log in to access this course', alert='alert-danger')

    return decorated_function

def enrollment_required_03(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        slug = kwargs.get('slug')
        if slug is None:
            flash('Course ID is missing', 'error')
            return handle_response(message='Course Not Found', alert='alert-danger')

        # Check if the current user is logged in
        if current_user.is_authenticated:
            # Retrieve the course object
            course = Course.query.filter(Course.slug == slug).first()
            if course is None:
                return redirect(request.referrer or url_for('main.welcome'))  # Redirect to home page or course catalog

            # Check if the current user is enrolled in the course
            enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id, deleted=False).first()
            if enrollment:
                # Get all payments for the course
                payments = Payment.query.filter_by(user_id=current_user.id, course_id=course.id, deleted=False).all()

                if any(payment.tx_status == 'successful' for payment in payments):
                    return func(*args, **kwargs)
            
                # Check the status of each payment
                successful_payment = None
                for payment in payments:
                    if payment.tx_status == 'successful':
                        successful_payment = payment
                        break

                if successful_payment:
                    # User is enrolled and at least one payment is successful, allow access to the route
                    return func(*args, **kwargs)
                    
                elif any(payment.tx_status == 'cancelled' for payment in payments):
                    return handle_response(message='You Cancelled Your Payment For This Course', alert='alert-danger')

                elif any(payment.tx_status == 'pending' for payment in payments):
                    #try to verify pending payments': 
                    # Make a request to verify the transaction
                    headers = {"Authorization": f"Bearer {getenv('RAVE_SECRET_KEY')}"}
                    verify_by_txref_endpoint = f"https://api.flutterwave.com/v3/transactions/{payment.tx_ref}"
                    response = requests.get(verify_by_txref_endpoint, headers=headers)
                    
                    # Check if the request was successful
                    if response.status_code == 200:
                        try:
                            response_data = response.json()
                        except ValueError:
                            #print(response.__dict__)
                            """ if 'data' not in response_data:
                                # Transaction not found, mark it for removal
                                db.session.delete(transaction) """

                            #return jsonify({'message': f'{response}, \n {response.__dict__}'}), 400
                            #return jsonify({'message': f'Invalid JSON in response {response}, {type(response)}, {response.__dict__}'}), 400
                            return redirect(request.referrer)
                        # Check if transaction data exists in the response
                        if 'data' in response_data:
                            transaction_data = response_data['data']
                            if (
                                transaction_data['status'] == "successful"
                                and transaction_data['amount'] >= payment.tx_amount
                                and transaction_data['currency'] == payment.currency
                                ):
                                # Success! Confirm the customer's payment
                                payment.tx_status = transaction_data['status']
                                payment.tx_id = transaction_data['id']
                                # Create enrollment record for the user and the course
                                enrollment = Enrollment(
                                    user=current_user, user_id=current_user.id, 
                                    course=payment.course, course_id=payment.course.id
                                )
                                db.session.add(enrollment)
                                db.session.commit()
                                return func(*args, **kwargs)
                            else:
                                # Inform the customer their payment was unsuccessful
                                payment.deleted = True
                                db.session.commit()
                                return jsonify({"success":False, 'error': 'Transaction Verification Failed', 'data': transaction_data}), 400
                        else:
                            payment.deleted = True
                            db.session.commit()
                            return jsonify({"success":False, 'error': 'No transaction data found'}), 400
                    else:
                        payment.deleted = True
                        db.session.commit()
                        return jsonify({"success":False, 'error': 'Failed to verify transaction'}), 400
                
                else:
                    flash('Payment is required to access this course', 'error')
                    return jsonify({"success":False, 'error': 'Kindly process your enrollment & payments for the course to continue.'})
            else:
                flash('You are not enrolled in this course', 'error')
                return handle_response(message='You are not enrolled in this course', alert='alert-danger')
        else:
            flash('You need to log in to access this course', 'error')
            return handle_response(message='You need to log in to access this course', alert='alert-danger')

    return decorated_function

""" 
For this one, the issue is that, at the querying for payment(with .first()), 
if there's any pending/cancelled payment for a course before
the successful payments, it matches from there and redirects as if the user did not later make/verify a successful transaction.
 """
 
def enrollment_required_bak(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        slug = kwargs.get('slug')
        if slug is None:
            flash('Course ID is missing', 'error')
            return handle_response(message='Course Not Found', alert='alert-danger')

        # Check if the current user is logged in
        if current_user.is_authenticated:
            # Retrieve the course object
            course = Course.query.filter(Course.slug == slug).first()
            if course is None:
                return redirect(request.referrer or url_for('main.index'))  # Redirect to home page or course catalog

            # Check if the current user is enrolled in the course
            enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id, deleted=False).first()
            if enrollment:
                # Check if the user has made a payment for the course
                payment = Payment.query.filter_by(user_id=current_user.id, course_id=course.id, deleted=False).first()
                if payment and payment.tx_status == 'successful': 
                    # User is enrolled and payment is successful, allow access to the route
                    return func(*args, **kwargs)
                
                elif payment and payment.tx_status == 'cancelled': 
                    return handle_response(
                        message='You Cancelled Your Payment For This Course', alert='alert-danger')
                
                elif payment and payment.tx_status == 'pending': 
                    # Make a request to verify the transaction
                    headers = {"Authorization": f"Bearer {getenv('RAVE_SECRET_KEY')}"}
                    verify_by_txref_endpoint = f"https://api.flutterwave.com/v3/transactions/{payment.tx_ref}"
                    response = requests.get(verify_by_txref_endpoint, headers=headers)
                    
                    # Check if the request was successful
                    if response.status_code == 200:
                        try:
                            response_data = response.json()
                        except ValueError:
                            #print(response.__dict__)
                            """ if 'data' not in response_data:
                                # Transaction not found, mark it for removal
                                db.session.delete(transaction) """

                            #return jsonify({'message': f'{response}, \n {response.__dict__}'}), 400
                            #return jsonify({'message': f'Invalid JSON in response {response}, {type(response)}, {response.__dict__}'}), 400
                            return redirect(request.referrer)
                        # Check if transaction data exists in the response
                        if 'data' in response_data:
                            transaction_data = response_data['data']
                            if (
                                transaction_data['status'] == "successful"
                                and transaction_data['amount'] >= payment.tx_amount
                                and transaction_data['currency'] == payment.currency
                            ):
                                # Success! Confirm the customer's payment
                                payment.tx_status = transaction_data['status']
                                payment.tx_id = transaction_data['id']
                                # Create enrollment record for the user and the course
                                enrollment = Enrollment(
                                    user=current_user, user_id=current_user.id, 
                                    course=payment.course, course_id=payment.course.id
                                )
                                db.session.add(enrollment)
                                db.session.commit()
                                return func(*args, **kwargs)
                            else:
                                # Inform the customer their payment was unsuccessful
                                payment.deleted = True
                                db.session.commit()
                                return jsonify({'message': 'Transaction Verification Failed', 'data': transaction_data}), 400
                        else:
                            payment.deleted = True
                            db.session.commit()
                            return jsonify({'message': 'No transaction data found'}), 400
                    else:
                        payment.deleted = True
                        db.session.commit()
                        return jsonify({'message': 'Failed to verify transaction'}), 400
                else:
                    flash('Payment is required to access this course', 'error')
                    return handle_response(
                        message='Payment is required to access this course', 
                        alert='alert-danger')
            else:
                flash('You are not enrolled in this course', 'error')
                return handle_response(message='You are not enrolled in this course', alert='alert-danger')
        else:
            flash('You need to log in to access this course', 'error')
            return handle_response(message='You need to log in to access this course', alert='alert-danger')

    return decorated_function

def enrollment_required_02(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        slug = kwargs.get('slug')
        if slug is None:
            flash('Course ID is missing', 'error')
            return redirect(url_for('home'))  # Redirect to home page or course catalog

        # Check if the current user is logged in
        if current_user.is_authenticated:
            # Access the enrolled courses directly from the current user object
            enrolled_courses = current_user.courses.all()
            # Check if the requested course is among the enrolled courses
            if any(course.id == slug for course in enrolled_courses):
                # Access the enrollment for the specified course directly from the current user object
                enrollment = next((enrollment for enrollment in current_user.enrollments if enrollment.slug == slug), None)
                if enrollment:
                    # Access the payment associated with the enrollment directly from the current user object
                    payment = enrollment.payment
                    if payment and payment.status == 'successful':
                        # User is enrolled and payment is successful, allow access to the route
                        return func(*args, **kwargs)
                    else:
                        flash('Payment is required to access this course', 'error')
                else:
                    flash('You are not enrolled in this course', 'error')
            else:
                flash('You are not enrolled in this course', 'error')
        else:
            flash('You need to log in to access this course', 'error')

        return redirect(url_for('home'))  # Redirect to home page or course catalog

    return decorated_function


