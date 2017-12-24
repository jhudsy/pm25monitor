from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
import redis
import logging

r = redis.StrictRedis(host='localhost', port=6379, db=0)

logging.getLogger('flask_cors').level = logging.DEBUG

application=Flask(__name__)
CORS(application)

@application.route("/")
def display():
    r=application.send_static_file('pm25.html')
    r.headers.add('Access-Control-Allow-Origin', '*')
    return r

@application.route("/getData",methods=['POST','GET'])
def data():
  start=request.form['starttime']
  end=request.form['endtime']
  sensor=request.form['sensor']
  return jsonify(r.zrangebyscore(sensor,int(start),int(end),withscores=True))

#application.run(host='0.0.0.0')
