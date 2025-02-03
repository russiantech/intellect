import secrets
import traceback, requests
from flask_login import current_user, login_required
from flask import current_app, jsonify, redirect, render_template, request, Blueprint, url_for
from web.models import Path, db, User, Payment, Course, Enrollment
from web.apis.make_slug import generate_random_id
from web.apis.errors import handle_response
from web.extensions import csrf
from requests.exceptions import ConnectionError, Timeout, RequestException

# from dotenv import load_dotenv
# Load environment variables from .env file
# load_dotenv()

pay = Blueprint('pay', __name__)

@pay.route('/init-payment/<string:slug>', methods=['POST', 'GET'])
@csrf.exempt
# @login_required
def init_payment(slug):
    try:

        # Check if the slug is for a course or a path
        course = Course.query.filter(Course.slug == slug).first()
        path = Path.query.filter(Path.slug == slug).first()

        if not course and not path:
            return handle_response(message="Course or Path Not Found", alert='alert-danger'), 404

        # Determine payment details
        if course:
            item_title = course.title
            amount = course.fee or 100
        elif path:
            item_title = path.title
            amount = path.fee or 100
        
        if not current_user.is_authenticated:
            return jsonify({"success": False, "error": f"Kindly sign-in to get enrolled into this {item_title or item_title}.", "redirect_url": url_for("auth_api.signin")}), 200


        # Prepare payment payload
        url = "https://api.flutterwave.com/v3/payments"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {current_app.config['RAVE_SECRET_KEY']}",
            "Content-Type": "application/json"
        }

        payload = {
            "tx_ref": f"-tx-techa-{generate_random_id(k=5)}",
            "amount": amount,
            "currency": "USD",
            "redirect_url": f"{request.url_root}payment-callback",
            "customer": {
                "email": current_user.email if current_user.is_authenticated else request.args.get('email', 'hello@intellect.com'),
                "phonenumber": current_user.phone if current_user.is_authenticated and current_user.phone else None,
                "name": current_user.name or current_user.username if current_user.is_authenticated else None
            },
            "payment_options": "card, ussd, banktransfer, credit, mobilemoneyghana",
            "customizations": {
                "title": f"{item_title} . Intellect",
                "logo": url_for('static', filename='img/favicon/favicon.png', _external=True)
            }
        }

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json() if response else {}
        payment_link = response_data.get("data", {}).get("link")

        if not payment_link:
            return handle_response(message="Failed to retrieve payment link", alert='alert-danger')

        # Save transaction details to the database
        payment_data = {
            'currency': payload['currency'],
            'tx_amount': payload['amount'],
            'tx_ref': payload['tx_ref'],
            'tx_status': 'pending',
            'provider': 'FlutterWave',
            'tx_id': None,
            'user_id': current_user.id,
            'course_id': course.id if course else None,
            'path_id': path.id if path else None
        }
        new_payment = Payment(**payment_data)
        db.session.add(new_payment)
        db.session.commit()

        # Redirect the user to the payment link
        # return redirect(payment_link)
        return jsonify({"success": True, "message": "Payment secured by flutterwave, continue in a moment.", "redirect_url": payment_link}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 200

@pay.route('/init-payment/<string:course_slug_1>', methods=['POST', 'GET'])
@csrf.exempt
@login_required
def init_payment_1(course_slug):
    try:

        # Retrieve course information from the database
        #course = Course.query.get(course_id)
        course = Course.query.filter(Course.slug == course_slug).first()
        if not course:
            return handle_response(message="Course Not Found", alert='alert-danger'), 404

        # Make a POST request to get the payment link
        url = "https://api.flutterwave.com/v3/payments"
        headers = {
            "accept": "application/json",
            # "Authorization": f"Bearer {getenv('RAVE_SECRET_KEY')}",
            "Authorization": f"Bearer {current_app.config['RAVE_SECRET_KEY']}", # working out of request context if used outside a route
            "Content-Type": "application/json"
        }

        # Prepare payment payload
        payload = {
            "tx_ref": f"-tx-techa-{generate_random_id(k=5)}",
            "amount": course.fee or 100,
            "currency": "USD",
            "redirect_url": f"{request.url_root}payment-callback",
            "customer": {
                "email": current_user.email if current_user.is_authenticated else request.args.get('email', 'hello@intellect.com'),
                "phonenumber": current_user.phone if current_user.is_authenticated and current_user.phone else None,
                "name": current_user.name or current_user.username if current_user.is_authenticated else None
            },
            "payment_options": "card, ussd, banktransfer, credit, mobilemoneyghana",
            "customizations": {
                "title": f"{course.title} . Intellect",
                "logo": url_for('static', filename='img/favicon/favicon.png', _external=True)
            }
        }

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json() if response else { }
        payment_link = response_data.get("data", {}).get("link")
        # print(payment_link, headers.get("Authorization"), response_data)
        if not payment_link:
            # print(payment_link, headers.get("Authorization"), response_data)
            return handle_response(message="Failed to retrieve payment link", alert='alert-danger')

        # Save transaction details to the database
        payment_data = {
            'currency': payload['currency'],
            'tx_amount': payload['amount'],
            'tx_ref': payload['tx_ref'],
            'tx_status': 'pending',
            'provider': 'FlutterWave',
            'tx_id': None,
            'user_id': current_user.id,
            'course_id': course.id
        }
        new_payment = Payment(**payment_data)
        db.session.add(new_payment)
        db.session.commit()

        # Redirect the user to the payment link
        return redirect(payment_link)

    except Exception as e:
        traceback.print_exc()
        return handle_response(message=str(e), alert='alert-danger'), 500

def path_enrollment(user, path_id):
    path = Path.query.get(path_id)
    if path:
        for course in path.courses:
            enrollment = Enrollment(
                user_id=user.id,
                course_id=course.id,
                path_id=path.id
            )
            db.session.add(enrollment)
        db.session.commit()
        
        # Redirect to the first course in the path
        first_course = path.courses[0]
        return redirect(url_for('main.learn', slug=first_course.slug))
    
    return jsonify({"success":False,'error': f'Path {path_id} not available.'})

def init_payment(slug):
    try:
        # Check if the slug is for a course or a path
        course = Course.query.filter(Course.slug == slug).first()
        path = Path.query.filter(Path.slug == slug).first()

        if not course and not path:
            return jsonify({"success": False, "error": "Course or Path Not Found"}), 404

        # Determine payment details
        if course:
            item_title = course.title
            amount = course.fee or 100
        elif path:
            item_title = path.title
            amount = path.fee or 100

        # Check if this is a subscription payment
        subscription = request.args.get('subscription', None)  # Assuming subscription is passed as a query param
        is_subscription = True if subscription else False

        # Prepare payment payload
        url = "https://api.flutterwave.com/v3/payments"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {current_app.config['RAVE_SECRET_KEY']}",
            "Content-Type": "application/json"
        }

        payload = {
            "tx_ref": f"-tx-techa-{generate_random_id(k=5)}",
            "amount": amount,
            "currency": "USD",
            "redirect_url": f"{request.url_root}payment-callback",
            "customer": {
                "email": current_user.email if current_user.is_authenticated else request.args.get('email', 'hello@intellect.com'),
                "phonenumber": current_user.phone if current_user.is_authenticated and current_user.phone else None,
                "name": current_user.name or current_user.username if current_user.is_authenticated else None
            },
            "payment_options": "card, ussd, banktransfer, credit, mobilemoneyghana",
            "customizations": {
                "title": f"{item_title} . Intellect",
                "logo": url_for('static', filename='img/favicon/favicon.png', _external=True)
            }
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json() if response else {}

            payment_link = response_data.get("data", {}).get("link")
            if not payment_link:
                return jsonify({"success": False, "error": "Failed to retrieve payment link"}), 500

            # Save transaction details to the database
            payment_data = {
                'currency': payload['currency'],
                'tx_amount': payload['amount'],
                'tx_ref': payload['tx_ref'],
                'tx_status': 'pending',
                'provider': 'FlutterWave',
                'tx_id': None,
                'user_id': current_user.id,
                'course_id': course.id if course else None,
                'path_id': path.id if path else None,
                'is_subscription': is_subscription  # Save the subscription status
            }
            new_payment = Payment(**payment_data)
            db.session.add(new_payment)
            db.session.commit()

            # Return the payment link for redirection
            return jsonify({"success": True, "message": "Continue to pay securely..", "redirect_url": payment_link}), 200

        except ConnectionError:
            return jsonify({"success": False, "error": "No internet connection. Please check your network and try again."}), 500

        except Timeout:
            return jsonify({"success": False, "error": "The request timed out. Please try again later."}), 500

        except RequestException as e:
            return jsonify({"success": False, "error": f"An error occurred: {str(e)}"}), 500
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@pay.route('/init-support-pay', methods=['POST'])
@csrf.exempt
def support_pay():
    try:
        if request.method == "POST":
            amount = request.form.get('amount', 0).strip()
            email = request.form.get('email', current_user.email if current_user.is_authenticated else None)
            subscription = request.form.get('subscription', None)
            currency = "USD"  # Set your default currency here

            if not email:
                return jsonify({"success": False, "error": "A valid email address is required for receipt of payment"})

            if not amount.isdigit() or int(amount) <= 0:
                return jsonify({"success": False, "error": "Kindly provide an amount > 0 to continue"})

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {current_app.config['RAVE_SECRET_KEY']}",
                "Content-Type": "application/json"
            }

            payload = {
                "tx_ref": f"Techa-{generate_random_id(k=5)}",
                "amount": int(amount),
                "currency": currency,  # Ensure this matches the currency in the payment plan
                "redirect_url": f"{request.url_root}payment-callback",
                "customer": {
                    "email": email,
                    "phonenumber": current_user.phone if current_user.is_authenticated and current_user.phone else None,
                    "name": current_user.name or current_user.username if current_user.is_authenticated else email
                },
                "payment_options": "card, ussd, banktransfer, credit, mobilemoneyghana",
                "customizations": {
                    "title": "Support . Intellect",
                    "logo": url_for('static', filename='img/favicon/favicon.png', _external=True)
                }
            }

            from requests.exceptions import ConnectionError, Timeout, RequestException
            try:
                if subscription:
                    # Step 1: Create the payment plan with the same currency
                    plan_payload = {
                        "amount": payload['amount'],
                        "name": payload['customizations']["title"],
                        "interval": subscription,
                        "currency": currency  # Match the currency here as well
                    }
                    
                    plan_response = requests.post("https://api.flutterwave.com/v3/payment-plans", json=plan_payload, headers=headers)
                    plan_data = plan_response.json().get('data', {})

                    if plan_response.status_code != 200 or not plan_data.get('id'):
                        return jsonify({"success": False, "error": "Failed to create payment plan"})

                    # Step 2: Update the payload with the plan ID and initiate payment
                    payload['payment_plan'] = plan_data['id']
                    payment_response = requests.post("https://api.flutterwave.com/v3/payments", json=payload, headers=headers)
                else:
                    payment_response = requests.post("https://api.flutterwave.com/v3/payments", json=payload, headers=headers)

                payment_data = payment_response.json() if payment_response else {}

                payment_link = payment_data.get("data", {}).get("link")
                if not payment_link:
                    return jsonify({"success": False, "error": "Failed to retrieve payment link"})

                user = User.query.filter_by(email=email).first()
                if not user:
                    user_data = {
                        'username': email,
                        'email': email,
                    }
                    new_user = User(**user_data)
                    new_user.set_password(secrets.token_urlsafe(5))
                    db.session.add(new_user)

                    from sqlalchemy.exc import IntegrityError
                    try:
                        db.session.commit()
                        user_id = new_user.id
                    except IntegrityError:
                        db.session.rollback()
                        user = User.query.filter_by(email=email).first()
                        user_id = user.id
                else:
                    user_id = user.id

                payment_data = {
                    'currency': payload['currency'],
                    'tx_amount': payload['amount'],
                    'tx_ref': payload['tx_ref'],
                    'tx_status': 'pending',
                    'provider': 'flutterwave',
                    'tx_id': None,
                    'user_id': user_id,
                    'course_id': None
                }
                new_payment = Payment(**payment_data)
                db.session.add(new_payment)
                db.session.commit()

                return jsonify({"success": True, "message": "Continue to pay securely..", "redirect_url": payment_link}), 200

            except ConnectionError:
                return jsonify({"success": False, "error": "No internet connection. pls check your network and try again."}), 500

            except Timeout:
                return jsonify({"success": False, "error": "The request timed out. Please try again later."}), 500

            except RequestException as e:
                return jsonify({"success": False, "error": f"An error occurred: {str(e)}"}), 500

        return jsonify({"success": False, "error": "Invalid request method"}), 405

    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"success": False, "error": str(e)}), 500

