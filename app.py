from flask import Flask, request, render_template, redirect
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

#For each subsequent question
#TODO: fix the code quality here --> use if statements for ext and int
@app.route('/question/<int:id>', methods=["POST"])
def question(id):
    if ext_tracker.next:
        if id == 1:
            #Initializing object costs
            e_costs = request.form.getlist("e_cost")
            s_costs = request.form.getlist("s_cost")
            g_costs = request.form.getlist("g_cost")
            ext_tracker.assign_costs(e_costs, s_costs, g_costs)

            #Max number of topics the user wants to see at the end
            ext_tracker.max = request.form.getlist("max")

            #Getting the Topics
            e, s, g = ext_tracker.get_topics()
            id += 1
            title, question = ext_tracker.next_question()
            return render_template("question.html", environment=e, social=s, governance=g, next=id, question=question, title=title)
        else:
            e = request.form.getlist("e")
            s = request.form.getlist("s")
            g = request.form.getlist("g")
            id += 1
            ext_tracker.update(e, s, g)

            if ext_tracker.next_question():
                title, question = ext_tracker.next_question()
                e, s, g = ext_tracker.get_topics()
                return render_template("question.html", environment=e, social=s, governance=g, next=id, question=question, title=title)
            else:
                ext_tracker.next = False
                e, s, g = int_tracker.initialize(list(ext_tracker.e.keys()),
                                                 list(ext_tracker.s.keys()),
                                                 list(ext_tracker.g.keys()))
                title, question = int_tracker.next_question()
                return render_template("question.html", environment=e, social=s, governance=g, next=id, question=question, title=title)
    elif int_tracker.next:
        e = request.form.getlist("e")
        s = request.form.getlist("s")
        g = request.form.getlist("g")
        id += 1
        int_tracker.update(e, s, g)

        if int_tracker.next_question():
            title, question = int_tracker.next_question()
            e, s, g = int_tracker.get_topics()
            return render_template("question.html", environment=e, social=s, governance=g, next=id, question=question, title=title)
        else:
            return redirect("/results")


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

@app.route("/results", methods=["GET"])
def result():
    #Getting the calculated results
    results_by_cost = ["a", "b", "c"]#merge_costs(int_tracker, ext_tracker)
    results_by_rank = merge_ranking(int_tracker, ext_tracker)

    #Results for each of the categories
    e, s, g = results_by_rank

    #Final results will be displayed
    return render_template("results.html", total=results_by_cost, environment=e, social=s, governance=g)
