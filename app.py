from flask import Flask, render_template, request, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey 

RESPONSES_KEY = 'responses'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mike123'

app.debug = True
debug = DebugToolbarExtension(app)

@app.route('/')
def start_page():
    
    return render_template('survey.html', survey = satisfaction_survey)

@app.route('/begin', methods=["POST"])
def start_survey():

    session[RESPONSES_KEY] = []

    return redirect('/questions/0')

@app.route('/answer', methods=["POST"])
def give_answer():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses)) == (len(satisfaction_survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/questions/<int:id>')
def show_question(id):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('complete')
    if (len(responses) != id):
        flash('Invalid Question ID')
        return redirect(f'questions/{len(responses)}')

    question = satisfaction_survey.questions[id]
    return render_template('question.html', question_num = id, question = question)

@app.route('/complete')
def show_complete():
    return render_template('complete.html')