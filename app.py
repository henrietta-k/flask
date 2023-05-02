from flask import Flask, request, render_template
from utils import *
from backend import *

app = Flask(__name__)

#Landing page
@app.route('/start')
def index():
    return render_template("start.html")

#Check to see whether the user has input at least 5 topics or not
@app.route('/topics')
def topics():
    return render_template("topics.html")

#Creating Tracker objects
#TODO: reuse the same pages but with different questions to make these two trackers
ext_tracker = Tracker()
int_tracker = Tracker(False)


#For each subsequent question
#Next step: change each column to 3 checkboxes each with low, medium, high
@app.route('/question/<int:id>', methods=["POST"])
def question(id):
    #Figure out how to turn this into internal and external tracker
    if ext_tracker.next_question():
        if id == 1:
            e = request.form.get("e")
            s = request.form.get("s")
            g = request.form.get("g")
            e, s, g = ext_tracker.initialize(e, s, g) #Figure out how to differentiate these two trackers
            id += 1
            title, question = ext_tracker.next_question()
            return render_template("question.html", environment=e, social=s, governance=g, next=id, question=question, title=title)
        else:
            e = request.form.getlist("e")
            s = request.form.getlist("s")
            g = request.form.getlist("g")
            print("E: ", e)
            print("S: ", s)
            print("G: ", g)
            id += 1

            #TODO: the questions are currently not being moved forward (stuck on Q.1)
            #ext_tracker.update()
            title, question = ext_tracker.next_question()
            return render_template("question.html", environment=e, social=s, governance=g, next=id, question=question, title=title)
    #else:
        #Keep working on this part here
        #return render_template("results.html")

#######################
#GREEDY ALGORITHM HERE#
#######################

#Results of program shown to the user
@app.route("/results")
def results():
    topics = ["1", "2", "3"]
    return render_template("results.html", topics=topics)

