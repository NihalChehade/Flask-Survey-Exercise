from flask import Flask, render_template, redirect, request, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, surveys

user_responses = "responses"
app = Flask(__name__)
app.config['SECRET_KEY'] = "something"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def get_homepage():
    
    return render_template("surveys-home.html", surveys = surveys)


@app.route('/picked_survey')
def picked_survey():
    selected_survey = request.args['survey_key']
    print(f"GETTTTT {selected_survey}", request.cookies.get(f"completed_{selected_survey}"))
    if request.cookies.get(f"completed_{selected_survey}"):
        return render_template("done.html")
    
    return render_template("survey-home.html", survey = surveys[selected_survey], selected_survey = selected_survey)


@app.route("/<selected_survey>/start_survey", methods=["POST"])
def start_survey(selected_survey):
    session[user_responses] = []     
    return redirect("questions/0") 


@app.route('/<selected_survey>/questions/<int:question_num>')
def questions(selected_survey, question_num):

    responses = session.get(user_responses)
    
    if not (len(responses)==question_num):
        flash("You tried to reach an invalid question!")    
        return redirect(f'{len(responses)}')
    
    if (len(surveys[selected_survey].questions) == len(responses)):
        return redirect(f"/{selected_survey}/completed")
    
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")
 
    question =surveys[selected_survey].questions[question_num]
    return render_template('question.html', question = question, selected_survey=selected_survey)

   

@app.route("/<selected_survey>/answer", methods=['POST'])
def get_answer(selected_survey):

    responses = session[user_responses]    
    responses.append({"choice": request.form['choice'], "comment": request.form.get("comment", "")})
    session[user_responses] = responses
    
    if (len(responses) == len(surveys[selected_survey].questions)) :
        return redirect("completed")
    else:
        return redirect(f"questions/{len(responses)}")


        
    
@app.route("/<selected_survey>/completed")
def survey_completed(selected_survey):
    questions = surveys[selected_survey].questions

    html = render_template("completed.html", questions= questions)

    # Set cookie noting this survey is done so they can't re-do it
    response = make_response(html)
    response.set_cookie(f"completed_{selected_survey}", "yes", max_age=120)
    print(f"SETTTTT: {selected_survey}", request.cookies.get(f"completed_{selected_survey}"))
    return response

   
