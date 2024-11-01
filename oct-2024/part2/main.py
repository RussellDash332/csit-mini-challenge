import requests, json, heapq, math, os

# attempt to optimize: early termination for comparison
class Record:
    def __init__(self, record, idx):
        self.record = record
        self.idx = idx
    def __lt__(self, other):
        if self.record['score'] != other.record['score']:
            return self.record['score'] < other.record['score']
        if self.record['rating'] != other.record['rating']:
            return self.record['rating'] < other.record['rating']
        if self.record['distance_from_me'] != other.record['distance_from_me']:
            return self.record['distance_from_me'] < other.record['distance_from_me']
        return self.record['restaurant_name'] > other.record['restaurant_name']

def get_topk(dataset, k):
    pq = []
    for idx, restaurant in enumerate(dataset):
        score = (restaurant['rating'] * 10 - restaurant['distance_from_me'] * 0.5 + math.sin(restaurant['id']) * 2) * 100 + 0.5
        restaurant['score'] = round(score / 100, 2)
        if len(pq) < k: f = heapq.heappush
        else: f = heapq.heappushpop
        f(pq, Record(restaurant, idx))
    return list(map(lambda x: dataset[x.idx], heapq.nlargest(k, pq)))

def check_topk(topk):
    r = requests.post(BASE_URL + '/test/check-topk-sort', json={'data': topk})
    message = r.json().get('message')
    print('check-topk-sort:', message)

if __name__ == '__main__':
    try:
        BASE_URL = os.environ['API_URL']
    except:
        BASE_URL = 'https://u8whitimu7.execute-api.ap-southeast-1.amazonaws.com/prod/'

    try:
        OUT_DIR = os.environ['OUT_DIR']
    except:
        OUT_DIR = ''

    # Part 2
    K = 10
    inp = OUT_DIR + 'validated_dataset.json'
    with open(inp, 'r') as f:
        dataset = json.load(f)
    out = OUT_DIR + 'topk_results.json'
    topk = get_topk(dataset, K)
    with open(out, 'w') as f:
        json.dump(topk, f, indent=4)
    check_topk(topk)