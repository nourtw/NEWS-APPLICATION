from flask import Flask, render_template, request
from newsapi import NewsApiClient
from flask_paginate import Pagination

newsappflask = Flask(__name__, static_folder='static')
api_key = "f6f88f75eecf48dd977460736881dbec"
newsapi = NewsApiClient(api_key)

def get_articles_from_source(source_id):
    articles = []
    desc = []
    img = []
    newsapi = NewsApiClient(api_key)
    top_headlines = newsapi.get_top_headlines(sources=source_id)
    if 'articles' in top_headlines:
        for article in top_headlines['articles']:
            articles.append(article['title'])
            desc.append(article['description'])
            img.append(article['urlToImage'])
    return articles, desc, img

@newsappflask.route('/search')
def search():
    query = request.args.get('query')
    if query:
        all_articles = newsapi.get_everything(q=query)
        articles = all_articles['articles']
    else:
        articles = []
    return render_template('search.html', articles=articles)

@newsappflask.route('/news/<int:page>')
def news(page=1):
    per_page = 10
    offset = (page - 1) * per_page
    all_articles = newsapi.get_everything()
    total_articles = len(all_articles['articles'])
    articles = all_articles['articles'][offset:offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total_articles, css_framework='bootstrap4')
    return render_template('pagination.html', articles=articles, pagination=pagination)

@newsappflask.route('/bbc')
def bbc(page=1):
    source_id = "bbc-news" 
    articles, desc, img = get_articles_from_source(source_id)
    pagination = Pagination(page=page, per_page=10, total=len(articles), css_framework='bootstrap4')
    return render_template('bbc.html', articles=articles, desc=desc, img=img, pagination=pagination)

@newsappflask.route('/argaam')
def argaam(page=1):
    source_id = "argaam" 
    articles, desc, img = get_articles_from_source(source_id)
    pagination = Pagination(page=page, per_page=10, total=len(articles), css_framework='bootstrap4')
    return render_template('argaam.html', articles=articles, desc=desc, img=img, pagination=pagination)

@newsappflask.route('/aljazeera')
def aljazeera(page=1):
    source_id = "al-jazeera-english"
    articles, desc, img = get_articles_from_source(source_id)
    pagination = Pagination(page=page, per_page=10, total=len(articles), css_framework='bootstrap4')
    return render_template('aljazeera.html', articles=articles, desc=desc, img=img, pagination=pagination)

@newsappflask.route('/')
def index():
    source_id = "abc-news-au" 
    articles, desc, img = get_articles_from_source(source_id)
    mylist = zip(articles, desc, img)
    return render_template('index.html', context=mylist)

if __name__ == "__main__":
    newsappflask.run(debug=True)
