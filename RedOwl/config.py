import configparser

class ConfigurationReader():
	
	def __init__(self):
		self._config = configparser.ConfigParser()
		
	def __init__(self, file):
		self._config = configparser.ConfigParser()
		self.read( file)
	
	def read(self):
		self.read('redowl.conf')
		
	def read(self, file):
		self._config.read(file)
		
		#Read Server parameters
		server_conf = self._config['server']
		self._auth_token = server_conf['refresh_token']
		self._conversation_id = server_conf['conversation_id']
		