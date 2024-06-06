from webapp import db

class Search(db.Model):
    __tablename__ = "search"

    id = db.Column(db.Integer(), primary_key=True)
    destination  = db.Column(db.String(255), nullable=False)
    total_adults = db.Column(db.Integer(), nullable=False)
    total_kids = db.Column(db.Integer(), nullable=True)
    checkin_date = db.Column(db.DateTime(), nullable=False)
    checkout_date = db.Column(db.DateTime(), nullable=False)
    rooms = db.Column(db.Integer(), nullable=True)
    user_id  = db.Column(db.Integer(), db.ForeignKey('users.id'))