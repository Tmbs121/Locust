import random
import re

from bs4 import BeautifulSoup
from locust import HttpUser, task

product_ids = []


class ParseHTMLResponseExtractProductIDs(HttpUser):
    host = "http://172.23.176.159/opencart"

    @task
    def extract_random_product_ids(self) -> list:
        response = self.client.get("/upload/index.php?route=product/category&path=18",
                                   name="/choosing_notebooks_and_laptops_product_category")
        soup = BeautifulSoup(response.text, "lxml")
        h4_tags_list = soup.find_all('h4')
        h4_tags_list_2_random_tags = random.sample(h4_tags_list, 2)
        random_h4_tag_1 = h4_tags_list_2_random_tags[0]
        random_h4_tag_2 = h4_tags_list_2_random_tags[1]
        pattern = "product_id=(\d*)"
        random_product_id_1 = re.findall(pattern, str(random_h4_tag_1))[0]
        random_product_id_2 = re.findall(pattern, str(random_h4_tag_2))[0]
        product_ids.insert(0, random_product_id_1)
        product_ids.insert(1, random_product_id_2)
        return product_ids
