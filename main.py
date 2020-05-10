from flask import Flask, render_template, request, Blueprint
from vk import Vk
import json

main = Blueprint('main', __name__)

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
    count = request.args.get('count')
    if 'vk.com' in group:
        group = group[group.index('/')]
    group_name, group_image = vk.get_profile_info(group)
    average, data = vk.get_all_statistic(group, int(count))
    map_data = vk.get_countries(group)
    return render_template('index.html', likes=average[0],
                           comments=average[1],
                           reposts=average[2],
                           views=average[3],
                           group=group,
                           group_name=group_name,
                           group_image=group_image,
                           likes_data=data['likes'],
                           comments_data=data['comments'],
                           reposts_data=data['reposts'],
                           views_data=data['views'],
                           time_data=data['dates'],
                           map_data=map_data
                           )


if __name__ == '__main__':
    app.run('127.0.0.1', 80)
