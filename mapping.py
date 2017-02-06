import requests
import json
import re
from bs4 import BeautifulSoup

def linkmap(num):
    list = [];
    r = requests.get("http://www.politifact.com/api/v/2/statement/?order_by=-ruling_date&edition__edition_slug=truth-o-meter&ruling__ruling=Pants%20on%20Fire!&limit={}&format=json&speaker__name_slug=donald-trump".format(num))
    
    key="AIzaSyA78nJZ-lOPY3p-kMhxeo7deBkE0iwOYG0"
    engine="003871306512245964513:-hacsnzdqlk"
    google="https://www.googleapis.com/customsearch/v1"
    data = json.loads(r.text)
    for obj in data["objects"]:
        politifact_url = obj["canonical_url"]
        statement = obj["statement"]
        soup = BeautifulSoup(statement, 'html.parser')
        text = ''.join(c for c in soup.text.strip() if c.isalnum() or c == ' ')
        r = requests.get(google, params={
        'key': key, 'cx': engine, 'q': text })
        gdata = json.loads(r.text)
        try:
            breitbart_url = gdata["items"][0]["link"]
            list.append((text,  "http://www.politifact.com"+politifact_url, breitbart_url));
        except KeyError:
            print(' no match for {}\n'.format(statement))
    return list    
