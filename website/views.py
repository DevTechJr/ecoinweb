from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from datetime import datetime

from . import db
from .models import User, Companies, Transactions

import json

views = Blueprint('views', __name__)

def updateUserCoins(id):
    user = User.query.get_or_404(int(id))
    getUserTransactions = Transactions.query.filter(Transactions.receiverId==int(id))
    sum = 0
    for transaction in getUserTransactions:
        sum += transaction.pointsValue
    user.points = sum

    db.session.commit()


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@login_required
@views.route('/customerdashboard', methods=['GET'])
def customer_dashboard():
    if current_user.is_authenticated == False:
        return redirect(url_for('auth.login'))
        
    updateUserCoins(current_user.id)
    user_info = User.query.get_or_404(int(current_user.id))
    updateUserCoins(current_user.id)
    user_transactions_list = []
    companies = []
    user_transactions = Transactions.query.filter(
    Transactions.receiverId == int(current_user.id)
).order_by(desc(Transactions.id)).all()

    
    for transaction in user_transactions:
        company_info = Companies.query.get_or_404(int(transaction.invokerId))

        companies.append(company_info.CompanyName)
        user_transactions_list.append(transaction)

    entries_length = len(companies)
    
    name = user_info.first_name + ' ' + user_info.last_name
    todayDate = datetime.now().strftime('%Y-%m-%d')

    return render_template("customerdashboard.html", todayDate = todayDate, current_user = current_user, name=name, entries_length=entries_length, companies=companies, user_transactions_list=user_transactions_list)


@views.route('/leaderboard', methods=['GET'])
def leaderboard():  
    all_customers = User.query.order_by(desc(User.points)).all()
    return render_template("leaderboard.html", customers=all_customers)


@views.route('/company/<int:CompanyId>', methods=['GET'])
def company_dashboard(CompanyId):  
   company_details = Companies.query.get_or_404(int(CompanyId))
   company_transactions = Transactions.query.filter(Transactions.invokerId==int(CompanyId)) 
   company_transactions_list = []
   names = []
   social_media = []

   
   
   for transaction in company_transactions:
       user_info = User.query.get_or_404(int(transaction.receiverId)) 
       company_transactions_list.append(transaction)
       names.append(str(user_info.first_name) + ' ' + str(user_info.last_name))
       social_media.append(str(user_info.social_media))
    
    
   entries_length = len(company_transactions_list)
   todayDate = datetime.now().strftime('%Y-%m-%d')
      
   return render_template("companydashboard.html", todayDate=todayDate, company_details=company_details, entries_length=entries_length, company_transactions_list=company_transactions_list, names=names, social_media=social_media, date=datetime.now().strftime('%Y-%m-%d'))


# QR code link
@views.route('/gainpoint/<int:UserId>/from/<int:CompanyId>/<int:PointsGained>', methods=["GET", 'POST'])
def gain_point(PointsGained, CompanyId, UserId):
    user_info = User.query.get_or_404(int(UserId))
    company_info = Companies.query.get_or_404(int(CompanyId))
    user_info.points = user_info.points + int(PointsGained)
    company_info.Balance = company_info.Balance + int(PointsGained*10//100)
    new_transaction = Transactions(receiverId=int(UserId), invokerId=int(CompanyId), pointsValue=int(PointsGained))
    db.session.add(new_transaction)
    db.session.commit()
    return redirect(url_for('views.customer_dashboard'))

@views.route('/explore', methods=["GET"])
def explore_companies():
    all_companies = Companies.query.all()
    all_companies_list = []
    business_descriptions = [   
    ["2-5", "Small Business","eco-friendly products made with natural resources to offset industrial grade produced products." ],
    ["6-10", "Large Business","green building practices in real estate development with eco-friendly materials and energy efficient systems." ],
    ["5-8", "Food Market", "Ditch The Plastic Campaign; to replace plastics with compostable containers and bags, local climate workshops" ], 
    ["4-9", "Partner Initiative", "offers resources, workshops, and networking opportunities to support eco-friendly initiatives with local businesses"],
    ["7-10", "Community Recognition", "recognizes and awards Kitchener businesses/organizations that excel in environmental practices and sustainability"], 
    ["4-7", "Partner Initiative", "Municipal Service in Kitchener-Waterloo Region provides programs focused on wastemanagement, recycling, and sustainability"], 
    ["8-10", "Large Business", "products are designed to provide reliable and efficient energy, affordability, and durability solutions for residential, commercial, and industrial applications."],

    ]
    for company in all_companies:
       all_companies_list.append(company)
    
    entries_length = len(all_companies_list)

    return render_template("explore.html", all_companies=all_companies_list, business_descriptions=business_descriptions, entries_length=entries_length)

    