from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)

GITHUB_API = "https://api.github.com"


@app.route('/<username>', methods=['GET'])
def user_gists(username):
    """Return the public gists for the specified GitHub username.

    Proxies the GitHub API: GET /users/{username}/gists
    """
    # Pagination
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=30, type=int)
    params = {'page': page, 'per_page': per_page}

    # Simple in-memory cache: { (username, page, per_page): (timestamp, data) }
    if not hasattr(app, '_gist_cache'):
        app._gist_cache = {}
    cache = app._gist_cache
    cache_key = (username, page, per_page)
    now = time.time()
    CACHE_TTL = 60  # seconds
    cached = cache.get(cache_key)
    if cached and now - cached[0] < CACHE_TTL:
        return jsonify(cached[1])

    url = f"{GITHUB_API}/users/{username}/gists"
    try:
        resp = requests.get(url, params=params, timeout=5)
    except requests.RequestException as e:
        return jsonify({"error": "upstream_error", "message": str(e)}), 502

    if resp.status_code == 404:
        return jsonify({"error": "not_found", "message": f"user {username} not found"}), 404

    try:
        data = resp.json()
    except ValueError:
        return jsonify({"error": "invalid_response", "message": "GitHub returned non-json"}), 502

    cache[cache_key] = (now, data)
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
