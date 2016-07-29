from views import CreateHandler,DeleteHandler,CmdHandler,MoniterHostHandler,MoniterTopoHandler

patterns = [
    (r"/create", CreateHandler),
    (r"/delete", DeleteHandler),
    (r"/cmd", CmdHandler),
    (r"/moniter_host", MoniterHostHandler),
    (r"/moniter_topo", MoniterTopoHandler),
]

settings = dict(
	debug=True,
)