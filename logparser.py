# Parse the log file using the search terms in the list
# Write results to a separate file
class LogParser:
    def __init__(self):
        self.search_terms = ["Associated with", "State", "CTRL-EVENT","Considering connect", "Request", "selected BSS"]
    #search_terms = ["wpa_supplicant"]
    
    def parse(self, line):
        if any(s in line for s in self.search_terms):
            return(line)
        return ""
