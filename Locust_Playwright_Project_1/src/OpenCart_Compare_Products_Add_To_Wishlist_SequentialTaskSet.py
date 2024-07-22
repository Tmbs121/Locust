import random, Parse_User_Credentials_From_CSV
from locust import HttpUser, task, events, SequentialTaskSet, between
from Parse_HTML_Response_Extract_Product_ids import ParseHTMLResponseExtractProductIDs

# In case we need to do debugging, we'll need to import the run_single_user function from locust module:
# from locust import run_single_user

import logging
from http.client import HTTPConnection

HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


# Retrieve from the 'Parse_User_Credentials_From_CSV' module the list USER_CREDENTIALS that contains all credentials parsed from csv file
USER_CREDENTIALS = Parse_User_Credentials_From_CSV.LoginWithCredsFromCSV.readCredsFromCSV()

@events.test_start.add_listener
def test_start(environment, **kwargs):
    print("Start of a new test")
    Parse_User_Credentials_From_CSV.LoginWithCredsFromCSV.useEachCredPairOnlyOnce


class CompareProductsAddToWishListScenario(HttpUser):
    host = "http://172.23.176.159/opencart"
    
    @task
    class SequenceOfTasks(SequentialTaskSet):
        wait_time = between(1,3)
        global host
    
        @task
        def land_to_oc_home_page(self):
            with self.client.get("/upload", catch_response=True) as resp1:
                if("Featured") in resp1.text:
                    resp1.success()
                else:
                    resp1.failure("Validation based on a string from response failed")
    
        @task
        def navigate_to_login_form(self):
            with self.client.get("/upload/index.php?route=account/login", catch_response=True) as resp2:
                if ("Returning Customer") in resp2.text:
                    resp2.success()
                else:
                    resp2.failure("Validation based on a string from response failed")      
    
        @task
        def login_to_user_profile(self):
            credentials_pair = random.choice(USER_CREDENTIALS)
            username = credentials_pair[0]
            password = credentials_pair[1]
            with self.client.post("/upload/index.php?route=account/account", {"username":username, "password":password}, catch_response=True) as resp3:
                if ("My Account") in resp3.text:
                    resp3.success()
                else:
                    resp3.failure("Validation based on a string from response failed")
                    
            logging.info('Login with %s username and %s password', username, password)
           
                      
        @task
        def choose_product_1_add_it_to_compare_list(self):
            self.product_id_1 = ParseHTMLResponseExtractProductIDs.extract_random_product_ids(self)[0]
            
            # to design a request with dynamic elements (e.g. random product_ids in the URL), Python makes use
            # of formatted string literals, aka f-strings. Put f in front of the double quotes before URL
            # and this will allow for substitution of the dynamic part of the URL with a variable name
            # whose value will be passed in the runtime:
            
            with self.client.get(f"/upload/index.php?route=product/product&path=18&product_id={self.product_id_1}", catch_response=True) as resp5:
                if ("Description") in resp5.text:
                    resp5.success()
                else:
                    resp5.failure("Validation based on a string from response failed")
                               
            with self.client.post(f"/upload/index.php?route=product/compare/add", {"product_id":{self.product_id_1}}, catch_response=True) as resp6:
                if (" Success: You have added " and "product comparison") in resp6.text:
                    resp6.success()
                else:
                    resp6.failure("Validation based on a string from response failed")
                    
            logging.info('Product %s has been added to compare list', self.product_id_1)
            
            
        @task   
        def choose_product_2_add_it_to_compare_list(self):
            # global product_id_2
            # Note on global variables:
            # Using global variables may be thread-unsafe and is generally considered risky and not the best practice.
            # So whenever we need a variable that could be visible across all the tasks in the 
            # SequentialTaskSet, using self.<variable name> (e.g. self.product_id_1 and self.product_id_2)
            # seems a much better option that dealing with global variables.
            self.product_id_2 = ParseHTMLResponseExtractProductIDs.extract_random_product_ids(self)[1]
            
            with self.client.get(f"/upload/index.php?route=product/product&path=18&product_id={self.product_id_2}", catch_response=True) as resp7:
                if ("Description") in resp7.text:
                    resp7.success()
                else:
                    resp7.failure("Validation based on a string from response failed")
                               
            with self.client.post(f"/upload/index.php?route=product/compare/add", {"product_id":{self.product_id_2}}, catch_response=True) as resp8:
                if (" Success: You have added " and "product comparison") in resp8.text:
                    resp8.success()
                else:
                    resp8.failure("Validation based on a string from response failed")
                    
            logging.info('Product %s has been added to compare list ', self.product_id_2)
           
            
        @task   
        def open_compare_list(self):
            with self.client.get("/upload/index.php?route=product/compare", catch_response=True) as resp9:
                if ("Product Comparison") in resp9.text:
                    resp9.success()
                else:
                    resp9.failure("Validation based on a string from response failed")
                    
        @task
        def remove_one_product_from_compare_list(self):
            with self.client.get(f"/upload/index.php?route=product/compare&remove={self.product_id_2}", catch_response=True) as resp10:
                if (" Success: You have modified") in resp10.text:
                    resp10.success()
                else:
                    resp10.failure("Validation based on a string from response failed")
            logging.info('Product %s has been removed from compare list ', self.product_id_2)
            
            
        @task
        def back_to_product_1_description_page(self):
            with self.client.get(f"/upload/index.php?route=product/product&product_id={self.product_id_1}", catch_response=True) as resp11:
                if ("Description") in resp11.text:
                    resp11.success()
                else:
                    resp11.failure("Validation based on a string from response failed")
            
        @task
        def add_product_1_to_wishlist(self):
            with self.client.post(f"/upload/index.php?route=account/wishlist/add", {"product_id":{self.product_id_1}}, catch_response=True) as resp12:
                if (" Success: You have added " and "wish list") in resp12.text:
                    resp12.success()
                else:
                    resp12.failure("Validation based on a string from response failed")
                    
            logging.info('Product %s has been added to wishlist', self.product_id_1)  
                  
                      
        @task
        def logout_from_user_profile(self):
            credentials_pair = random.choice(USER_CREDENTIALS)
            username = credentials_pair[0]
            with self.client.get("/upload/index.php?route=account/logout", catch_response=True) as resp13:
                if ("You have been logged off your account. It is now safe to leave the computer.") in resp13.text:
                    resp13.success()
                else:
                    resp13.failure("Validation based on a string from response failed")
                    
            logging.info('User with %s username logged out of their OpenCart profile', username)
            
            
        # Since we are inside the SequentialTaskSet, the last @task in the TaskSet
        # should be the one that calls a self interrupt:  
        @task
        def stop(self):
            self.interrupt()
     
        
@events.test_stop.add_listener  
def test_stop(environment, **kwargs):
    environment.runner.quit()
    print("End of test")         
        
        