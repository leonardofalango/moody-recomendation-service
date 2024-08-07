from concurrent.futures import ThreadPoolExecutor
import json
import random
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

places_data = {"places": []}

raw_names = json.load(open("model/data/generate/raw_places.json", encoding="utf-8"))
locations = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Brasília", "Curitiba"]
names = []
for k, v in raw_names.items():
    names.extend(v)

# print(names)


def get_image_url(place_name):
    search_url = "https://www.bing.com/images/search"
    params = {"q": place_name, "FORM": "HDRSC2"}
    response = requests.get(search_url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    img_tag = soup.find("a", class_="iusc")
    if img_tag:
        img_url = img_tag.get("m")
        img_url = img_url.split('"murl":"')[1].split('"')[0]
        return img_url
    return None


def generate(i):
    name = names[i]
    return {
        "place_id": str(i),
        "name": name,
        "location": random.choice(locations),
        "rating": round(random.uniform(3.0, 5.0), 1),
        "likes": random.randint(50, 1000),
        "image": get_image_url(name)
        or "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTw_HeSzHfBorKS4muw4IIeVvvRgnhyO8Gn8w&s",
    }


import concurrent.futures

with ThreadPoolExecutor(max_workers=16) as executor:
    f = {executor.submit(generate, i): i for i in range(len(names))}

    for future in tqdm(concurrent.futures.as_completed(f), total=len(names)):
        data = f[future]
        try:
            data = future.result()
            places_data["places"].append(data)
        except Exception as exc:
            print("%r generated an exception: %s" % (data, exc))

        with open("model/data/places.json", "w", encoding="utf-8") as file:
            json_data = json.dumps(places_data, indent=2, ensure_ascii=False)
            file.write(json_data)
