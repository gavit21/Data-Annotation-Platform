from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import Database

app = Flask(__name__, static_folder='static')
app.secret_key = '48e95fd3df11fe0e7feafa71193733995f4c21663112faa5235b35ebae0c8a9c'  # Secret key for session management
dbo = Database()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/perform_registration', methods=['POST'])
def perform_registration():
    name = request.form.get('user_name')
    roll_no = request.form.get('roll_no')
    email = request.form.get('user_email')
    password = request.form.get('user_password')

    if not name or not email or not password:
        flash("All fields are required.", "danger")
        return redirect(url_for('register'))

    response = dbo.insert_student(name, roll_no, email, password)

    if response == 1:
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('index'))
    else:
        flash("Email already exists or there was an error in registering the user.", "danger")
        return redirect(url_for('register'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if dbo.authenticate(email, password):
        print(f"Login successful for {email}")
        session['user_email'] = email
        return redirect('/profile')
    else:
        print(f"Login failed for {email}")
        flash("Invalid email or password.", "danger")
        return redirect(url_for('index'))


@app.route('/profile')
def profile():
    if 'user_email' not in session:
        return redirect(url_for('index'))

    student_id = dbo.get_student_id(session['user_email'])
    memes = dbo.get_assigned_memes(student_id)
    
    return render_template('profile.html', memes=memes)


@app.route('/rate_meme', methods=['POST'])
def rate_meme():
    if 'user_email' not in session:
        return redirect(url_for('index'))

    meme_id = request.form.get('meme_id')
    rating = request.form.get('rating')
    comment_1= request.form.get('comment')
    classification_1 = request.form.get('classification')
    student_id = dbo.get_student_id(session['user_email'])

    dbo.submit_rating(student_id, meme_id, rating, comment_1, classification_1)
    return redirect('/profile')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
