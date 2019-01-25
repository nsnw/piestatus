#!/usr/bin/env python

import requests
import logging
import sys
import os
from bs4 import BeautifulSoup

def get_pies(event, context):
    # Chime webhook
    if 'webhook_url' not in os.environ:
        print("Missing webhook_url")
        return {'message': "Missing pie webhook :("}

    webhook_url = os.environ['webhook_url']
    saltchuck_url = "https://saltchuckpies.com"

    # Get page
    try:
        r = requests.get(saltchuck_url)
        print("Pies retrieved...")
    except:
        logger.critical("Could not retrieve pies! Oh no!")
        return {'message': "Pie retrieval failure!"}

    # Parse
    s = BeautifulSoup(r.text, 'html.parser')
    menu = s.find_all('div')[19]
    date = menu.p.text

    # Grab menus
    daily_menu, feature_menu, soup_menu, dessert_menu = menu.find_all('ul')

    # Parse menus
    dailies = [li.text for li in daily_menu.find_all('li')]
    features = [li.text for li in feature_menu.find_all('li')]
    soups = [li.text for li in soup_menu.find_all('li')]
    desserts = [li.text for li in dessert_menu.find_all('li')]
    print("Menus parsed...")

    # Build webhook content
    webhook_content = "--- Saltchuck feature pies for {} ---\n{}\n\nFor more information see {}".format(
        date,
        '\n'.join(["* {}".format(feature) for feature in features]),
        saltchuck_url
    )

    print(webhook_content)

    # Post to Chime webhook
    try:
        requests.post(webhook_url, json={'Content': webhook_content})
        return {'message': "Pie success!"}
    except:
        logger.critical("Could not post to Chime webhook! Nobody will ever know what pies are available!")
        return {'message': "Pie posting failure!"}
