import requests
import json
import pycountry
from datetime import datetime


class Vk():
    def __init__(self, access_token):
        # data = requests.post(
        #     f"https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username={login}&password={password}")
        # parsed_data = json.loads(data.content)
        # print(data.content)
        # self.access_token = parsed_data['access_token']
        self.access_token = access_token
        if self.access_token:
            print(f'Account was succesfully connected!')

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

    def get_all_statistic(self, domain, count):
        data = json.loads(self.get_posts(domain, count))
        result = {
            "dates": [],
            "likes": [],
            "comments": [],
            "reposts": [],
            "views": [],
            "labels": []
        }
        average = [0, 0, 0, 0]  # likes, comments, reposts, views
        for i in data['response']['items']:
            print(i['date'])
            result["dates"].append(i['date'] * 1000)
            result["likes"].append(i['likes']['count'])
            result["comments"].append(i['comments']['count'])
            result["reposts"].append(i['reposts']['count'])
            result["views"].append(i['views']['count'])
            result["labels"].append('https://vk.com/wall' + str(i['owner_id']) + '_' + str(i['id']))
            average[0] += i['likes']['count']
            average[1] += i['comments']['count']
            average[2] += i['reposts']['count']
            average[3] += i['views']['count']

        items_col = len(data['response']['items'])
        for i in range(4):
            average[i] //= items_col

        return (average, result)

    def get_countries(self, domain, count=1000):
        data = requests.get("https://api.vk.com/method/groups.getMembers", params={
            "access_token": self.access_token,
            "group_id": domain,
            "count": count,
            "lang": "en",
            "fields": "country",
            "v": "5.103"
        })
        raw = {}
        data = json.loads(data.content)['response']
        for i in data['items']:
            if 'country' in i:
                if i['country']['title'] == 'Russia': i['country']['title'] = 'Russian Federation'
                if i['country']['title'] == 'USA': i['country']['title'] = 'United States'
                if i['country']['title'] == 'Falkland Islands': i['country']['title'] = 'Falkland Islands (Malvinas)'
                if i['country']['title'] in raw:
                    raw[i['country']['title']] += 1
                else:
                    raw[i['country']['title']] = 1
        result = []
        print(raw)
        for i in list(raw):
            print(i)
            result.append({
                "id": pycountry.countries.get(name=i).alpha_2,
                "name": i,
                "value": raw[i]
            })
        return result
