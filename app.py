from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/image')
def render_example():
    return render_template('index.html', page_type='image')

@app.route('/menu')
def render_menu():
    return render_template('menu.html', page_type='menu')

if __name__ == '__main__':
    app.run("0.0.0.0", port=80)
