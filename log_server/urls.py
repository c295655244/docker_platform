from views import *

patterns = [
    (r"/", Index),
    (r"/(.*)/(.*)", GetFile),
]

settings = dict(
	debug=True,
)