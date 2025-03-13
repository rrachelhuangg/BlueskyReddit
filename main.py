import requests

from flask import Flask, render_template
from methods import get_refresh_token, get_access_token

app = Flask(__name__)

@app.route("/")
def home():
    refresh_token = get_refresh_token('demo-bluesky-acc.bsky.social', 'Bluesky#1!')
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
    return render_template("index.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True)