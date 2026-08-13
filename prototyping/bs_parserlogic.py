import re

from bs4 import BeautifulSoup

with open("dumps.html") as file:
    soup = BeautifulSoup(file, "lxml")
    for item in soup.find_all("li"):
        tag = item.a.text.strip()
        pset = re.sub(r".*/", "", tag)
        print(pset)
        pset_date = item.find(attrs={"data-moment": "LLLL"}).text.strip()
        print(pset_date)
