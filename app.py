from flask import Flask, request, redirect, url_for, session, send_file, send_from_directory
import json, os

app = Flask(__name__)
app.secret_key = 'hine_secret_key'

USER_FILE = 'users.json'

# Load or create user data file
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return send_file('register.html')  # send without template rendering
        users[username] = password
        save_users(users)
        return redirect(url_for('login'))
    return send_file('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('main'))
        else:
            return send_file('login.html')  # fallback on failed login
    return send_file('login.html')

@app.route('/main')
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    return send_file('main.html')

@app.route('/index.css')
def serve_css():
    return send_file('index.css')

@app.route('/main.css')
def serve_main_css():
    return send_file('main.css')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/download/<filename>')
def download(filename):
    if 'username' not in session:
        return redirect(url_for('login'))
    return send_from_directory('downloads', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
