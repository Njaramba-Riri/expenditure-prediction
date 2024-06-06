import datetime
import hashlib 
import jwt
from time import time

from flask import current_app, request, has_request_context
from flask_login import AnonymousUserMixin, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp import db, cache
from . import bcrypt

class Permission:
    SEARCH_DESTINATION = 0x01
    BOOK_HOTELS = 0x02
    GIVE_FEEDBACK = 0x04
    MODERATE_FEEDBACK = 0x08
    ADMINISTER = 0x80
    
class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    default = db.Column(db.Boolean(), default=False, index=True)
    permissions = db.Column(db.Integer())
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod    
    def insert_roles():
        roles = {
            'User': (Permission.GIVE_FEEDBACK |
                     Permission.SEARCH_DESTINATION |
                     Permission.BOOK_HOTELS, True),         
            'Anonymous': (Permission.SEARCH_DESTINATION,
                           False),
            'Administrator': (0xff, False)
        }
        # default_role = 'User'
        # for r in roles:
        #     role = Role.query.filter_by(name=r).first()
        #     if role is None:
        #         role = Role(name=r)
        #     role.reset_permissions()
        #     for perm in roles[r]:
        #         role.add_permission(perm)
        #     role.default = (role.name == default_role)
        #     db.session.add(role)
        # db.session.commit()

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
        
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    def __repr__(self):
        return 'Role: {}'.format(self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    full_name = db.Column(db.String(100))
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(255))
    location = db.Column(db.String(255))
    about = db.Column(db.String(200))
    confirmed = db.Column(db.Boolean(), default=False)
    avatar = db.Column(db.String(255))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    date_created = db.Column(db.DateTime(), default=datetime.datetime.now())
    last_seen = db.Column(db.DateTime(), default=datetime.datetime.now())
    features = db.relationship('Features', backref='user', lazy='dynamic')
    feedback = db.relationship('Feedback', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN']:
                self.confirmed = True
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        
        if self.email is not None and self.avatar is None:
            self.avatar = hashlib.md5(
                self.email.encode('utf-8')
            ).hexdigest()   
   
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if has_request_context() and request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


    def generate_confirmation_token(self, expiration=20000):
        reset_token = jwt.encode(
            {
                "confirm": self.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm  ="HS256"
        )
        return reset_token
    
    def confirm(self, token):
        try:
            data = jwt.decode(
                token, 
                current_app.config['SECRET_KEY'],
                algorithms = ["HS256"]
            )
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    def generate_reset_token(self, expiration=3600):
        return jwt.encode(
            {
                'reset_password':self.id, 
                'exp': time() + expiration},
                current_app.config['SECRET_KEY'], 
                algorithm='HS256'
            )

    @staticmethod
    def confirm_reset_token(token, new_password):
        try:
            unique = jwt.decode(
                token, 
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except:
            return False
        user = db.session.get(User, unique)
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True 
      
    def ping(self):
        self.last_seen = datetime.datetime.now()
        db.session.add(self)
    
    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True
    
    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False
        
    def get_id(self):
        return str(self.id)    
    
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
    
    @cache.memoize(60)
    def has_role(self, name):
        for role in self.role:
            if role.name == name:
                return True
        return False
