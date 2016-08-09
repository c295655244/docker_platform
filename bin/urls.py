from views import *

patterns = [
    (r"/", Index),
    (r"/create", CreateHandler),
    (r"/delete", DeleteHandler),
    (r"/cmd", CmdHandler),
    (r"/monitor_host", MonitorHostHandler),
    (r"/monitor_topo", MonitorTopoHandler),
    (r"/monitor_cluster", MonitorClusterHandler),
    (r"/log_day", LogDayHandler),
    (r"/log_all", LogAllHandler),
    (r"/vnc",VncHandler),    
    (r"/get_image",GetImageHandler),
]

settings = dict(
	debug=True,
)