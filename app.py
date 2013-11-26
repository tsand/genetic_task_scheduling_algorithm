from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/schedule')
def schedule():
    # This is where we will take the post and format it in a way that the algorithm will accept
    # Then it will be pased through the algorithm and return the results of the algorithm
    # in a way the the frontend can understand
    return 'Not Implemented'

if __name__ == "__main__":
    app.run()