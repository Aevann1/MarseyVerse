import gevent.monkey
gevent.monkey.patch_all()
from os import environ
import secrets
from flask import *
from flask_caching import Cache
from flask_limiter import Limiter
from flask_compress import Compress
from flask_limiter.util import get_ipaddr
import requests
import time
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, template_folder='./templates')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=3)
app.url_map.strict_slashes = False
app.jinja_env.auto_reload = True

app.config['SECRET_KEY'] = environ.get('MASTER_KEY')
app.config["SERVER_NAME"] = "marseyverse.xyz"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 86400
app.config["SESSION_COOKIE_NAME"] = "session_marseyverse"
app.config["VERSION"] = "1.0.0"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["SESSION_COOKIE_SECURE"] = 1
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = 60 * 60 * 24 * 365
app.config["SESSION_REFRESH_EACH_REQUEST"] = True
app.config["FORCE_HTTPS"] = 1
app.jinja_env.cache = {}
app.config["CACHE_TYPE"] = "filesystem"
app.config["CACHE_DIR"] = "cache"
app.config["RATELIMIT_KEY_PREFIX"] = "flask_limiting_"
app.config["RATELIMIT_ENABLED"] = True
app.config["RATELIMIT_DEFAULTS_DEDUCT_WHEN"]=lambda:True
app.config["RATELIMIT_DEFAULTS_EXEMPT_WHEN"]=lambda:False
app.config["RATELIMIT_HEADERS_ENABLED"]=True

cache = Cache(app)
Compress(app)

limiter = Limiter(
	app,
	key_func=get_ipaddr,
	default_limits=["100/minute"],
	headers_enabled=True,
	strategy="fixed-window"
)




@app.before_request
def before_request():

	g.timestamp = int(time.time())

	if not request.path.startswith("/assets"):
		session.permanent = True

		if not session.get("session_id"): session["session_id"] = secrets.token_hex(16)


	if app.config["FORCE_HTTPS"] and request.url.startswith(
			"http://") and "localhost" not in app.config["SERVER_NAME"]:
		url = request.url.replace("http://", "https://", 1)
		return redirect(url, code=301)

	ua=request.headers.get("User-Agent","")
	if "CriOS/" in ua: g.system="ios/chrome"
	elif "Version/" in ua: g.system="android/webview"
	elif "Mobile Safari/" in ua: g.system="android/chrome"
	elif "Safari/" in ua: g.system="ios/safari"
	elif "Mobile/" in ua: g.system="ios/webview"
	else: g.system="other/other"

@app.after_request
def after_request(response):

	response.headers.add("Strict-Transport-Security", "max-age=31536000")
	response.headers.add("Referrer-Policy", "same-origin")
	response.headers.add("X-Frame-Options", "deny")

	return response


class Post(object):
      
    def __init__(self, my_dict):
          
        for key in my_dict:
            setattr(self, key, my_dict[key])

@cache.memoize(timeout=3600)
def postcache():
	count = 0
	drama = requests.get("https://rdrama.net/", headers={"Authorization": "sex"}).json()["data"]
	vidya = requests.get("https://vidya.cafe/", headers={"Authorization": "sex"}).json()["data"]
	# pcm = requests.get("https://pcmemes.net/", headers={"Authorization": "sex"}).json()["data"]
	gigachad = requests.get("https://gigachadlife.com/", headers={"Authorization": "sex"}).json()["data"]
	weebzone = requests.get("https://weebzone.xyz/", headers={"Authorization": "sex"}).json()["data"]
	dankchristian = requests.get("https://dankchristian.com/", headers={"Authorization": "sex"}).json()["data"]
	listing = []

	while count < 50:
		# for site in [drama,vidya,pcm,gigachad,weebzone,dankchristian]:
		for site in [drama,vidya,gigachad,weebzone,dankchristian]:
			try: post = site[count]
			except: continue
			post = Post(post)
			if hasattr(post, "url") and post.url and (post.url.lower().endswith('.jpg') or post.url.lower().endswith('.png') or post.url.lower().endswith('.webp') or post.url.lower().endswith('.gif') or post.url.lower().endswith('.jpeg') or post.url.lower().endswith('?maxwidth=9999')): post.is_image = True
			if site == drama: post.site = "rdrama.net"
			# elif site == pcm: post.site = "pcmemes.net"
			elif site == gigachad: post.site = "gigachadlife.com"
			elif site == weebzone: post.site = "weebzone.xyz"
			elif site == dankchristian:
				post.site = "dankchristian.com"
				post.downvotes = 0
			elif site == vidya:
				post.site = "vidya.cafe"
				post.downvotes = 0

			if post.club or not hasattr(post, "upvotes") or not hasattr(post, "downvotes"): continue
			if time.time() - post.created_utc < 86400: listing.append(post)
		count += 1

	return listing

@app.get("/dump")
def dump():
	cache.clear()
	return {"message": "Internal cache cleared."}

@app.get("/")
def marseyverse():
	return render_template("marseyverse.html", listing=postcache())

@app.get("/assets/favicon.ico")
def favicon():
	return send_file(f"./assets/icon.gif")

@app.route('/assets/<path:path>')
@limiter.exempt
def static_service(path):
	resp = make_response(send_from_directory('./assets', path))
	if request.path.endswith('.gif') or request.path.endswith('.ttf') or request.path.endswith('.woff') or request.path.endswith('.woff2'):
		resp.headers.remove("Cache-Control")
		resp.headers.add("Cache-Control", "public, max-age=2628000")

	return resp