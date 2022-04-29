import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if "apikey" in kwargs:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(url)
    print(payload)
    print(kwargs)
    try:
        response = requests.post(url, params=kwargs, json=payload)
    except Exception as e:
        print("Error" ,e)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_state_from_cf(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,state=state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
            
    return results

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    
    if json_result:
        reviews = json_result["entries"]
        # For each review object
        for review in reviews:
            try:
                review_obj = DealerReview(
                    dealership=review["dealership"],
                    name=review["name"],
                    purchase=review["purchase"],
                    review=review["review"],
                    purchase_date=review["purchase_date"],
                    car_make=review["car_make"],
                    car_model=review["car_model"],
                    car_year=review["car_year"],
                    sentiment=analyze_review_sentiments(review)
                    )
            except:
                review_obj = DealerReview(
                    dealership=review["dealership"],
                    name=review["name"],
                    purchase=review["purchase"],
                    review=review["review"],
                    purchase_date='none',
                    car_make='none',
                    car_model='none',
                    car_year='none',
                    sentiment=analyze_review_sentiments(review)
                    )
            results.append(review_obj)
    #print(results[0])
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    API_KEY="W1clNL0mYew8F8eKtmDOxrRiYmf2f-FntOJ74rhfQUs-"
    URL='https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/767a163f-e5a9-49c5-86b1-464a92f1e2d2'
    params = json.dumps({"text": dealerreview, "features": {"sentiment": {}}})
    response = requests.post(
        URL, data=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', API_KEY)
    )
    try:
        return response.json()['sentiment']['document']['label']
    except KeyError:
        return 'neutral'
    

