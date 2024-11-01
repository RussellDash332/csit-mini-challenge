import requests, time, re, json, os

def get_auth_token():
    r = requests.get(BASE_URL + '/register')
    auth_token = r.json()['data']['authorizationToken']
    return auth_token

def get_cleaned_dataset():
    # this should take at most a minute, which is way under the auth_token lifetime which is observed to be about an hour
    dataset = []
    payload = {'next_id': ''}
    while True:
        r = requests.post(BASE_URL + '/download-dataset', headers=HEADERS, json=payload)
        if r.status_code == 429: # rate limit
            time.sleep(5)
            continue
        resp = r.json()['data']
        url = resp['dataset_url']
        payload['next_id'] = resp['next_id']

        r = requests.get(url)
        dataset.extend(filter(is_valid, r.json()))
        if payload['next_id']:
            time.sleep(10)
        else:
            break
    return dataset

def is_valid(restaurant):
    if type(restaurant.get('id')) != int:
        return False
    if type(restaurant.get('restaurant_name')) != str:
        return False
    name = restaurant['restaurant_name']
    if not re.match(r'^[A-Za-z\s]+$', name):
        return False
    if type(restaurant.get('rating')) != float:
        return False
    rating = restaurant['rating']
    if rating < 1 or rating > 10:
        return False
    if type(restaurant.get('distance_from_me')) != float:
        return False
    dist = restaurant['distance_from_me']
    if dist < 10 or dist > 1000:
        return False
    return True

def validate_dataset(dataset):
    r = requests.post(BASE_URL + '/test/check-data-validation', json={'data': dataset})
    message = r.json().get('message')
    print('check-data-validation:', message)

if __name__ == '__main__':
    try:
        BASE_URL = os.environ['API_URL']
    except:
        BASE_URL = 'https://u8whitimu7.execute-api.ap-southeast-1.amazonaws.com/prod/'

    try:
        OUT_DIR = os.environ['OUT_DIR']
    except:
        OUT_DIR = '../part2'

    HEADERS = {'authorizationToken': get_auth_token(), 'Content-Type': 'application/json'}
    dataset = get_cleaned_dataset()

    # Part 1
    out = OUT_DIR + 'validated_dataset.json'
    if OUT_DIR: os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        json.dump(dataset, f, indent=4)
    validate_dataset(dataset)