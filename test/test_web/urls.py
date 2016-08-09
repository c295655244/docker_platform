from views import CreateHandler,DeleteHandler,CmdHandler,MonitorHostHandler,MonitorTopoHandler

patterns = [
    (r"/create", CreateHandler),
    (r"/delete", DeleteHandler),
    (r"/cmd", CmdHandler),
    (r"/monitor_host", MonitorHostHandler),
    (r"/monitor_topo", MonitorTopoHandler),
]

settings = dict(
	debug=True,
)