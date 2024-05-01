import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

class Lecturer:
    def __init__(self):
        self.name = None
        self.room = None
        self.email = None
        self.contact = None
        self.specilization_area = None


def add_data(person,soup):

    # Extracting the name
    h3_tags = soup('h3')
    for h3_tag in h3_tags:
        person.name=h3_tag.text

    # Extracting the email
    ancher_tags = soup('a')
    for ancher_tag in ancher_tags:
        if re.search(r'@', ancher_tag.text):
            person.email=ancher_tag.text

    #Extract contact number
    span_tags = soup('span')
    for span_tag in span_tags:
        if re.search(r'Phone',span_tag.text):
            person.contact=re.search(r"\+.+ext[0-9]{3}\)",span_tag.text).group()

    #Extract room number
    for span_tag in span_tags:
        if re.search(r'Room', span_tag.text) and re.search(r"[A-Z][0-9].[0-9]{3}", span_tag.text):
        # person.room=span_tag.text[8:14]
            person.room = re.search(r"[A-Z][0-9].[0-9]{3}",span_tag.text).group()

    # Extracting the specilization
    all_specilizations = ""
    parent_divs = soup('div', class_="sppb-panel sppb-panel-modern")
    for parent_div in parent_divs:
        span_tags = parent_div.find_all('span')
        for span_tag in span_tags:
            if "Specialization" in span_tag.text:
                li_tags = parent_div.find_all('li')
                for li_tag in li_tags:
                    all_specilizations += li_tag.text + ", "
                person.specilization_area = all_specilizations

data =[]




#Browsing to each profiles
url = 'https://science.kln.ac.lk/depts/im/index.php/staff/academic-staff'
main_page_html = requests.get(url).content
soup = BeautifulSoup(main_page_html,'html.parser')
tags = soup('a')
for tag in tags:
    if(tag.text=="View Full Profile"):
        view_profile_url = tag.get('href')
        response = requests.get(view_profile_url)
        view_profile_html = response.content
        view_profile_soup = BeautifulSoup(view_profile_html, 'html.parser')

        lecturer = Lecturer()
        add_data(lecturer,view_profile_soup)
        data.append([lecturer.name,lecturer.room,lecturer.email,lecturer.contact,lecturer.specilization_area])


df = pd.DataFrame(data,columns=['Name','Room No.','Email','Contact No.','Specilization Area'])
print(data)
df.to_csv('data_set.csv')