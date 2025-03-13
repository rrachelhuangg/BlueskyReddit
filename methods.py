import requests

def get_access_token(refresh_jwt: str)->str:
    """Uses refresh token to generate BlueskyAPI access token"""
    url = "https://bsky.social/xrpc/com.atproto.server.refreshSession"
    headers = {"Authorization": f"Bearer {refresh_jwt}", "Content-Type":"application/json"}
    response = requests.post(url, headers=headers, timeout=30)
    return response.json().get('accessJwt')

def get_refresh_token(username: str, password: str) -> str:
    """Generate a Bluesky refresh token that is used to generate Bluesky API access tokens"""
    url = "https://bsky.social/xrpc/com.atproto.server.createSession"
    data = {
        'identifier': username,
        'password': password
    }
    response = requests.post(url, json=data, timeout = 30)
    response.raise_for_status()
    return response.json().get('refreshJwt')