import requests
import json
import os

from flask import Flask, request, render_template, session
from flask_cors import CORS
from methods import get_refresh_token, get_access_token

app = Flask(__name__)
app.secret_key="SECRETKEY"
CORS(app)

def append_skeet_storage(file_name, handle, data):
    temp_file_path = os.path.join("/tmp", file_name)
    try:
        with open(temp_file_path, "r") as file:
            file_data = json.load(file)
    except: 
        file_data = {}
    file_data[handle] = data
    with open(temp_file_path, "w") as file:
        json.dump(file_data, file, indent = 4)

def check_duplicate(file_name, handle):
    temp_file_path = os.path.join("/tmp", file_name)
    try:
        with open(temp_file_path, "r") as file:
            file_data = json.load(file)
            for h in file_data:
                if handle == h:
                    return True
        return False
    except:
        return False

def load_posts(file_name):
    posts = []
    temp_file_path = os.path.join("/tmp", file_name)
    try:
        with open(temp_file_path, "r") as file:
            file_data = json.load(file)
            for handle in file_data:
                for post in file_data[handle]:
                    posts += [post]
    except:
        return []
    return posts

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def access_login_info():
    session['added_accounts'] = []
    if 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        refresh_token = get_refresh_token(username, password)
        access_token = get_access_token(refresh_token)
        session['access_token'] = access_token
        handle = "demo-bluesky-acc.bsky.social"
        url = f'https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed?actor={handle}&limit={100}'
        headers = {
            'Authorization':f"Bearer {access_token}",
            'Content-Type':'application/json'
        }
        response = requests.get(url, headers=headers, timeout=15)
        posts = []
        for i in range(len(response.json()['feed'])):
            post = {}
            post['name'] = response.json()['feed'][i]['post']['author']['displayName']
            post['handle'] = response.json()['feed'][i]['post']['author']['handle']
            post['text_content'] = response.json()['feed'][i]['post']['record']['text']
            post['reply_count'] = response.json()['feed'][i]['post']['replyCount']
            post['repost_count'] = response.json()['feed'][i]['post']['repostCount']
            post['like_count'] = response.json()['feed'][i]['post']['likeCount']
            posts += [post]
        return render_template("postlogin.html", posts=posts)
    elif 'account' in request.form:
        access_token = session['access_token']
        handle = request.form['account']
        session['added_accounts'] += [handle] #should implement some sort of a cache to speed things up!
        for handle in session['added_accounts']:
            url = f'https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed?actor={handle}&limit={100}'
            headers = {
                'Authorization':f"Bearer {access_token}",
                'Content-Type':'application/json'
            }
            response = requests.get(url, headers=headers, timeout=15)
            posts = []
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
            if not check_duplicate("skeets.json", handle):
                append_skeet_storage("skeets.json", handle, posts)
        posts = load_posts("skeets.json")
        return render_template("postlogin.html", posts=posts)
    else:
        return render_template("postlogin.html")

if __name__ == "__main__": #can remove after final version is deployed (only for testing rn)
    app.run(debug=True)