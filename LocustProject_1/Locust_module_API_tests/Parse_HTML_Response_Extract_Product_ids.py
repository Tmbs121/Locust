from locust import HttpUser, task
import re, random, lxml
from bs4 import BeautifulSoup


class ParseHTMLResponseExtractProductIDs(HttpUser):
    host = "http://172.23.176.159/opencart"
    
    @task  
    def extract_random_product_ids(self):
        response = self.client.get("/upload/index.php?route=product/category&path=18",
                                       name="/choosing_notebooks_and_laptops_product_category")
        soup = BeautifulSoup(response.text, lxml)
        h4_tags_list = soup.find_all('h4')           
        h4_tags_list_2_random_tags = random.sample(h4_tags_list, 2)
        random_h4_tag_1 = h4_tags_list_2_random_tags[0]
        random_h4_tag_2 = h4_tags_list_2_random_tags[1]
        pattern = "product_id=(\d*)"           
        random_product_id_1 = re.findall(pattern, str(random_h4_tag_1))[0]
        random_product_id_2 = re.findall(pattern, str(random_h4_tag_2))[0]
        return [random_product_id_1, random_product_id_2]
     
        
        # For debugging:
        # print("h4_tags_list_2_random_tags including 2 randomly chosen tags: ", h4_tags_list_2_random_tags)
        # print("random_h4_tag_1 is: ", random_h4_tag_1)
        # print("random_h4_tag_2 is: ", random_h4_tag_2)
        # print("random_product_id_1 is: ", random_product_id_1)
        # print("random_product_id_2 is: ", random_product_id_2)
    
        