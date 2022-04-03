# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from flask import current_app, session, request
from flask_login import current_user
from restaurant_webapp import create_app
from restaurant_webapp.models import reservation
import requests
from werkzeug.local import LocalProxy
import random, re
import json
from threading import Thread

# app = create_app()                   # these 3 lines links the thread from application restaurant_webapp to this current_app
#                                      # else you can also use ctx = app.app_context() to just create the context and install it using 
# with app.app_context():              # ctx.push() and again to unlink, use ctx.pop()
#     print(current_app.config)        # 

# def random_one(p1, N):
#         p0 =  1 - p1
#         T = [(1,p1),(0,p0)]
#         deck = []

#         for item in T:
#             deck += [item[0]] * int(round(N*item[1]))

#         random.shuffle(deck)
#         return deck

class askTime(Action):

    def name(self) -> Text:
        return "action_ask_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        time = tracker.get_slot('time')
        
        if time == None:
            dispatcher.utter_message(response="utter_booking_time")

        return []

class askNOPeople(Action):

    def name(self) -> Text:
        return "action_ask_no_of_people"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        no_people = tracker.get_slot('no_of_people')

        if no_people == None:
            dispatcher.utter_message(response="utter_no_people")

        return []

class askUnderName(Action):

    def name(self) -> Text:
        return "action_ask_under_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        under_name = tracker.get_slot('under_name')

        if under_name == None:
            dispatcher.utter_message(response="utter_ask_under_name")

        return []

class askDay(Action):

    def name(self) -> Text:
        return "action_ask_day"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        day = tracker.get_slot('day')

        if day == None:
            dispatcher.utter_message(response="utter_ask_day")

        return []
        

class confirmReservation(Action):

    def name(self) -> Text:
        return "action_confirm_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        no_people = tracker.get_slot('no_of_people')
        time = tracker.get_slot('time')
        day = tracker.get_slot('day')
        under_name = tracker.get_slot('under_name')

        intent = tracker.latest_message['intent'].get('name')

        if intent == 'ans_yes':

            # # add to db
            # app = create_app()
            # with app.test_request_context():
            #     # table_reservation(under_name=under_name, no_of_people=no_people, time=time, day=day)
            #     Thread(target=table_reservation, args=(under_name, no_people, time, day))
                
                # user_id = request.session.get('user_id')
                # print(user_id)
            payload = {'under_name': under_name, 'no_of_people': no_people, 'time': time, 'day': day}
            r = requests.post('http://localhost:5000/application/json/details', json=payload)

            print(r)
            print(r.text)
            det = json.loads(r.text)
            res_id = det["reservation_id"]

            # dispatcher.utter_message(text="Your reservation ID is: {}" .format(res_id))
            # row_template = '''
            # <html>
            #     <body>
            #         <table>
            #             <tr class="trBorder">
            #                 <!-- content inside <td> -->
            #                 <th>ID</th>
            #                 <th>Name</th>
            #                 <th>Time</th>
            #                 <th>Day</th>
            #             </tr>
            #             <tr class="trBorder">
            #                     <!-- content inside <td> -->
            #                     <td>{}</td>
            #                     <td>{}</td>
            #                     <td>{}</td>
            #                     <td>{}</td>
            #             </tr>
            #         </table>
            #     </body>
            # </html>'''
            # row_template = row_template.format(res_id,under_name,time,day)
            # # row_template = row_template.format(row_template)
            # row_template = row_template.replace("\n", "")
            # row_template = row_template.replace(" ","")
            # dispatcher.utter_message(row_template)
            dispatcher.utter_message(response="utter_booking_slot_values")
        elif intent == 'ans_no':
            dispatcher.utter_message(response="utter_no_tables_reserved")

        return []