@pay.route('/init-support-pay-1', methods=['POST'])
@csrf.exempt
def support_pay_1():
    try:
        if request.method == "POST":
            # Get the amount, email, and subscription details from the form
            amount = request.form.get('amount', 0).strip()
            email = request.form.get('email', current_user.email if current_user.is_authenticated else None)
            subscription = request.form.get('subscription', None)

            if not email:
                return jsonify({"success": False, "error": "A valid email address is required for receipt of payment"})

            if not amount.isdigit() or int(amount) <= 0:
                return jsonify({"success": False, "error": "Kindly provide an amount > 0 to continue"})

            # Prepare request details
            url = "https://api.flutterwave.com/v3/payments"
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {current_app.config['RAVE_SECRET_KEY']}",
                "Content-Type": "application/json"
            }

            # Prepare payment payload
            payload = {
                "tx_ref": f"Techa-{generate_random_id(k=5)}",
                "amount": int(amount),
                "currency": "USD",
                "redirect_url": f"{request.url_root}payment-callback",
                "customer": {
                    "email": email,
                    "phonenumber": current_user.phone if current_user.is_authenticated and current_user.phone else None,
                    "name": current_user.name or current_user.username if current_user.is_authenticated else email
                },
                "payment_options": "card, ussd, banktransfer, credit, mobilemoneyghana",
                "customizations": {
                    "title": "Support . Intellect",
                    "logo": url_for('static', filename='img/favicon/favicon.png', _external=True)
                }
            }

            from requests.exceptions import ConnectionError, Timeout, RequestException
            try:
                # Check if it's a subscription payment
                if subscription:
                    subscription_payload = {
                        "amount": payload['amount'],
                        "name": payload['customizations']["title"],
                        "interval": subscription,
                    }
                    response = requests.post("https://api.flutterwave.com/v3/payment-plans", json=subscription_payload, headers=headers)
                else:
                    response = requests.post(url, json=payload, headers=headers)

                response_data = response.json() if response else {}
                print("response_data", response_data)
                # Handle payment link or errors
                payment_link = response_data.get("data", {}).get("link")
                if not payment_link:
                    return jsonify({"success": False, "error": "Failed to retrieve payment link"})

                # Check if user exists with the provided email
                user = User.query.filter_by(email=email).first()
                if not user:
                    # Create a new user
                    user_data = {
                        'username': email,
                        'email': email,
                    }
                    new_user = User(**user_data)
                    new_user.set_password(secrets.token_urlsafe(5))
                    db.session.add(new_user)

                    from sqlalchemy.exc import IntegrityError
                    try:
                        db.session.commit()
                        user_id = new_user.id
                    except IntegrityError:
                        db.session.rollback()
                        user = User.query.filter_by(email=email).first()
                        user_id = user.id
                else:
                    user_id = user.id

                # Save transaction details to the database
                payment_data = {
                    'currency': payload['currency'],
                    'tx_amount': payload['amount'],
                    'tx_ref': payload['tx_ref'],
                    'tx_status': 'pending',
                    'provider': 'flutterwave',
                    'tx_id': None,
                    'user_id': user_id,
                    'course_id': None
                }
                new_payment = Payment(**payment_data)
                db.session.add(new_payment)
                db.session.commit()

                # Redirect the user to the payment link
                return jsonify({"success": True, "message": "Continue to pay securely..", "redirect_url": payment_link}), 200

            except ConnectionError:
                return jsonify({"success": False, "error": "No internet connection. pls check your network and try again."}), 500

            except Timeout:
                return jsonify({"success": False, "error": "The request timed out. Please try again later."}), 500

            except RequestException as e:
                return jsonify({"success": False, "error": f"An error occurred: {str(e)}"}), 500

        return jsonify({"success": False, "error": "Invalid request method"}), 405

    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"success": False, "error": str(e)}), 500

