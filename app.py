from flask import Flask, render_template, request, jsonify
from flask import flash
from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import time

engine = ("mysql+pymysql://root:shreesh@localhost/ticketsdb")

app = Flask(__name__)
app.config['SECRET_KEY']='1234567shreesh'
app.config['SQLALCHEMY_DATABASE_URI'] = engine
db = SQLAlchemy(app)

class tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    timing = db.Column(db.DateTime)

def display():
    alltickets= tickets.query.all()
    l=[]
    for i in alltickets:
        temp={}
        temp['name']=i.user_name
        temp['phone_no']=i.phone
        temp['timing']=str(i.timing)
        l.append(temp)
    return json.dumps(l)

@app.route('/book', methods=["GET","POST"])
def book():
    if request.method == "GET":
        return jsonify("HELLO")
    if request.method== "POST":
        req_Json = request.json
        name = req_Json['name']
        phone = req_Json['phone number']
        t = req_Json['timings']
        time1 = datetime.strptime(t,"%d/%m/%Y %H:%M:%S")
        alltickets = tickets.query.filter_by(timing=time1).all()
        count = len(alltickets)
        print(count)
        if(count<=20):
            ticket = tickets(user_name=name, phone=phone, timing=time1)
            db.session.add(ticket)
            db.session.commit()
            return display()
        else:
            return {"message":"All seats are full"}

@app.route('/update', methods=["GET","POST"])
def update():
    if request.method == "GET":
        return jsonify("HELLO")
    if request.method== "POST":
        req_Json = request.json
        userid = int(req_Json['id'])
        newtime = req_Json['newtime']
        newtime = datetime.strptime(newtime,"%d/%m/%Y %H:%M:%S")
        ticket = tickets.query.filter_by(id=userid).first()
        if ticket is None:
            return {"message":"ticket expired"}
        ticket.timing = newtime
        db.session.commit()
        return display()

@app.route('/viewAccToTime', methods=["GET","POST"])
def viewAccToTime():
    req_Json = request.json
    time = req_Json['timing']
    time = datetime.strptime(time,"%d/%m/%Y %H:%M:%S")
    alltickets = tickets.query.filter_by(timing=time).all()
    l=[]
    for i in alltickets:
        temp={}
        temp['name']=i.user_name
        temp['phone_no']=i.phone
        l.append(temp)
    return json.dumps(l)

@app.route('/delete', methods=["GET","POST"])
def delete():
    req_Json = request.json
    name = req_Json['name']
    time = req_Json['timing']
    time = datetime.strptime(time,"%d/%m/%Y %H:%M:%S")
    deleteticket = tickets.query.filter_by(user_name=name,timing=time).first()
    db.session.delete(deleteticket)
    db.session.commit()
    return display()

@app.route('/viewAccToId', methods=["GET","POST"])
def viewAccToId():
    req_Json = request.json
    id = int(req_Json['id'])
    alltickets = tickets.query.filter_by(id=id).all()
    l=[]
    for i in alltickets:
        temp={}
        temp['name']=i.user_name
        temp['phone_no']=i.phone
        temp['timing']=str(i.timing)
        l.append(temp)
    return json.dumps(l)


db.create_all()

if __name__ == "__main__":
    allticketdata= tickets.query.all()
    for i in allticketdata:
        now = datetime.now()
        # print("current time ")
        # print(now)
        bookingtime = i.timing
        duration = bookingtime-now
        # print("time diff: "),
        # print(duration)
        duration_in_s = duration.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]
        print(hours)
        if hours>8 :
            exp = tickets.query.filter_by(timing=bookingtime).first()
            db.session.delete(exp)
            db.session.commit()
            display()
    app.run(debug=True)
