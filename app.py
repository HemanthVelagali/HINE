from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

# Secret key for session management (for flash messages, etc.)
app.secret_key = 'your_secret_key'

# Sample data for login validation (this should be replaced by a database or authentication system)
users = {
    'testuser': 'password123'
}

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate login credentials
        if username in users and users[username] == password:
            flash("Login Successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials, please try again.", "error")
    
    return render_template('index.html')

# Dashboard route (protected page after successful login)
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Route to toggle dark mode
@app.route('/toggle_dark_mode', methods=['POST'])
def toggle_dark_mode():
    # Toggle dark mode via session or other method
    dark_mode = request.form.get('dark_mode', 'false')
    if dark_mode == 'true':
        return render_template('index.html', dark_mode=True)
    else:
        return render_template('index.html', dark_mode=False)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
