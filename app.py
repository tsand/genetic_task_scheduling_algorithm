from flask import Flask, render_template, request
import json
from time import sleep

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.json

    tasks = data.get('tasks')
    constraints = data.get('constraints')

    # This is where we will take the post and format it in a way that the algorithm will accept
    # Then it will be pased through the algorithm and return the results of the algorithm
    # in a way the the frontend can understand

    schedule = []

    # Build Schedule
    for processor in range(constraints.get('processors')):
        p_schedule = []
        for time in range(constraints.get('total_time')):
            p_schedule.append({})
        schedule.append(p_schedule)

    # Hard code schedule for testing
    schedule[0][1] = {'name': 'test', 'color': '#3498db'}
    schedule[0][2] = {'name': 'test', 'color': '#3498db'}
    schedule[0][3] = {'name': 'test', 'color': '#3498db'}

    schedule[2][0] = {'name': 'test', 'color': '#f1c40f'}
    schedule[2][1] = {'name': 'test', 'color': '#f1c40f'}
    schedule[2][2] = {'name': 'test', 'color': '#f1c40f'}
    schedule[2][3] = {'name': 'test', 'color': '#f1c40f'}

    schedule[1][0] = {'name': 'test', 'color': '#c0392b'}

    schedule[1][4] = {'name': 'test', 'color': '#8e44ad'}
    schedule[1][5] = {'name': 'test', 'color': '#8e44ad'}
    schedule[1][6] = {'name': 'test', 'color': '#8e44ad'}

    sleep(1)

    return json.dumps(schedule)

if __name__ == "__main__":
    app.run(debug=True)