#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import json
from urllib import parse
from flask import Flask, request, jsonify, render_template

from query import Query

# init flask app and env variables
app = Flask(__name__)

query_engine = Query()

app.debug = True


@app.route("/", methods=['GET'])
def search():
    """
    URL : /
    Query engine to find a list of relevant URLs.
    Method : POST or GET (no query)
    Form data :
        - query : the search query
        - hits : the number of hits returned by query
        - start : the start of hits
    Return a template view with the list of relevant URLs.
    """
    # GET data
    query_term = request.args.get("query", None)
    page_num = request.args.get("page_num", 1, type=int)
    page_len = request.args.get("page_len", 10, type=int)
    sort_type = request.args.get("sort", 1, type=int)
    similar = request.args.get("similar", False, type=bool)
    if page_num < 0 or page_len < 0:
        return "Error, start or hits cannot be negative numbers"

    if similar:
        url = request.args.get("url", 1, type=str)
        data = query_engine.search_more_like_this(
            url=url, fieldname="content", top=10)
        range_pages = [1]

        # show the list of matching results
        return render_template('spatial/index.html', query=query_term,
                               # response_time=r.elapsed.total_seconds(),
                               response_time=0.1,
                               total=data["total"],
                               page_len=page_len,
                               page_num=page_num,
                               range_pages=range_pages,
                               results=data["results"],
                               maxpage=1,
                               similar=True)
    elif query_term:
        # query search engine

        data, time  = query_engine.query_page(
            query_term, page_num, page_len, sort_type)

        recom_search = query_engine.get_recommend_query(query_term)

        i = page_num
        maxi = 1+int(data["total"]/page_len)
        range_pages = range(
            i-5, i+5 if i+5 < maxi else maxi) if i >= 6 else range(1, maxi+1 if maxi < 10 else 10)

        # show the list of matching results
        return render_template('spatial/index.html', query=query_term,
                               # response_time=r.elapsed.total_seconds(),
                               response_time=time,
                               total=data["total"],
                               page_len=page_len,
                               page_num=page_num,
                               range_pages=range_pages,
                               results=data["results"],
                               maxpage=maxi,
                               recommends=recom_search,
                               sort_type=sort_type)
    else:  # retrun home page with hot news
        
        data = query_engine.recommend_news()

        # show the list of matching results
        return render_template('spatial/index.html',
                               # response_time=r.elapsed.total_seconds(),
                               results=data["results"]
                               )


@app.route("/reference", methods=['POST'])
def reference():
    """
    URL : /reference
    Request the referencing of a website.
    Method : POST
    Form data :
        - url : url to website
        - email : contact email
    Return homepage.
    """
    # POST data
    data = dict((key, request.form.get(key)) for key in request.form.keys())
    if not data.get("url", False) or not data.get("email", False):
        return "Vous n'avez pas renseigné l'URL ou votre email."

    # query search engine
    try:
        r = requests.post('http://%s:%s/reference' % (host, port), data={
            'url': data["url"],
            'email': data["email"]
        })
    except:
        return "Une erreur s'est produite, veuillez réessayer ultérieurement"

    return "Votre demande a bien été prise en compte et sera traitée dans les meilleurs délais."


# -- JINJA CUSTOM FILTERS -- #
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