@pay.route('/init-support-pay-0', methods=['POST'])
@csrf.exempt
def support_pay_0():
    try:
        if request.method == "POST":
            # Get the amount, email, and subscription details from the form
            # amount = int(request.form.get('amount', 0))
            amount = request.form.get('amount', 0).strip()
            email = request.form.get('email', current_user.email if current_user.is_authenticated else None)
            subscription = request.form.get('subscription', None)

            if not email:
                return jsonify({"success": False, "error": "A valid email address is required for receipt of payment"})

            # if not amount or amount <= 0 :
            if not amount.isdigit() or int(amount) <= 0:
                return jsonify({"success": False, "error": "Kindly provide an amount > 0 to continue"})
    
            # Prepare request details
            url = "https://api.flutterwave.com/v3/payments"
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {current_app.config['RAVE_SECRET_KEY']}",
                "Content-Type": "application/json"
            }

            # Prepare payment payload
            payload = {
                "tx_ref": f"Techa-{generate_random_id(k=5)}",
                "amount": int(amount),
                "currency": "USD",
                # "redirect_url": f"{request.url_root}",
                "redirect_url": f"{request.url_root}payment-callback",
                "customer": {
                    "email": email,
                    "phonenumber": current_user.phone if current_user.is_authenticated and current_user.phone else None,
                    "name": current_user.name or current_user.username if current_user.is_authenticated else email
                },
                "payment_options": "card, ussd, banktransfer, credit, mobilemoneyghana",
                "customizations": {
                    "title": "Support . Intellect",
                    "logo": url_for('static', filename='img/favicon/favicon.png', _external=True)
                }
            }

            from requests.exceptions import ConnectionError, Timeout, RequestException
            try:
                # Check if it's a subscription payment
                # interval = request.form.get('interval', None)
                if subscription:
                    url = "https://api.flutterwave.com/v3/payment-plans"
                    payload = {
                        "amount": payload['amount'],
                        "name": payload['customizations']["title"],
                        "interval": subscription,
                        # "duration": request.form.get('duration', 48)
                    }
                    response = requests.post(url, json=payload, headers=headers)
                else:
                    response = requests.post(url, json=payload, headers=headers)

                response_data = response.json() if response else {}

                # Handle payment link or errors
                payment_link = response_data.get("data", {}).get("link")
                if not payment_link:
                    # print(response_data)
                    return jsonify({"success": False, "error": "Failed to retrieve payment link"})

                # Check if user exists with the provided email
                user = User.query.filter_by(email=email).first()
                if not user:
                    # Create a new user
                    user_data = {
                        'username': email,
                        'email': email,
                    }
                    new_user = User(**user_data)
                    new_user.set_password(secrets.token_urlsafe(5))
                    db.session.add(new_user)

                    from sqlalchemy.exc import IntegrityError
                    try:
                        db.session.commit()
                        user_id = new_user.id
                    except IntegrityError:
                        db.session.rollback()
                        # Fetch the user again if IntegrityError is raised due to race condition
                        user = User.query.filter_by(email=email).first()
                        user_id = user.id
                else:
                    user_id = user.id

                # Save transaction details to the database
                payment_data = {
                    'currency': payload['currency'],
                    'tx_amount': payload['amount'],
                    'tx_ref': payload['tx_ref'],
                    'tx_status': 'pending',
                    'provider': 'flutterwave',
                    'tx_id': None,
                    'user_id': user_id,
                    'course_id': None
                }
                new_payment = Payment(**payment_data)
                db.session.add(new_payment)
                db.session.commit()

                # Redirect the user to the payment link
                return jsonify({"success": True, "message": "Continue to pay securely..", "redirect_url": payment_link}), 200

            
            except ConnectionError:
                # Handle the case where the user is not connected to the internet
                return jsonify({"success": False, "error": "No internet connection. pls check your network and try again."}), 500

            except Timeout:
                # Handle request timeout
                return jsonify({"success": False, "error": "The request timed out. Please try again later."}), 500

            except RequestException as e:
                # Handle other types of request exceptions
                return jsonify({"success": False, "error": f"An error occurred: {str(e)}"}), 500

        return jsonify({"success": False, "error": "Invalid request method"}), 405

    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"success": False, "error": str(e)}), 500

