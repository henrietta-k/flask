from flask import Flask, request, render_template
from utils import *
from backend import *
from results import *

app = Flask(__name__)

#Landing page
@app.route('/start')
def index():
    return render_template("start.html")

#TODO: [maybe] Check to see whether the user has input at least 5 topics or not
@app.route('/topics')
def topics():
    return render_template("topics.html")

#Creating Tracker objects
#TODO: reuse the same pages but with different questions to make these two trackers
ext_tracker = Tracker()
int_tracker = Tracker(False)

#For each subsequent question
@app.route('/question/<int:id>', methods=["POST"])
def question(id):
    #Figure out how to turn this into internal and external tracker
    if ext_tracker.next_question(): #TODO: figure out which function to call here, it's either update or next_question
        if id == 1:
            e = request.form.get("e")
            s = request.form.get("s")
            g = request.form.get("g")
            e, s, g = ext_tracker.initialize(e, s, g) #Figure out how to differentiate these two trackers
            id += 1
            title, question = ext_tracker.next_question()
            return render_template("question.html", environment=e, social=s, governance=g, next=id, question=question, title=title)
        else:
            #TODO: Change this and feed it into the update function
            e = request.form.getlist("e")
            s = request.form.getlist("s")
            g = request.form.getlist("g")
            id += 1

            title, question = ext_tracker.update(e, s, g)
            e, s, g = ext_tracker.get_topics()
            return render_template("question.html", environment=e, social=s, governance=g, next=id, question=question, title=title)
    #else:
        #Keep working on this part here
        #return render_template("results.html")

@app.route("/choose-result", methods=["POST"]) #or is it get?
def choose_result():
    return render_template("choose_result.html")
    #Then make a form that redirects to the results page

#Results of program shown to the user
@app.route("/results", methods=["POST"])
def results():
    choices = request.form.get("choices")
    results = compile_results(int_tracker, ext_tracker, choices)
    return render_template("results.html", results=results)

