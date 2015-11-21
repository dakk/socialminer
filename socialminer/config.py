from colorlog import ColoredFormatter
import logging


formatter = ColoredFormatter(
	'%(log_color)s[%(asctime)-8s] %(module)s: %(message_log_color)s%(message)s',
	datefmt=None,
	reset=True,
	log_colors = {
		'DEBUG':	'blue',
		'REPORT': 'purple',
		'INFO':	 'green',
		'WARNING':  'yellow',
		'ERROR':	'red',
		'CRITICAL': 'red',
	},
	secondary_log_colors={
		'message': {
			'DEBUG':	'purple',
			'REPORT': 'blue',
			'INFO':	 'yellow',
			'WARNING':  'green',
			'ERROR':	'yellow',
			'CRITICAL': 'red',
		}
	},
	style = '%'
)

stream = logging.StreamHandler()
stream.setFormatter(formatter)

logger = logging.getLogger('socialminer')
logger.addHandler(stream)


logging.addLevelName(15, "REPORT")
logging.Logger.pluginfo = lambda self, message, *args, **kws: self._log(15, message, args, **kws) if self.isEnabledFor(15) else None



DATA_DIR = '.'

BASE_CONF = {
    "adapters": {
		"Twitter": {
		    'consumer_key': '',
		    'consumer_secret': '',
		    'access_token': '',
		    'access_token_secret': ''
		},
		"Facebook": {
			'access_token': ''
		}
    },
	"reportservers": [
		{ 'host': '', 'port': '' }
	]
}
