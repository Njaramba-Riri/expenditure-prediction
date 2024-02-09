from flask_admin.contrib.sqla import ModelView


from webapp import db

class CustomModelView(ModelView):
    pass
    
class Admin(db.Model):
    __tablename__ = "superusers"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    username =  db.Column(db.String(50), unique=True ,nullable=False)
    mobile = db.Column(db.String(20), nullable=False, unique=True)
    agency = db.Column(db.String(255), nullable=False)
    agency_email = db.Column(db.String(100), nullable=False)
    agency_mobile = db.Column(db.String(20), nullable=False)
    agency_address = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    roles = db.relationship('Role', backref='admin')
    users = db.relationship('User', backref='admin')

    def is_administrator(self):
        return True



