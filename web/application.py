from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

application=Flask(__name__)
CORS(application)

@application.route("/")
def display():
    return send_static_file('pm25.html')

@application("/getData",methods=['POST','GET'])
def data():
  start=request.form['starttime']
  end=request.form['endtime']
  sensor=request.form['sensor']
  return jsonify(r.zrangebyscore(sensor,int(start),int(end)))
