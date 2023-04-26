from flask import Flask, render_template
from utils import *

app = Flask(__name__)

#Landing page
@app.route('/start')
def index():
    return render_template("start.html")

#User inputs their material topics
@app.route('/topics')
def topics():
    e = None
    s = None
    g = None
    return render_template("topics.html")

#First question to ask the user
@app.route("/question-1")
def question_1():
    topics = ["1", "2", "3"]
    return render_template("question-1.html", topics=topics)

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

#Use an if statement in the html question files themselves
@app.route('/') #question/<int:id>'
def question(): #q, topics, next=True figure out how to use inputs later
    topics = ["1", "2", "3"]
    q = "Hello"
    return render_template("question.html", question=q, topics=topics, next=next)

