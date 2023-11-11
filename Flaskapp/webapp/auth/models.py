from webapp import db, cache
from . import bcrypt
import datetime
import hashlib 
from flask_login import AnonymousUserMixin, UserMixin, login_manager
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as serializer
import jwt

roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class Permission:
    SEARCH_DESTINATION = 0x01
    BOOK_HOTELS = 0x02
    GIVE_FEEDBACK = 0x04
    MODERATE_FEEDBACK = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename_ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
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
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
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
        return '<Role {}>'.format(self.name)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(255))
    mobile = db.Column(db.Integer())
    location = db.Column(db.String(255))
    about = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=datetime.datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role_name = db.Column(db.String(64))
    tour_company = db.Column(db.String(64), nullable=False)
    company_email = db.Column(db.String(64), unique=True)
    company_mobile = db.Column(db.Integer())    
    company_address = db.Column(db.String(100))



    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role_name is None:
            if self.email == current_app.config['LETSGO_ADMIN']:
                self.role_name = Role.query.filter_by(name='Administrator').first()
            if self.role_name is None:
                self.role_name = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)   
   
    """ 
        def __init__(self, username=''):
            default = Role.query.filter_by(name='user').one()
            self.roles.append(default)
            self.username = username
    """

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    

    def generate_confirmation_token(self, expiration=1200):
        reset_token = jwt.encode(
            {
                "confirm": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=expiration)
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
                leeway = datetime.timedelta(seconds=20),
                algorithms = ["HS256"]
            )
        except:
            return False
        if data.get('confirmed') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    def generate_reset_token(self, expiration=3600):
        s = serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = jwt.decode(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    
    def ping(self):
        self.last_seen = datetime.datetime.now()
        db.session.add(self)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)
    
   
    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True
        
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False
        
    def get_id(self):
        return str(self.id)    
    
    @cache.memoize(60)
    def has_role(self, name):
        for role in self.role:
            if role.name == name:
                return True
        return False
    
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False
    
login_manager.anonymous_user = AnonymousUser

