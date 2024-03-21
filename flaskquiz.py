from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)

dizRisposte = {
    "question1" : "r2",
    "question2" : "r1",
    "question3" : "r1",
    "question4" : "r2",
    "question5" : "r1",
    "question6" : "r1",
}

def get_db_connection():
    mydb = mysql.connector.connect(
     host="gabrielepetroni.mysql.pythonanywhere-services.com",
     user="gabrielepetroni",
     password="kodlandprovapython",
     database="gabrielepetroni$default"
    )
    return mydb

def get_decimal_score(score : int):
    return score * 100 / 6

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/res',  methods=['POST'])
def result():
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['usermail']

        score = 0

        for key in dizRisposte.keys():
            if dizRisposte[key] == request.form[key]:
                score += 1

        decimalScore = get_decimal_score(score)

        cursor.execute('SELECT score FROM users WHERE id=%s', (email,))

        result = cursor.fetchone()

        if result:
            currentDecimalScore = get_decimal_score(result[0])
            if decimalScore > currentDecimalScore:
                cursor.execute('UPDATE users SET score=%s WHERE id=%s', (score, email))
                db.commit()
            cursor.close()
            db.close()
            return render_template('result.html', username=username, decimalScore=round(decimalScore), score=score, maxscore=round(currentDecimalScore))
        else:
            cursor.execute('INSERT INTO users VALUES (%s, %s)', (email, score))
            db.commit()
            cursor.close()
            db.close()
            return render_template('result.html', username=username, decimalScore=round(decimalScore), score=score, maxscore=round(decimalScore))


