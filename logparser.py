import wifi_status
# Parse the log file using the search terms in the list
# Write results to a separate file
class LogParser:
	def __init__(self):
		self.search_terms = ["Associated with", "State", "CTRL-EVENT","Considering connect", "Request", "selected BSS"]
		self.status = wifi_status.WifiStatus();
    #search_terms = ["wpa_supplicant"]

	def parse(self, line):
		for i in range(len(self.search_terms)):
			if self.search_terms[i] in line and self.status.updateState(i, line):
				return self.status.getStateString() 
	#			
        #if any(s in line for s in self.search_terms):
        #    return(line)
		return None
