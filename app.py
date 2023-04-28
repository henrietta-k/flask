from flask import Flask, request, render_template, redirect, url_for
from utils import *

app = Flask(__name__)

#Landing page
@app.route('/start')
def index():
    return render_template("start.html")

@app.route('/topics')
def topics():
    return render_template("topics.html")

#First question to ask the user
@app.route("/question-1", methods=["POST"])
def question_1():
    environment = request.form.get("environment")
    social = request.form.get("social")
    governance = request.form.get("governance")
    return render_template("question-1.html", environment=environment, social=social, governance=governance)

#DELETE THIS LATER
@app.route("/question", methods=["POST", "GET"])
def question_2():
    #environment = request.form.get("environment")
    #social = request.form.get("social")
    #governance = request.form.get("governance")
    return render_template("question.html", environment=environment, social=social, governance=governance)

#Current question number
question_id = 2

#For each remaining question
@app.route('/#question/<int:id>')
def question(e, s, g, next, methods=["POST", "GET"]): #q, topics, next=True figure out how to use inputs later
    if questions_ext:
        next=True
    return render_template("question-<int>.html", environment=e, social=s, governance=g, next=next) #Figure out how to fix this

#######################
#GREEDY ALGORITHM HERE#
#######################

#Results of program shown to the user
@app.route("/results")
def results():
    topics = ["1", "2", "3"]
    return render_template("results.html", topics=topics)


#THESE ROUTES AREN'T CURRENTLY IN USE
@app.route('/about')
def about():
    id = "Materiality Assesment"
    names = ["1", "2", "3"]
    return render_template("about.html", title=id, names=names)
