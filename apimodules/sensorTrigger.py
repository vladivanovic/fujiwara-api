import requests
import os
import json


if __name__ == "__main__":
    ## retrieve data from database
    ## Dev note: using hardcoded json for now
    dir = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(dir, "sampleWebhook.json")) as temp:
        hook = temp.read()

    jsonHook = json.loads(hook)

    print (jsonHook)
