from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/runandresult")
def runandresult():
    return render_template('runandresult.html')

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

@app.route("/acknowledgement")
def acknowledgement():
    return render_template('acknowledgement.html')

if __name__ == '__main__':
    app.run(debug=True)
