from flask_admin.contrib.sqla import ModelView


from webapp import db

class CustomModelView(ModelView):
    pass
    
class Admin(db.Model):
    __tablename__ = "superusers"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, index=True)
    username =  db.Column(db.String(50), unique=True)
    mobile = db.Column(db.String(20), unique=True)
    agency = db.Column(db.String(255))
    agency_email = db.Column(db.String(100))
    agency_mobile = db.Column(db.String(20))
    agency_address = db.Column(db.String(255))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    roles = db.relationship('Role', backref='admin')
    users = db.relationship('User', backref='admin')

    def is_administrator(self):
        return True
