from flask import Blueprint, render_template, request, jsonify, session, make_response, g
from flask_login import login_required, current_user
from restaurant_webapp.models import reservation, User
from restaurant_webapp import db, create_app
import requests
import rasa
import json

main = Blueprint('main', __name__)

@main.before_request
def before_request():
    g.user = current_user

@main.context_processor
def inject_user():
    g.user = current_user.get_id()
    return dict(user=g.user)

@main.route('/')
def index():
    return render_template('index.html') 

@main.route('/chatbot', methods=["POST","GET"])
@login_required
def chatbot():
    # session["user_id"] = current_user.get_id()
    # if current_user.is_authenticated():
    #     g.user = current_user.get_id()
    #     session['user_id'] = g.user
    #     print(g.user)
    usr = inject_user()
    print(usr)

    # url = 'http://localhost:5000/application/json/details'
    # try:
    #     uResponse = requests.get(url)
    # except requests.ConnectionError:
    #    return "Connection Error"  
    # if uResponse:
    #     Jresponse = uResponse.text
    #     data = json.loads(Jresponse)
    #     print(data)
    
    # response = processjson(usr=usr)
    # if response:
    #     data = json.loads(response.decode(as_text=True))
    #     print(data)

    #     under_name = data['under_name']
    #     no_of_people = data['no_of_people']
    #     time = data['time']
    #     day = data['day']

    #     new_reservation = reservation(under_name=under_name, no_of_people=no_of_people, time=time, day=day)
    #     if new_reservation:
    #         # flash('Table reserved')
    #         # return redirect(url_for('/profile'))
    #         db.session.add(new_reservation)
    #         db.session.commit()
    

    return render_template('chatbot.html', name=current_user.name)


# @main.route('/')
# @login_required
# def table_reservation():
    # new_reservation = reservation(user_id=current_user.name, under_name=under_name, no_of_people=no_of_people, time=time, day=day)
    # if new_reservation:
    #     flash('Table reserved')
    #     # return redirect(url_for('/profile'))
    # db.session.add(new_reservation)
    # db.session.commit()

@main.route('/application/json/details', methods=['POST'])
# @login_required
def processjson():
    if request.method == 'POST':
        data = request.get_json()
        under_name = data['under_name']
        no_of_people = data['no_of_people']
        time = data['time']
        day = data['day']

        # usr =  inject_user()
        # usr_id = usr['user_id']
        # user = User.query.get(session['user_name'])
        # print(data)
        # usr = session.get("user_id")
        #     #session.get("user", "")
        # app = create_app()
        # with app.test_request_context(): 
        #     if current_user.is_authenticated():
        # current_user.is_authenticated
        # print(g.user)   
        # print(current_user.get_id())  

        new_reservation = reservation(under_name=under_name, no_of_people=no_of_people, time=time, day=day)
        if new_reservation:
            # flash('Table reserved')
            # return redirect(url_for('/profile'))
            db.session.add(new_reservation)
            db.session.commit()

        return (jsonify({'result': 'success','reservation_id': new_reservation.reservation_id, 'under_name': under_name, 'no_of_people': no_of_people, 'time': time, 'day': day}))
        
    