@pay.route('/payment-callback', methods=['GET'])
@csrf.exempt
def payment_callback():
    try:
        status = request.args.get('status')
        transaction_id = request.args.get('transaction_id')
        tx_ref = request.args.get('tx_ref')

        payment = Payment.query.filter(Payment.tx_ref == tx_ref).first()

        if not payment:
            return jsonify({'error': 'Payment record not found'}), 404

        if status == 'successful':
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {current_app.config['RAVE_SECRET_KEY']}",
                "Content-Type": "application/json"
            }

            verify_endpoint = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
            response = requests.get(verify_endpoint, headers=headers)

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

                    if payment.path_id and payment.user:
                        # Handle enrollment for all courses under the path
                        for course in payment.path.courses:
                            # Check if the user is already enrolled in the course
                            existing_enrollment = Enrollment.query.filter_by(
                                user_id=payment.user.id,
                                course_id=course.id,
                                deleted=False
                            ).first()

                            if not existing_enrollment:
                                enrollment = Enrollment(
                                    user=payment.user, user_id=payment.user.id,
                                    course=course, course_id=course.id
                                )
                                db.session.add(enrollment)
                                db.session.commit()

                        return redirect(url_for('main.learn', slug=payment.path.courses[0].slug))

                    elif payment.course_id and payment.user:
                        # Check if the user is already enrolled in the course
                        existing_enrollment = Enrollment.query.filter_by(
                                user_id=payment.user.id,
                                course_id=course.id,
                                deleted=False
                            ).first()
                        
                        if not existing_enrollment:
                            enrollment = Enrollment(
                                user=payment.user, user_id=payment.user.id,
                                course=payment.course, course_id=payment.course.id
                            )
                            db.session.add(enrollment)
                            db.session.commit()
                            return redirect(url_for('main.learn', slug=payment.course.slug))
                        return redirect(url_for('main.learn', slug=payment.course.slug))
                    else:
                        return render_template('incs/payment_successful.html', data=response_data), 200
                else:
                    return jsonify({'success':False, 'error': 'Transaction verification failed', 'data': response_data}), 400
            else:
                return jsonify({'success':False, 'error': 'Failed to verify transaction'}), 400

        elif status == 'cancelled':
            payment.tx_status = status
            db.session.commit()
            if payment.course_id:
                return redirect(url_for('main.prev', slug=payment.course.slug))
            else:
                return jsonify({'success':False, 'error': 'Transaction was cancelled'})

        else:
            return jsonify({'success':False, 'error': 'Invalid transaction status'}), 400

    except Exception as e:
        traceback.print_exc()
        return jsonify({'success':False, 'error': str(e)}), 500


