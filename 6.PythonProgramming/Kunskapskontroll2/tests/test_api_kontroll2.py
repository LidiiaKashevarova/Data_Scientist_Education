#Testet är utformat för kontroll2.py  att verifiera att API-svaret tas emot korrekt och att fel hanteras korrekt.

import unittest
from unittest.mock import patch #to replace parts of code with mock objects during testing
import requests

# Defines a new test case class which contain the test methods 
class TestAPIRequest(unittest.TestCase):
    
    def setUp(self):
        # Define the URL and query at the class level, so they can be reused in both tests
        self.url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/UF/UF0550/UF0550C/Historisk11b"
        self.query = {
            "query": [
                {
                    "code": "Yrkesexamen",
                    "selection": {
                        "filter": "item",
                        "values": [
                            "YLÄKA"  # Code for medical exam
                        ]
                    }
                },
                {
                    "code": "Kon",  # Gender
                    "selection": {
                        "filter": "item",
                        "values": [
                            "1.2",  # All genders
                            "1",    # Men
                            "2"     # Women
                        ]
                    }
                }
            ],
            "response": {
                "format": "json"  # Expecting the response in JSON format
            }
        }
    
    #To replace the requests.post method with a mock object
    @patch('requests.post')
    def test_api_request_success(self, mock_post):  #the mock object replacing requests.post 
        mock_response = mock_post.return_value
        mock_response.status_code = 200 #success response code
        mock_response.json.return_value = {
            "data": [
                {"key": "value1"},
                {"key": "value2"}
            ]
        }
        
        response = requests.post(self.url, json=self.query)
        self.assertEqual(response.status_code, 200) #verifying that the response is success
        self.assertIsInstance(response.json(), dict) #verifying that the response is s of type dict
        
    

    @patch('requests.post') 
    def test_api_request_failure(self, mock_post):
        mock_post.return_value.status_code = 404 #response code for error
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.RequestException("Not Found")

        with self.assertRaises(requests.exceptions.RequestException):
            response = requests.post(self.url, json=self.query)
            response.raise_for_status()
            
if __name__ == '__main__':  #to prevent unintended execution of code when the module is imported
    unittest.main() #Runs all test methods in the script