import requests
import json
import os
from upstash_redis import Redis

from flask import Flask, request, render_template, session, jsonify
from flask_cors import CORS
from methods import get_refresh_token, get_access_token

redis_client = Redis(url="https://caring-jaguar-31380.upstash.io", token="AXqUAAIjcDEwMTcwODliMGNjMDc0ZTgwOWIzMDhlOTExMTEwM2MzZnAxMA")

app = Flask(__name__)
app.secret_key="SECRETKEY"
CORS(app)

#should move these to methods eventually
def append_skeet_storage(handle, data):
    data_dump = json.dumps(data)
    redis_client.set(handle, data_dump)

def check_duplicate(handle):
    return redis_client.exists(handle)

def load_posts():
    posts = []
    for handle in redis_client.keys("*"):
        posts_data = redis_client.get(handle)
        if posts_data:
            posts += json.loads(posts_data)
    return posts


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def access_login_info():
    session['added_accounts'] = []
    redis_client.flushdb()
    if 'username' in request.form and 'password' in request.form:
        redis_client.flushdb()
        username = request.form['username']
        password = request.form['password']
        refresh_token = get_refresh_token(username, password)
        access_token = get_access_token(refresh_token)
        session['access_token'] = access_token
        return render_template("postlogin.html")

@app.route("/get_posts", methods=["POST"])
def get_posts():
    data = request.get_json()
    handles = data['handles']
    posts = fetch_data(handles)
    return posts

def fetch_data(handles):
    access_token = session['access_token']
    posts = []
    for handle in handles:
        if handle not in session['added_accounts']:
            session['added_accounts'] += [handle]
        url = f'https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed?actor={handle}&limit={100}'
        headers = {
            'Authorization':f"Bearer {access_token}",
            'Content-Type':'application/json'
        }
        response = requests.get(url, headers=headers, timeout=15)
        for i in range(len(response.json()['feed'])):
            post = {}
            if response.json()['feed'][i]['post']['author']['handle'] == handle: #filtering out random posts??
                post['name'] = response.json()['feed'][i]['post']['author']['displayName']
                post['handle'] = response.json()['feed'][i]['post']['author']['handle']
                post['text_content'] = response.json()['feed'][i]['post']['record']['text']
                post['reply_count'] = response.json()['feed'][i]['post']['replyCount']
                post['repost_count'] = response.json()['feed'][i]['post']['repostCount']
                post['like_count'] = response.json()['feed'][i]['post']['likeCount']
                posts += [post]
        if not check_duplicate(handle):
            append_skeet_storage(handle, posts)
    return posts

if __name__ == "__main__": #can remove after final version is deployed (only for testing rn)
    app.run(debug=True)