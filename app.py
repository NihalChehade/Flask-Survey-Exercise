from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

user_key = "responses"
app = Flask(__name__)
app.config['SECRET_KEY'] = "something"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)



@app.route('/')
def get_homepage():
    
    return render_template("survey-home.html", s = satisfaction_survey)

@app.route("/start_survey", methods=["POST"])
def start_survey():
    session[user_key] = []
    return redirect("/questions/0")

@app.route('/questions/<int:question_num>')
def questions(question_num):
    responses = session.get(user_key)
    if not (len(responses)==question_num):
        flash("You tried to reach an invalid question!")    
        return redirect(f'/questions/{len(responses)}')
    
    if (len(satisfaction_survey.questions) == len(responses)):
        return redirect("/completed")
    
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")
   

    question = satisfaction_survey.questions[question_num]
    return render_template('question.html', question=question)
   

@app.route("/answer", methods=["POST"])
def get_answer():
    responses = session[user_key]
    if (len(responses) == len(satisfaction_survey.questions)) :
        return redirect("/completed")
    else : 
        print(request.form["choice"])
        responses.append(request.form["choice"])
        session[user_key] = responses
        return redirect(f"/questions/{len(responses)}")
        
    
@app.route("/completed")
def survey_completed():
    return render_template("completed.html")

