import datetime
from email.mime.text import MIMEText
import smtplib, os
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import distinct, func 

from sqlalchemy.future import select
from sqlalchemy.sql import or_ , and_
from web.utils.chat_list import chat_list

from web.extensions import socketio
from web.chatme.forms import MessageForm
from web.models import db, User, Message

chat = Blueprint('chat', __name__)

#@chat.route('/chat', methods=['GET', 'POST'])
@chat.route('/chat/<string:usr>', methods=['GET', 'POST'])
@login_required
def chst(usr):
    usr = User.query.filter_by(username=usr).first_or_404()

    our_chat = Message.query.filter(
    and_(Message.recipient == current_user, Message.author == usr) | \
        (and_(Message.recipient == usr, Message.author == current_user) ) )
    
    form = MessageForm()
    flash(f'Your Message({form.errors}).', 'danger') if not form.validate_on_submit() else ''
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=usr, body=form.message.data)
        usr.notify('count_unread', usr.count_unread())
        db.session.add(msg)
        db.session.commit()
        flash(f'Your Message Has Been Sent.', 'success')

    return render_template('chatme/chat.html', user=usr, form=form, chat = [c for c in our_chat])

"""db.session.query(
    UserModel.city
).distinct().all()
"""
@chat.route('/chat')
@login_required
def list():
    current_user.last_message_read_time = func.now()
    current_user.notify('count_unread', 0)
    db.session.commit()

    #conversation = Message.query.filter(or_(Message.recipient == current_user, Message.author == current_user)).order_by(Message.created.desc()).distinct()
    #conversation = Message.query.filter( or_(current_user != Message.recipient, current_user != Message.author), and_(Message.author == current_user, Message.recipient == current_user)).distinct()
    conversation = User.query.filter(or_(Message.recipient == current_user, Message.author == current_user)).order_by(Message.created.desc()).distinct() 
    query = select(User.id, User.username, User.image).where(or_(Message.recipient == current_user, Message.author == current_user)).distinct()
    context = {
        'chats': conversation, #'chatsx': [ m for m in conversation]
        'chat':  [ m for m in conversation ],
        'query': query
    }
    print(conversation)
        
    return render_template('chatme/chatlist.html', **context)

#send message route
@chat.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.message.data)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.add(msg)
        db.session.commit()
        flash( ('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template('chatme/send_message.html', form=form, recipient=recipient)


#view message route
@chat.route('/email')
def email():
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('jameschristo962@gmail.com', os.environ.get('EMAIL_PASSWORD') )
        #gmail.login(FROM_EMAIL,PASSWORD)
        return 'success 1'
    except:
        print("Couldn't setup email!!")
        msg=MIMEText('message')
        msg['Subject']='subject'
        msg['To']=','.join('jameschristo962@gmail.com')
        msg['From']='jameschristo962@gmail.com'
        return 'failure 1'
    try:
        gmail.send_message(msg)
        return 'success 2'
    except:
        print("COULDN'T SEND EMAIL")
        return 'failure 2'

#view message route
@chat.route('/messages')
@login_required
def messages():
    #current_user.last_message_read_time = datetime.utcnow() 
    current_user.last_message_read_time = func.now()
    current_user.notify('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.created.desc()).paginate( page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('chat.messages', page=messages.next_num) if messages.has_next else None
    prev_url = url_for('chat.messages', page=messages.prev_num) if messages.has_prev else None
    return render_template('chatme/messages.html', messages=messages.items, next_url=next_url, prev_url=prev_url)


@socketio.on('/echo')
def echo(ws):
    while True:
        data = ws.receive()
        ws.send(data)


@socketio.on('message')
def message(data):
    print(f'\n\n{data}\n\n')
    send(data)
