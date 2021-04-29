from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Vivek'}
    return render_template('index.html', title='Home', user=user)


@app.route('/if')
def conditional():
    user = {'username': 'Vivek'}
    return render_template('conditional.html', user=user)


@app.route('/loop')
def posts():
    user = {'username': 'Vivek'}
    posts = [
        {
            'author': {'username': 'Abey'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Seán'},
            'body': 'The All-Blacks win again!'
        }
    ]
    return render_template('loops.html', title='Home', user=user, posts=posts)


@app.route('/template')
def inherit():
    user = {'username': 'Vivek'}
    posts = [
        {
            'author': {'username': 'Abey'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Seán'},
            'body': 'The All-Blacks win again!'
        }
    ]
    return render_template('extended.html', title='Home', user=user, posts=posts)


if __name__ == '__main__':
    app.run()
