from flask import Blueprint, render_template
from flask_login import login_required, current_user

from . import db
from .models import User, Companies, Transactions

import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@login_required
@views.route('/customerdashboard', methods=['GET'])
def customer_dashboard():
    user_info = User.query.get_or_404(int(current_user.id))
    return render_template("customerdashboard.html", user=user_info)


@views.route('/leaderboard', methods=['GET'])
def leaderboard():  
   all_customers = User.query.all()
   return render_template("leaderboard.html", customers=all_customers)


# QR code link
@views.route('/gainpoint/<int:UserId>/by/<int:CompanyId>/<int:PointsGained>', methods=["GET", 'POST'])
def gain_point(PointsGained, CompanyId, UserId):

    user_info = User.query.get_or_404(int(UserId))
    print("prevpoints: ", user_info.points)

    company_info = Companies.query.get_or_404(int(CompanyId))

    user_info.points += int(PointsGained)
    print("afterpoints: ", user_info.points)

    print('company that gave points is named: ', company_info.CompanyName)

    new_transaction = Transactions(receiverId=int(UserId), invokerId=int(CompanyId), pointsValue=int(PointsGained))
    db.session.add(new_transaction)
    db.session.commit()

    return render_template("business.html", user=current_user)

@views.route('/explore', methods=["GET"])
def explore_companies():
    all_companies = Companies.query.all()
    return render_template("explore.html", all_companies=all_companies)
