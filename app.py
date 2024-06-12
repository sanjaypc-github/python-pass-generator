from flask import Flask, render_template, request
import random
import string
import pyttsx3

app = Flask(__name__)

def analyze_password(password):
    length = len(password)
    upper_count = sum(1 for c in password if c.isupper())
    lower_count = sum(1 for c in password if c.islower())
    digit_count = sum(1 for c in password if c.isdigit())
    special_count = sum(1 for c in password if c in string.punctuation)

    score = length + upper_count + lower_count + digit_count + special_count

    return {
        'score': score,
        'length': length,
        'upper_count': upper_count,
        'lower_count': lower_count,
        'digit_count': digit_count,
        'special_count': special_count
    }

def generate_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def pronounce_password(password):
    engine = pyttsx3.init()
    engine.setProperty('rate', 100)  # Slow down the speech rate
    engine.say(' '.join(password))   # Spell out the password slowly
    engine.runAndWait()

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis = None
    generated_password = None
    suggestion_analysis = None

    if request.method == 'POST':
        if 'password_to_analyze' in request.form:
            password = request.form['password_to_analyze']
            analysis = analyze_password(password)
            pronounce_password(password)
            if analysis['score'] < 8:
                generated_password = generate_password()
                suggestion_analysis = analyze_password(generated_password)
                pronounce_password(generated_password)
        elif 'generate_password' in request.form:
            generated_password = generate_password()
            pronounce_password(generated_password)
            suggestion_analysis = analyze_password(generated_password)
    
    return render_template('index.html', analysis=analysis, generated_password=generated_password, suggestion_analysis=suggestion_analysis)

if __name__ == '__main__':
    app.run(debug=True)
