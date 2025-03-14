import requests

from flask import Flask, request, render_template
from methods import get_refresh_token, get_access_token

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def access_login_info():
    if 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        refresh_token = get_refresh_token(username, password)
        access_token = get_access_token(refresh_token)
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
            post['handle'] = response.json()['feed'][i]['post']['author']['handle']
            post['text_content'] = response.json()['feed'][i]['post']['record']['text']
            post['reply_count'] = response.json()['feed'][i]['post']['replyCount']
            post['repost_count'] = response.json()['feed'][i]['post']['repostCount']
            post['like_count'] = response.json()['feed'][i]['post']['likeCount']
            posts += [post]
        return render_template("postlogin.html", posts=posts)
    else:
        return render_template("postlogin.html")

if __name__ == "__main__": #can remove after final version is deployed (only for testing rn)
    app.run(debug=True)