@pay.route("/payment-successful")
def success():
    support_amount = "30, 40, 50, 70, 80, 90, 100, 200, 300, 400, 500"
    support_interval = "daily, weekly, monthly, quarterly, yearly"
    context = {
        "title" :'Us . Intellect',
        "support_amount" : support_amount, 
        "support_interval" : support_interval, 
    }
    return render_template('incs/payment_successful.html', **context)


""" ============Backups==================== """
@pay.route('/payment-callback-0', methods=['GET'])
@csrf.exempt
# @login_required
def payment_callback_0():
    try:
        # Extract data from query parameters
        status = request.args.get('status')
        transaction_id = request.args.get('transaction_id')
        tx_ref = request.args.get('tx_ref')

        # Fetch the payment record using the transaction reference
        payment = Payment.query.filter(Payment.tx_ref == tx_ref).first()

        if not payment:
            return jsonify({'error': 'Payment record not found'}), 404

        if status == 'successful':
            # Verify the transaction
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {current_app.config['RAVE_SECRET_KEY']}",
                "Content-Type": "application/json"
            }

            verify_endpoint = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
            response = requests.get(verify_endpoint, headers=headers)

            if response.status_code == 200:
                response_data = response.json().get('data', {})

                if (
                    response_data.get('status') == "successful"
                    and response_data.get('amount') >= payment.tx_amount
                    and response_data.get('currency') == payment.currency
                ):
                    # Update payment record
                    payment.tx_status = response_data['status']
                    payment.tx_id = response_data['id']
                    db.session.commit()

                    if payment.course_id and payment.user:
                        # If the payment is related to a course, enroll the user
                        enrollment = Enrollment(
                            user=payment.user, user_id=payment.user.id, 
                            course=payment.course, course_id=payment.course.id
                        )
                        db.session.add(enrollment)
                        db.session.commit()
                        return redirect(url_for('main.learn', slug=payment.course.slug))

                    elif payment.path_id and payment.user:
                        # print(x.title for x in payment.path.courses)
                        for course in payment.path.courses:
                            enrollment = Enrollment(
                            user=payment.user, user_id=payment.user.id, 
                            course=course, course_id=course.id
                            )
                            db.session.add(enrollment)
                            db.session.commit()
                        # path_enrollment(current_user, payment.path_id)
                        # return f"{[x.title for x in payment.path.courses]}"
                        return redirect(url_for('main.learn', slug=payment.path.courses[0].slug))

                    else:
                        # Handle non-course related transactions
                        # return jsonify({'message': 'Transaction verified successfully', 'data': response_data}), 200
                        return render_template('incs/payment_successful.html', data=response_data), 200
                else:
                    return jsonify({'message': 'Transaction verification failed', 'data': response_data}), 400
            else:
                return jsonify({'message': 'Failed to verify transaction'}), 400

        elif status == 'cancelled':
            payment.tx_status = status
            db.session.commit()
            if payment.course_id:
                return redirect(url_for('main.prev', slug=payment.course.slug))
            else:
                return jsonify({'message': 'Transaction was cancelled'})

        else:
            return jsonify({'error': 'Invalid transaction status'}), 400

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@pay.route('/init-support-pay2', methods=['POST'])
@csrf.exempt
def support_pay2():
    try:
        if request.method == "POST":
            # Get the amount, email, and subscription details from the form
            amount = request.form.get('amount')
            email = request.form.get('email') or (current_user.email if current_user.is_authenticated else None)
            subscription = request.form.get('subscription')

            if not email:
                return jsonify({"success": False, "error": "A valid email address is required for receipt of payment"})

            # Prepare request details
            url = "https://api.flutterwave.com/v3/payments"
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {current_app.config['RAVE_SECRET_KEY']}",
                "Content-Type": "application/json"
            }

            # Prepare payment payload
            payload = {
                "tx_ref": f"Techa-{generate_random_id(k=5)}",
                "amount": int(amount),
                "currency": "USD",
                # "redirect_url": f"{request.url_root}",
                "redirect_url": f"{request.url_root}payment-callback",
                "customer": {
                    "email": email,
                    "phonenumber": current_user.phone if current_user.is_authenticated and current_user.phone else None,
                    "name": current_user.name or current_user.username if current_user.is_authenticated else email
                },
                "payment_options": "card, ussd, banktransfer, credit, mobilemoneyghana",
                "customizations": {
                    "title": "Support . Intellect",
                    "logo": url_for('static', filename='img/favicon/favicon.png', _external=True)
                }
            }

            try:
                # Check if it's a subscription payment
                interval = request.form.get('interval', None)
                if interval:
                    url = "https://api.flutterwave.com/v3/payment-plans"
                    payload = {
                        "amount": payload['amount'],
                        "name": payload['customizations']["title"],
                        "interval": interval,
                        "duration": request.form.get('duration', 48)
                    }
                    response = requests.post(url, json=payload, headers=headers)
                else:
                    response = requests.post(url, json=payload, headers=headers)

                response_data = response.json() if response else {}

                # Handle payment link or errors
                payment_link = response_data.get("data", {}).get("link")
                if not payment_link:
                    print(response_data)
                    return jsonify({"success": False, "error": "Failed to retrieve payment link"})

                # Check if user exists with the provided email
                user = User.query.filter_by(email=email).first()
                if not user:
                    # Create a new user
                    user_data = {
                        'username': email,
                        'email': email,
                    }
                    new_user = User(**user_data)
                    new_user.set_password(secrets.token_urlsafe(5))
                    db.session.add(new_user)
                    db.session.commit()
                    user_id = new_user.id
                else:
                    user_id = user.id

                # Save transaction details to the database
                payment_data = {
                    'currency': payload['currency'],
                    'tx_amount': payload['amount'],
                    'tx_ref': payload['tx_ref'],
                    'tx_status': 'pending',
                    'provider': 'flutterwave',
                    'tx_id': None,
                    'user_id': user_id,
                    'course_id': None
                }
                new_payment = Payment(**payment_data)
                db.session.add(new_payment)
                db.session.commit()

                # Redirect the user to the payment link
                return jsonify({"success": True, "message": "Redirecting to payment gateway...", "redirect_url": payment_link}), 200

            except requests.exceptions.RequestException as e:
                # Handle network-related errors (e.g., no internet connection)
                return jsonify({"success": False, "error": f"An error occurred: {str(e)}"}), 500

        return jsonify({"success": False, "error": "Invalid request method"}), 405

    except Exception as e:
        print(traceback.print_exc())
        return jsonify({"success": False, "error": str(e)}), 500


