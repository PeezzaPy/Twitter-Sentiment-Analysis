from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/success/<username>')
def success(username):
    return render_template('hello.html', name=username)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['nm']
        return redirect(url_for('success', username=username))
    else:
        username = request.args.get('nm')
        return redirect(url_for('success', username=username))

if __name__ == '__main__':
    app.run(debug=True)
