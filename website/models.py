from . import db, admin
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    social_media = db.Column(db.String(300))
    points = db.Column(db.Integer)
    
class Explore(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.String(100))
    promotionTitle = db.Column(db.String(100))
    promotionDescription = db.Column(db.String(200))
    promotion_image = db.Column(db.String(300))
    promotion_points = db.Column(db.Integer)


class ExploreView(ModelView):
    pass

admin.add_view(ExploreView(Explore, db.session))  

class UsersView(ModelView):
    pass

admin.add_view(UsersView(User, db.session))

class Companies(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.String(100))
    Balance = db.Column(db.Integer)


class CompaniesView(ModelView):
    pass

admin.add_view(CompaniesView(Companies, db.session))  

class Transactions(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiverId = db.Column(db.String(100))
    invokerId = db.Column(db.String(100))
    pointsValue = db.Column(db.Integer)

class TransactionsView(ModelView):
    pass

admin.add_view(TransactionsView(Transactions, db.session))



