from files.helpers.wrappers import *
from files.__main__ import app

class Post(object):
      
    def __init__(self, my_dict):
          
        for key in my_dict:
            setattr(self, key, my_dict[key])

@app.get("/")
def marseyverse(v):
	count = 0
	drama = requests.get("https://rdrama.net/", headers={"Authorization": "sex"}).json()["data"]
	pcm = requests.get("https://pcmemes.net/", headers={"Authorization": "sex"}).json()["data"]
	gigachad = requests.get("https://gigachadlife.com/", headers={"Authorization": "sex"}).json()["data"]
	weebzone = requests.get("https://weebzone.xyz/", headers={"Authorization": "sex"}).json()["data"]

	listing = []

	while count < 100:
		for site in [drama,pcm,gigachad,weebzone]:
			try: post = site[count]
			except: continue
			listing.append(Post(post))
		count += 1

	return render_template("marseyverse.html", v=v, listing=listing)