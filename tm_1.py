ACCESS_TOKEN = ""


def get_words(url):
    import requests
    words = requests.get(url).content.decode('latin-1')
    word_list = words.split('\n')
    index = 0
    while index < len(word_list):
        word = word_list[index]
        if ';' in word or not word:
            word_list.pop(index)
        else:
            index += 1
    return word_list


def get_access_token():
    url = "https://api.yelp.com/oauth2/token"
    with open('yelp_keys.txt', 'r') as f:
        count = 0
        for line in f:
            if count == 0:
                client_id = line.strip().split('=')[1]
            if count == 1:
                client_secret = line.strip().split('=')[1]
            count += 1
    params = {"client_id": client_id, "client_secret": client_secret}
    # print(params)
    import requests
    r = requests.post(url, params)
    access_token = r.json()['access_token']
    # access_token
    return access_token


def get_nrc_data():
    nrc = "data/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
    count = 0
    emotion_dict = dict()
    with open(nrc, 'r') as f:
        all_lines = list()
        for line in f:
            if count < 46:
                count += 1
                continue
            line = line.strip().split('\t')
            if int(line[2]) == 1:
                if emotion_dict.get(line[0]):
                    emotion_dict[line[0]].append(line[1])
                else:
                    emotion_dict[line[0]] = [line[1]]
    return emotion_dict


def set_search_parameters(lat, long, radius):
    # See the Yelp API for more details
    params = {}
    params["term"] = "restaurant"
    params["latitude"] = "{}".format(str(lat))
    params["longitude"] = "{}".format(str(long))
    params["radius_filter"] = str(radius)  # The distance around our point in metres
    params["limit"] = "10"  # Limit ourselves to 10 results

    return params


def get_results(params):
    import requests
    url = "https://api.yelp.com/v3/businesses/search?limit={}&latitude={}&radius_filter={}&term={}&longitude={}"
    url = url.format(params.get('limit'), params.get('latitude'), params.get('radius_filter'), params.get('term'),
                     params.get('longitude'))
    token = ACCESS_TOKEN
    r = requests.get(url, headers={"Authorization": "Bearer " + token})
    data = r.json()
    return data


def get_lat_lng(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    url += address
    import requests
    response = requests.get(url)
    if not (response.status_code == 200):
        return None
    data = response.json()
    if not (data['status'] == 'OK'):
        return None
    main_result = data['results'][0]
    geometry = main_result['geometry']
    latitude = geometry['location']['lat']
    longitude = geometry['location']['lng']
    return latitude, longitude


def get_business_id(json_data):
    all_business_id = list()
    for business in json_data['businesses']:
        name = business['name']
        id = business['id']
        all_business_id.append((id, name))
    return all_business_id


def get_reviews(all_business_id):
    url = "https://api.yelp.com/v3/businesses/{}/reviews"
    token = ACCESS_TOKEN
    snippet = list()
    import requests
    for i in range(len(all_business_id)):
        business_id = str(all_business_id[i][0])
        business_name = str(all_business_id[i][1])
        # print(business_id + " " + business_name)
        url1 = url.format(str(all_business_id[i][0]))
        r = requests.get(url1, headers={"Authorization": "Bearer " + token})
        wjdata = r.json()
        ls = wjdata.get('reviews')
        if (ls == None):
            ls = list()
        text = ""
        for i in range(len(ls)):
            d = ls[i]
            text = text + d.get('text')
            # l.append(d.get('text'))
        snippet.append((business_id, business_name, text))
    return snippet


def emotion_analyzer(text, emotion_dict):
    # Set up the result dictionary
    emotions = {x for y in emotion_dict.values() for x in y}
    emotion_count = dict()
    for emotion in emotions:
        emotion_count[emotion] = 0

    # Analyze the text and normalize by total number of words
    total_words = len(text.split())
    for word in text.split():
        if emotion_dict.get(word):
            for emotion in emotion_dict.get(word):
                emotion_count[emotion] += 1 / len(text.split())
    return emotion_count


def comparative_emotion_analyzer(text_tuples, emotion_dict):
    print("%-20s %1s\t%1s %1s %1s %1s   %1s %1s %1s %1s" % (
        "restaurant", "fear", "trust", "negative", "positive", "joy", "disgust", "anticip",
        "sadness", "surprise"))

    for text_tuple in text_tuples:
        text = text_tuple[2]
        result = emotion_analyzer(text, emotion_dict)
        print("%-20s %1.2f\t%1.2f\t%1.2f\t%1.2f\t%1.2f\t%1.2f\t%1.2f\t%1.2f\t%1.2f" % (
            text_tuple[1][0:20], result['fear'], result['trust'],
            result['negative'], result['positive'], result['joy'], result['disgust'],
            result['anticipation'], result['sadness'], result['surprise']))
