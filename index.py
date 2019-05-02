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
host = os.getenv("HOST")
port = os.getenv("PORT")

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
    query = request.args.get("query", None)
    start = request.args.get("start", 0, type=int)
    hits = request.args.get("hits", 10, type=int)
    if start < 0 or hits < 0:
        return "Error, start or hits cannot be negative numbers"

    if query:
        # query search engine
        try:
            data = query_engine.query(query)
        except:
            return "Error, check your installation"

        i = int(start/hits)
        maxi = 1+int(data["total"]/hits)
        range_pages = range(
            i-5, i+5 if i+5 < maxi else maxi) if i >= 6 else range(0, maxi if maxi < 10 else 10)

        # show the list of matching results
        return render_template('spatial/index.html', query=query,
                               # response_time=r.elapsed.total_seconds(),
                               response_time=0.1,
                               total=data["total"],
                               hits=hits,
                               start=start,
                               range_pages=range_pages,
                               results=data["results"],
                               page=i,
                               maxpage=maxi-1)

    # return homepage (no query)
    return render_template('spatial/index.html')


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
