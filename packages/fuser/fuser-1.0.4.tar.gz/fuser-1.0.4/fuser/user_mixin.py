from flaskapp.extensions import db
from flask import (Blueprint, request, render_template, flash, url_for, send_from_directory, make_response,
                   redirect, current_app, abort, g)

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps
from pga.basemodel import BaseModelMixin
import bcrypt
from sqlalchemy.dialects.postgresql import ARRAY

from citext import CIText
from sqlalchemy.ext.declarative import declared_attr


import sendgrid
import os
from sendgrid.helpers.mail import *

class UserMixin(BaseModelMixin):
    email = db.Column(CIText, nullable=False, unique=True)
    phone = db.Column(db.Text, nullable=True, unique=True)
    hashed_pw = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    @declared_attr
    def clients(self):
        from .client import Client
        return relationship("Client", backref="user")

    @declared_attr
    def activator_tokens(self):
        from .activator_token import ActivatorToken
        return relationship("ActivatorToken", backref="user")

    def has_ever_logged_in(self):
        return len(self.clients) > 0

    def after_login_redirect_desintation(self):
        try:
            return self.after_login_desintation()
        except AttributeError:
            return '/dashboard'

    def set_password(self, plaintext_password):
        self.hashed_pw = bcrypt.hashpw(plaintext_password.encode('utf-8'),
                                       bcrypt.gensalt())\
                               .decode('utf-8')

    def hashed_pw_matches_plaintext(self, plaintext_password):
        try_hash = bcrypt.hashpw(plaintext_password.encode('utf-8'),
                                 self.hashed_pw.encode('utf-8'))
        
        return try_hash.decode('utf-8') == self.hashed_pw


    def send_email(self, to, subject, content):
        sg = sendgrid.SendGridAPIClient(apikey=current_app.config['SENDGRID_API_KEY'])
        from_email = Email(current_app.config['SENDGRID_DEFAULT_FROM'])
        to_email = Email(to)
        subject = subject
        content = Content("text/html", content)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        return response.status_code



    def send_default_activator_email(self, subject, text_main, text_second='Please click the button below to confirm your email.', title='Activate your account', template='default_alert_email.html', function='default'):
        # Create the activator token.
        from fuser.activator_token import ActivatorToken

        activator_token = ActivatorToken.activator_token_for_user(self, function)

        status_code = self.send_email(to=self.email,
                             subject=subject,
                             content=render_template(template, 
                             title=title, 
                             text_main=text_main, 
                             text_second=text_second, 
                             button_href= "http://" + current_app.config['SERVER_NAME'] + '/auth/set_password/' + activator_token.activator_code, 
                             button_text='Activate account & Set Password',
                            ))



def authenticate(mode=True):
    """ 
    * admin: must has is_admin flag set to true (useful for prod support access)
    * valid: must be a user in "good standing"
    * public: allow anyone through, may or may not inject a user_obj into the context

    Only admin and valid gaurentee a user object being injected into the resonse func
    """ 
    assert mode in ('admin', 'valid', 'public'), "Invalid authentication mode '{}'".format(mode)

    def auth_actual(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'client_key' not in request.cookies:
                if not mode == 'public':
                    return redirect('/login')
                else:
                    return f(*args, **kwargs)
            else:
                client_key = request.cookies['client_key']
                try:
                    from .client import Client
                    client_obj = Client.query.filter_by(client_key=client_key)\
                                             .filter_by(is_active=True)\
                                             .one()
                    if client_obj.user.is_active == False:
                        abort(401, 'Inactive user')

                except NoResultFound:
                    if not mode == 'public':
                        return redirect('/login')
                    else:
                        return f(*args, **kwargs)
                else: # Valid client was found
                    if mode == 'admin':
                        if not client_obj.user.is_admin:
                            abort(401, 'Unauthorized to view this page.')
                    
                    kwargs['user_obj'] = client_obj.user
                    return f(*args, **kwargs)
        return decorated
    return auth_actual
