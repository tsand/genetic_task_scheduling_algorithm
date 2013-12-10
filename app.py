from flask import Flask, render_template, request
import json
from time import sleep

import genetic_algorithm

app = Flask(__name__)

COLORS = ['#3498db', '#f1c40f', '#c0392b', '#a061ba', '#e67e22', '#1abc9c']

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.json

    raw_tasks = data.get('tasks')
    tasks = []
    for task in raw_tasks:
        dependencies = task.get('depend')
        if dependencies:
            dependencies = [dependencies]

        t = genetic_algorithm.Task(task.get('id'), task.get('name'), task.get('length'), task.get('priority'), dependencies)
        tasks.append(t)

    # Setup dependencies
    for task in tasks:
        dependencies = []
        for depend_id in task.dependencies:
            for t2 in tasks:
                if t2.identifier == depend_id:
                    dependencies.append(t2)
                    break
            else:
                raise Exception('Invalid dependency')
        task.dependencies = dependencies

    constraints = data.get('constraints')

    processors = constraints.get('processors')
    generations = constraints.get('generations')
    total_time = constraints.get('total_time')

    gen_alg = genetic_algorithm.GeneticTaskScheduler(tasks)
    schedule = gen_alg.schedule_tasks(processors, generations, total_time)

    # Reformat tasks in a way compatible with UI
    for i, processor in enumerate(schedule):
        for j, task in enumerate(processor):
            if task:
                schedule[i][j] = {'name': task.name, 'color': COLORS[task.identifier % len(COLORS)]}
            else:
                schedule[i][j] = None

    return json.dumps(schedule)

if __name__ == "__main__":
    app.run(debug=True)