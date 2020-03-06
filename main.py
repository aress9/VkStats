from flask import Flask, render_template, request
from vk import Vk
import json

app = Flask(__name__, static_folder='static/')

with open('secret.json', 'r') as file:
    secret = json.loads(file.read())
    vk = Vk(secret['login'], secret['password'])

@app.route('/')
@app.route('/index')
def index():
    return app.send_static_file('index.html')


@app.route('/stat')
def stat():
    group = request.args.get('group')
    average = vk.get_average_posts_data(group, 100)
    return render_template('index.html', likes=average[0],
                           comments=average[1],
                           reposts=average[2],
                           views=average[3])


if __name__ == '__main__':
    app.run('127.0.0.1', 80)
