from flask import Flask, request, render_template
from utils import *
from backend import *
from results import *

app = Flask(__name__)

#Landing page
@app.route('/start')
def index():
    return render_template("start.html")

#User enters a list of Material topics under consideration
@app.route('/topics')
def topics():
    return render_template("topics.html")

#Creating Tracker objects
ext_tracker = Tracker()
int_tracker = Tracker(False)

#Keeping track of the question id for the internal tracker
#TODO: fix this part
int_id = 1

#For each subsequent question
@app.route('/question/<int:id>', methods=["POST"])
def question(id):
    print("Here is the next question: ", ext_tracker.next_question())
    if ext_tracker.next_question():
        if id == 1:
            #Initializing object costs
            e_costs = request.form.getlist("e_cost")
            s_costs = request.form.getlist("s_cost")
            g_costs = request.form.getlist("g_cost")
            ext_tracker.assign_costs(e_costs, s_costs, g_costs)

            #TODO: see if this works and store it somewhere
            #NOTE: either put it in a Tracker object or somehow get it to the results page
            max = request.form.getlist("max")

            #Getting the Topics
            e, s, g = ext_tracker.get_topics()
            id += 1
            title, question = ext_tracker.next_question()
            return render_template("question.html", environment=e, social=s, governance=g, next=id, question=question, title=title)
        else:
            print("I'm here now")
            e = request.form.getlist("e")
            s = request.form.getlist("s")
            g = request.form.getlist("g")
            id += 1

            title, question = ext_tracker.update(e, s, g)
            e, s, g = ext_tracker.get_topics()
            return render_template("question.html", environment=e, social=s, governance=g, next=id, question=question, title=title)

    elif int_tracker.next_question():
        if int_id == 1:
            e = request.form.get("e")
            s = request.form.get("s")
            g = request.form.get("g")
            e, s, g = int_tracker.initialize(e, s, g) #Figure out how to differentiate these two trackers
            int_id += 1
            title, question = int_tracker.next_question()
            return render_template("question.html", environment=e, social=s, governance=g, next=int_id, question=question, title=title)
        else:
            e = request.form.getlist("e")
            s = request.form.getlist("s")
            g = request.form.getlist("g")
            int_id += 1

            title, question = int_tracker.update(e, s, g)
            e, s, g = int_tracker.get_topics()
            return render_template("question.html", environment=e, social=s, governance=g, next=int_id, question=question, title=title)
    else:
        #TODO: figure out how to get to this point --> code keeps breaking somewhere here
        return render_template("pre-result.html")


@app.route("/get-costs", methods=["POST"])
def get_costs():
    #Initializing Topic objects
    e = request.form.get("e")
    s = request.form.get("s")
    g = request.form.get("g")
    e, s, g = ext_tracker.initialize(e, s, g)

    #Total number of questions
    total = len(e) + len(s) + len(g)
    total = [i for i in range(1, total + 1)]

    return render_template("costs.html", environment=e, social=s, governance=g, total=total)

#TODO: fix this later
@app.route("/results", methods=["POST"])
def result():
    #Max number of topics the user wants to see
    max = request.form.get("max")

    #Getting the calculated results
    results_by_cost = merge_costs(int_tracker, ext_tracker, max)
    results_by_rank = merge_ranking(int_tracker, ext_tracker)

    #Results for each of the categories
    e, s, g = results_by_rank

    #Final results will be displayed
    return render_template("results.html", total=results_by_cost, environment=e, social=s, governance=g)
