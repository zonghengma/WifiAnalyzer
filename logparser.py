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
			start_index = line.find(self.search_terms[i])
			if start_index != -1 and self.status.updateState(i, line[start_index + len(self.search_terms[i]): ]):
				return self.status.getStateString() 
	#			
        #if any(s in line for s in self.search_terms):
        #    return(line)
		return None
