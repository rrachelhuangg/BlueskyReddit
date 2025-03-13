import requests

from flask import Flask, render_template
from methods import get_refresh_token, get_access_token

app = Flask(__name__)

@app.route("/")
def home():
    refresh_token = get_refresh_token('demo-bsky-reddit.bsky.social', 'Bluesky#1!')
    access_token = get_access_token(refresh_token)
    handle = "demo-bsky-reddit.bsky.social"
    url = f'https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed?actor={handle}&limit={100}'
    headers = {
        'Authorization':f"Bearer {access_token}",
        'Content-Type':'application/json'
    }
    response = requests.get(url, headers=headers, timeout=15)

    posts = []
    for i in range(10):
        post = {}
        post['handle'] = response.json()['feed'][0]['post']['author']['handle']
        post['text_content'] = response.json()['feed'][0]['post']['record']['text']
        post['reply_count'] = response.json()['feed'][0]['post']['replyCount']
        post['repost_count'] = response.json()['feed'][0]['post']['repostCount']
        post['like_count'] = response.json()['feed'][0]['post']['likeCount']
        posts += [post]
    return render_template("index.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True)