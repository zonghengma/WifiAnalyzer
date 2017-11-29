# Parse the log file using the search terms in the list
# Write results to a separate file
class LogParser:
    def __init__(self):
        self.search_terms = ["wlan0: Associated with", "wlan0: State", "wlan0: CTRL-EVENT","wlan0: Considering connect", "wlan0: Request", "selected BSS"]
    #search_terms = ["wpa_supplicant"]
    
    def parse(self, line):
        if any(s in line for s in self.search_terms):
            return(line)
        return ""
