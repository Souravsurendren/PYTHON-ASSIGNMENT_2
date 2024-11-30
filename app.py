from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Used for session management

# Load quiz questions from a JSON file
def load_questions():
    with open('questions.json') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username  # Store username in session
        return redirect(url_for('quiz'))
    return render_template('profile.html')

@app.route('/quiz')
def quiz():
    if 'username' not in session:
        return redirect(url_for('profile'))
    
    questions = load_questions()
    return render_template('quiz.html', questions=questions)

@app.route('/result', methods=['POST'])
def result():
    questions = load_questions()
    total_score = 0
    correct_answers = 0
    
    # Evaluate user's answers
    for question in questions:
        user_answer = request.form.get(str(question['id']))
        if user_answer == question['answer']:
            correct_answers += 1
            total_score += 1  # Modify scoring logic if needed
    
    username = session.get('username', 'Guest')
    return render_template('result.html', score=total_score, total=len(questions), username=username)

if __name__ == '__main__':
    app.run(debug=True)
