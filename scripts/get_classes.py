import requests;
from bs4 import BeautifulSoup;
import re;

response = requests.post("https://cdcs.ur.rochester.edu/default.aspx");

soup = BeautifulSoup(response.text, features="html.parser");

deptSelecter = soup.find("select", {"id": "ddlDept"});

depts = [dept["value"] for dept in deptSelecter.find_all("option") if dept["value"] != ''];

print(depts);