@pay.route('/init-support-pay1', methods=['GET', 'POST'])
@csrf.exempt
def support_pay1():
    try:
        if request.method == "POST":

            # Make a POST request to get the payment link
            url = "https://api.flutterwave.com/v3/payments"
            headers = {
                "accept": "application/json",
                # "Authorization": f"Bearer {getenv('RAVE_SECRET_KEY')}",
                "Authorization": f"Bearer {current_app.config['RAVE_SECRET_KEY']}", # working out of request context if used outside a route
                "Content-Type": "application/json"
            }

            # Prepare payment payload
            payload = {
                "tx_ref": f"Techa-{generate_random_id(k=5)}",
                "amount": int(request.args.get('amount', 0)),
                "currency": "USD",
                #"redirect_url": f"{request.url_root}payment-callback",
                "redirect_url": f"{request.url_root}",
                "customer": {
                    "email": current_user.email if current_user.is_authenticated else request.args.get('email', 'hello@intellect.com'),
                    "phonenumber": current_user.phone if current_user.is_authenticated and current_user.phone else None,
                    "name": current_user.name or current_user.username if current_user.is_authenticated else request.args.get('email', 'hello@intellect.techa.tech')
                },
                
                "payment_options": "card, ussd, banktransfer, credit, mobilemoneyghana",
                "customizations": {
                    "title": f"Support . Russian Developers",
                    "logo": url_for('static', filename='img/favicon/favicon.png', _external=True)
                }
            }

            # is it subscription payment , just check ?
            if request.args.get('interval', None) is not None:
                #update payload and url to point to subscription endpoint
                url = "https://api.flutterwave.com/v3/payment-plans"
                payload = {
                "amount": payload['amount'],
                "name": payload['customizations']["title"],
                "interval": int(request.args.get('interval', None)),
                "duration": request.args.get('interval', 48) 
                }
                
                response = requests.post( url, json=payload, headers=headers)
            else:
                response = requests.post( url, json=payload, headers=headers)
                response_data = response.json() or response.text  if response else { }
            
                payment_link = response_data.get("data", {}).get("link")

                if not payment_link:
                    return handle_response(message="Failed to retrieve payment link", alert='alert-danger')
            
            # Check if user exists with the same email
            request_data = request.form if request.form else { }
            
            email = request_data.get('email', None)
         
            if email is None:
                return jsonify({'message': 'Ensure your email is provided'})
            
            user = User.query.filter_by(email=email).first()
            
            if user is None:
                # User does not exist, create a new user
                user_data = {
                    'username': email,
                    'email': email,
                    'password': request.args.get('password', generate_random_id(k=5))
                }
                new_user = User(**user_data)
                db.session.add(new_user)
                db.session.commit()
                db.session.refresh(new_user)  # Refresh the session to get the new user ID
                user_id = new_user.id
            else:
                # User already exists, use the existing user's ID
                user_id = user.id

            # Save transaction details to the db
            payment_data = {
                'currency': payload['currency'],
                'tx_amount': payload['amount'],
                'tx_ref': payload['tx_ref'],
                'tx_status': 'pending',
                'provider': 'flutterwave',
                'tx_id': None,
                'user_id': user_id,
                'course_id': None
            }
            new_payment = Payment(**payment_data)
            db.session.add(new_payment)
            db.session.commit()


            # Redirect the user to the payment link
            return redirect(payment_link)
    
        else:
                
            # is it subscription payment , just check ?
            #if request.args.get('interval', None) is not None:
            #update payload and url to point to subscription endpoint
            url = "https://api.flutterwave.com/v3/payment-plans"
            payload = {
            "amount": request.args.get('amount', 0),
            "name": request.args.get('name', None),
            "interval": request.args.get('interval', None) ,
            "duration": request.args.get('interval', 48) 
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            response_data = response.json() if response.text else { }
            
            if response_data.get("status") == "success":
                return handle_response(
                    message=f"Successfully subscribed to\
                        {response_data.get('interval')} for the period of {response_data.get('duration')} ",
                    alert='alert-danger')
            
            print(response.text)
            print(response.json())
                
    # except Exception as e:
    except Exception as e:
        print(traceback.print_exc())
        return f"Error:-> {e}"

@pay.route('/payment-callback1', methods=['GET'])
@csrf.exempt
@login_required
def payment_callback1():
    try:
        # Extract data from query parameters
        status = request.args.get('status')
        transaction_id = request.args.get('transaction_id')
        tx_ref = request.args.get('tx_ref')

        # Check if the transaction was successful and meets my criteria
        payment = Payment.query.filter(Payment.tx_ref == tx_ref ).first()

        if status == 'successful':
            # Proceed with processing the successful payment
            # -------------------------------------------
            # Make a request to verify the transaction
            # headers={"Authorization": f"Bearer {getenv('RAVE_SECRET_KEY')}"}
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {current_app.config['RAVE_SECRET_KEY']}", # working out of request context if used outside a route
                "Content-Type": "application/json"
            }

            verify_by_txref_endpoint = f"https://api.flutterwave.com/v3/transactions/{tx_ref}"
            verify_by_txid_endpoint = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"

            response = requests.get(verify_by_txid_endpoint, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Convert the JSON string to a Python dictionary
                response_data = response.json() if response else response.text

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
                        payment.tx_id =  transaction_data['id']

                        # Create enrollment record for the user and the course
                        enrollment = Enrollment(
                            user=current_user, user_id=current_user.id, 
                            course=payment.course, course_id=payment.course.id
                            )
                        db.session.add(enrollment)

                        db.session.commit()
                        #return jsonify({'message': 'Transaction verified successfully', 'data': transaction_data}), 200
                        return redirect(url_for('main.learn', slug=payment.course.slug))
                    else:
                        # Inform the customer their payment was unsuccessful
                        return jsonify({'message': 'Transaction Verification Failed', 'data': transaction_data}), 400
                else:
                    return jsonify({'message': 'No transaction data found'}), 400
            else:
                return jsonify({'message': 'Failed to verify transaction'}), 400

        if status == 'cancelled':
            # Success! Confirm the customer's payment
            payment.tx_status = status
            #payment.tx_id =  transaction_data['id'] ->No Transact
            db.session.commit()
            #return jsonify({'message': 'Transaction verified successfully', 'data': transaction_data}), 200
            return redirect(url_for('main.prev', slug=payment.course.slug))

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@pay.route('/check-pending-txn', methods=['GET'])
@csrf.exempt
def check_pending():
    try:
        # Your existing logic for checking transaction status
        pending_payments = Payment.query.filter(Payment.tx_status == 'pending').all()
        print([x for x in pending_payments], '\n')
        for payment in pending_payments:
            # Process pending payments
            # Make a request to verify the transaction using tx_ref
            # Make a POST request to get the payment link
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {current_app.config['RAVE_SECRET_KEY']}", # working out of request context if used outside a route
                "Content-Type": "application/json"
            }

            # headers={"Authorization": f"Bearer {getenv('RAVE_SECRET_KEY')}"}
            verify_by_txref_endpoint = f"https://api.flutterwave.com/v3/transactions/{payment.tx_ref}"
            response = requests.get(verify_by_txref_endpoint, headers=headers)
            
            if response.status_code == 200:

                response_data = response.json()

                if response_data.get('status') == 'successful':
                    # Update payment status and create enrollment
                    payment.tx_status = response_data.get('status')
                    payment.tx_id = response_data.get('id')
        
                    enrollment = Enrollment(
                        user=payment.user, user_id=payment.user.id, 
                        course=payment.course, course_id=payment.course.id
                    )
                    db.session.add(enrollment)
                    return "('Pending TXNS Updated')"
            else:
                current_app.logger.error('Failed to verify transaction')
                return "Error: Failed to verify transaction"

        db.session.commit()
        
    except Exception as e:
        # Handle exceptions
        print(type(response))
        return f"Error:-> {(e) }"

