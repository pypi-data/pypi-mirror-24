from urllib.request import (urlopen, Request)
from urllib.parse import (quote, urlunparse, urlencode)
from urllib.error import HTTPError
from urllib.error import URLError

import json

def correct(msg):
    
    FINALMSG = ""
    original_text = msg
    fixed_text = original_text
    # public api
    API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"
    scheme = "http"
    netloc = "services.gingersoftware.com"
    path = "/Ginger/correct/json/GingerTheText"
    params = ""
    query = urlencode([
        ("lang", "US"),
        ("clientVersion", "2.0"),
        ("apiKey", API_KEY),
        ("text", msg)])
    fragment = ""

    results = urlunparse((scheme, netloc, path, params, query, fragment))
    try:
        response = urlopen(results)
    except HTTPError as e:
            print("HTTP Error:", e.code)
    except URLError as e:
            print("URL Error:", e.reason)

    try:
        results = json.loads(response.read().decode('utf-8'))
    except ValueError:
        print("Value Error: Invalid server response.")

    if results["LightGingerTheTextResult"] == []:
        pass

    elif(results["LightGingerTheTextResult"]):
        # I modified this piece of code from somewhere just cause I wanted to make this wrapper very quickly.

        color_gap, fixed_gap = 0, 0
        for result in results["LightGingerTheTextResult"]:
            if(result["Suggestions"]):
                from_index = result["From"] + color_gap
                to_index = result["To"] + 1 + color_gap
                suggest = result["Suggestions"][0]["Text"]

                colored_suggest, gap = suggest, 0

                fixed_text = fixed_text[:from_index-fixed_gap] + colored_suggest + fixed_text[to_index-fixed_gap:]

                color_gap += gap
                fixed_gap += to_index-from_index-len(suggest)

                FINALMSG = fixed_text

    return(str(FINALMSG))