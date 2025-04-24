from locust import User, constant, os
import csv

USER_CREDENTIALS = []

class LoginWithCredsFromCSV(User):
    username = "NOT_FOUND"
    password = "NOT_FOUND"
    
    def readCredsFromCSV():
        global USER_CREDENTIALS
        with open(os.path.join("test_data", "OpencartCreds.csv"), 'r') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip the headers in the OpencartCreds.csv
            USER_CREDENTIALS = list(reader)
            return USER_CREDENTIALS
        
        
    def useEachCredPairOnlyOnce(self):
        if len(USER_CREDENTIALS) > 0:
            self.username, self.password = USER_CREDENTIALS.pop()
            
        
    tasks = [readCredsFromCSV, useEachCredPairOnlyOnce]
    wait_time = constant(1)
        