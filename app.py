from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__, template_folder='.')

DATA_FILE = 'data.json'


def load_data():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return {'classes': [], 'assignments': [], 'completed': []}


def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)


@app.route('/')
def index():
    data = load_data()

    # Calculate remaining days for each assignment and format due date
    for assignment in data['assignments']:
        due_date = datetime.strptime(assignment['due_date'], '%Y-%m-%d')
        remaining_days = (due_date - datetime.now()).days
        assignment['remaining_days'] = remaining_days

        # Calculate remaining days for completed assignments
    for assignment in data['completed']:
        due_date = datetime.strptime(assignment['due_date'], '%Y-%m-%d')
        remaining_days = (due_date - datetime.now()).days
        assignment['remaining_days'] = remaining_days

    save_data(data)  # Save updated data

    return render_template('index.html', data=data)


@app.route('/add_assignment', methods=['POST'])
def add_assignment():
    class_name = request.form['class']
    title = request.form['title']
    due_date = request.form['due_date']
    description = request.form['description']

    new_assignment = {'class': class_name, 'title': title, 'due_date': due_date, 'description': description}

    data = load_data()
    data['assignments'].append(new_assignment)
    save_data(data)

    return redirect(url_for('index'))


@app.route('/mark_as_submitted/<int:index>', methods=['POST'])
def mark_as_submitted(index):
    data = load_data()
    assignment = data['assignments'][index]
    data['completed'].append(assignment)
    data['assignments'].pop(index)
    save_data(data)
    return redirect(url_for('index'))


@app.route('/unsubmit_assignment/<int:index>', methods=['POST'])
def unsubmit_assignment(index):
    data = load_data()
    assignment = data['completed'][index]
    data['assignments'].append(assignment)
    data['completed'].pop(index)
    save_data(data)
    return redirect(url_for('index'))


@app.route('/delete_assignment/<int:index>', methods=['POST'])
def delete_assignment(index):
    data = load_data()
    del data['assignments'][index]
    save_data(data)
    return redirect(url_for('index'))


@app.route('/delete_completed_assignment/<int:index>', methods=['POST'])
def delete_completed_assignment(index):
    data = load_data()
    del data['completed'][index]
    save_data(data)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False)
