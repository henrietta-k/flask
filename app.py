from flask import Flask, request, render_template
from utils import *

app = Flask(__name__)

#Landing page
@app.route('/start')
def index():
    return render_template("start.html")

@app.route('/topics')
def topics():
    return render_template("topics.html")

#For each subsequent question
#Change each column to 3 checkboxes each with low, medium, high
@app.route('/question/<int:id>', methods=["POST"])
def question(id):
    if questions_ext:
        if id == 1:
            #Remember to split this by "," later on
            e = request.form.get("e")
            s = request.form.get("s")
            g = request.form.get("g")
        else:
            e = request.form.getlist("e")
            s = request.form.getlist("s")
            g = request.form.getlist("g")
        id += 1
        title, q = questions_ext.pop(0)

        #Update topics + minheap
        #Update the questions list
        return render_template("question.html", environment=e, social=s, governance=g, next=id, question=q, title=title)
    else:
        return render_template("results.html")

#######################
#GREEDY ALGORITHM HERE#
#######################

#Results of program shown to the user
@app.route("/results")
def results():
    topics = ["1", "2", "3"]
    return render_template("results.html", topics=topics)

