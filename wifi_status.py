class WifiStatus:
	def __init__(self):
		self.state = 0
		self.info = ""
		self.SSID = ""
		self.mac = ""
		
	def setSSID(self, ssid):
		self.SSID = ssid
	
	def updateState(self, new_state, inf):
		self.state = new_state
		self.info = inf

	def getState(self):
		return self.state

	def getStateString(self):
		if self.state == 0:
			return "Associated with: " + self.info
		elif self.state == 1:
			return "State: " + self.info
		elif self.state == 2:
			return "Control Event: " + self.info
		elif self.state == 3:
			return "Considering connect: " + self.info
		elif self.state == 4:
			return "Request: " + self.info
		elif self.state == 5:
			return "Selected BSS: " + self.info
		else:
			return "Error: unkown state"
