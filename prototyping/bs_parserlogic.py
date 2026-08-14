import json
import re

from bs4 import BeautifulSoup

pset_list = []

with open("dumps.html") as file:
    soup = BeautifulSoup(file, "lxml")
    for item in soup.find_all("li"):
        tag = item.a.text.strip()
        pset_name = re.sub(r".*/", "", tag)
        # print(pset_name)
        pset_date = item.find(attrs={"data-moment": "LLLL"}).text.strip()
        # print(pset_date)
        pset_dict = {"pset_name": pset_name, "pset_date": pset_date}
        pset_list.append(pset_dict)

print(json.dumps(pset_list, indent=2))
