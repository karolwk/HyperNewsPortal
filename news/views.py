from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import View
from hypernews.settings import NEWS_JSON_PATH
from datetime import datetime
import random
import json
import re

def open_json() -> list:
    with open(NEWS_JSON_PATH, 'r') as json_file:
        news_list = json.load(json_file)
    return news_list


def save_to_json(js_list) -> None:
    with open(NEWS_JSON_PATH, 'w') as json_file:
        json.dump(js_list, json_file)


def search_results(search_string: str, dict_) -> []:
    # Returns new list with dictionaries matching search results
    search_string = search_string.lower()
    search_result = []
    for key in dict_:
        if re.search(f'.*{search_string}.*', key['title'].lower()):
            search_result.append(key)
    return search_result


class ComingSoon(View):
    def get(self, response, *args, **kwargs):
        return redirect('/news/')


class MainPage(View):
    def get(self, response, *args, **kwargs):
        # Removing hour format from 'created' key example output will be: '2020-02-22'
        temp_dict = open_json().copy()
        for date in temp_dict:
            date['created'] = date['created'][0:10]
        if response.GET.get('q'):
            temp_dict = search_results(response.GET.get('q'), temp_dict)
            return render(response, "news/index.html", context={'links': temp_dict})
        return render(response, "news/index.html", context={'links': temp_dict})


class CreateNews(View):
    def get(self, response, *args, **kwargs):
        return render(response, "news/create.html")

    def post(self, request, *args, **kwargs):
        js_to_save = open_json()
        js_to_save.append({'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                           'text': request.POST.get('text'),
                           'title': request.POST.get('title'),
                           'link': random.randint(1, 100000)})
        save_to_json(js_to_save)
        return redirect('/news/')


class NewPost(View):
    def get(self, response, news_id, *args, **kwargs):
        if news_id.isdigit():
            for news in open_json():
                print(news['link'])
                if news['link'] == int(news_id):
                    return HttpResponse(f"<h2>{news['title']}</h2><p>{news['created']}</p><p>{news['text']}</p>"
                                        f'<a target="_blank" href="/news/">Back to news page!</a>')
        raise Http404
