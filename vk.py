import requests
import json
import time


class Vk():
    def __init__(self, login, password):
        data = requests.post(
            f"https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username={login}&password={password}")
        parsed_data = json.loads(data.content)
        self.access_token = parsed_data['access_token']
        if self.access_token:
            print(f'Account was succesfully connected! - {parsed_data["user_id"]}')

    def get_profile_info(self, screenname):
        req = requests.get('https://api.vk.com/method/groups.getById', params={
            'group_id': screenname,
            'access_token': self.access_token,
            'v': '5.103'
        })
        print(req.content)
        data = json.loads(req.content)
        return (data['response'][0]['name'], data['response'][0]['photo_50'])

    def get_posts(self, domain, count):
        req = requests.get('https://api.vk.com/method/wall.get', params=
        {'access_token': self.access_token,
         'domain': domain,
         'count': count,
         'v': '5.103'})
        return req.content

    def get_average_posts_data(self, domain, count):
        data = json.loads(self.get_posts(domain, count))
        print(data)
        average = [0, 0, 0, 0]  # likes, comments, reposts, views
        for i in data['response']['items']:
            average[0] += i['likes']['count']
            average[1] += i['comments']['count']
            average[2] += i['reposts']['count']
            average[3] += i['views']['count']

        items_col = len(data['response']['items'])
        for i in range(4):
            average[i] //= items_col
        return average

    def get_all_statistic(self, domain, count):
        data = json.loads(self.get_posts(domain, count))
        result = []
        average = [0, 0, 0, 0]  # likes, comments, reposts, views
        for i in data['response']['items']:
            result.append({"date": time.ctime(i["date"]),
                           "likes": i['likes']['count'],
                           "comments": i['comments']['count'],
                           "reposts": i['reposts']['count'],
                           "views": i['views']['count']
                           })
            average[0] += i['likes']['count']
            average[1] += i['comments']['count']
            average[2] += i['reposts']['count']
            average[3] += i['views']['count']

        items_col = len(data['response']['items'])
        for i in range(4):
            average[i] //= items_col

        return (average, result)
