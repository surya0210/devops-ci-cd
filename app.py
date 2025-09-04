# app.py

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your__here' # Needed for flashing messages

# A simple list to act as our "database"
workouts = []

@app.route('/')
def index():
    """Renders tthe main page with the workout form."""
    return render_template('index.html', workouts=workouts)

@app.route('/add_workout', methods=['POST'])
def add_workout():
    """Handles adding a new workout."""
    workout = request.form.get('workout')
    duration_str = request.form.get('duration')

    if not workout or not duration_str:
        flash('Please enter both a workout and a duration.', 'error')
        return redirect(url_for('index'))

    try:
        duration = int(duration_str)
        workouts.append({'workout': workout, 'duration': duration})
        flash(f"'{workout}' added successfully!", 'success')
    except ValueError:
        flash('Duration must be a number.', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port= 5001)
