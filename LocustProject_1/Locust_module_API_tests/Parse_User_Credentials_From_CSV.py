from locust import User, constant, os
import csv

USER_CREDENTIALS = {}

class LoginWithCredsFromCSV(User):
    
    def readCredsFromCSV():
        global USER_CREDENTIALS
        with open(os.path.join("test_data", "OpencartCreds.csv"), 'r') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip the headers in the OpencartCreds.csv
            USER_CREDENTIALS = dict(reader)
            return USER_CREDENTIALS
        
        
    def useEachCredPairOnlyOnce():
        for username in USER_CREDENTIALS:
            if len(USER_CREDENTIALS) > 0:
                USER_CREDENTIALS.pop(username)
                
        
    tasks = [readCredsFromCSV, useEachCredPairOnlyOnce]
    wait_time = constant(1)
        