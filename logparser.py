# Parse the log file using the search terms in the list
# Write results to a separate file

search_terms = ["wlan0: Associated with", "wlan0: State", "wlan0: CTRL-EVENT",
                "wlan0: Considering connect", "wlan0: Request", "selected BSS"]
#search_terms = ["wpa_supplicant"]


filename_final = './logfile_parsed.txt'
logfile = './log.txt'
ff = open(filename_final, 'w')

print('parsing logfile...')
with open(logfile) as f:
    for line in f:
        if any(s in line for s in search_terms):
             ff.write(line)

print('finished')             
ff.close()
