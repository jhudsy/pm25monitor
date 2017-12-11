from serialWorker import SerialWorker
import time,random #for testing only
from util import makePGChart
import flask
from threading import Lock

app=flask.Flask(__name__)

ds=[]
lock=Lock()
sw=SerialWorker(None,ds,lock)
#ds=[[time.time()-24*60*60+x,random.random(),random.random()] for x in range(24*60*60)]

@app.route("/dayInMinutes.svg")
def minutes():
  chart=makePGChart(time.time()-24*60*60,60,ds)
  return chart.render_response()
  
