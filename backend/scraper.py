import json
from time import sleep

from bs4 import BeautifulSoup
import requests

def scrape_sjsu_catalog():
    for i in range(1, 57):
        url = f"https://catalog.sjsu.edu/content.php?catoid=13&catoid=13&navoid=4972&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D={i}#acalog_template_course_filter"
        scrape_courses_from_page(url)
        print(f"Page {i} done")


def scrape_courses_from_page(page_url):
    page = requests.get(page_url)

    soup = BeautifulSoup(page.content, "html.parser")
    rows = soup.find_all("table", class_="table_default")[6].find_all("tr")

    course_description_map = []

    possible_desc_ends = ['  ', 'Prerequisite', 'Grading']

    for row in rows:
        sleep(1)
        if row.find('td', {'colspan': "2"}) == None: # if the first row is not a header
            course_name = row.find('a').text[:-1]
            onclick_attr = row.find('a').get('onclick').split("'")
            catoid = onclick_attr[1]
            coid = onclick_attr[3]

            url = f"https://catalog.sjsu.edu/ajax/preview_course.php?catoid={catoid}&show&coid={coid}"

            response = requests.get(url).content

            soup = BeautifulSoup(response, "html.parser")

            course_info = soup.find_all('div')[4].text
            if 'unit(s)' in course_info:
                desc_start_idx = course_info.index('unit(s)') + 8
            else:
                desc_start_idx = course_info.index('  ') + 3
            desc_end_idx = 10000
            for possible_desc_end in possible_desc_ends:
                if possible_desc_end in course_info[desc_start_idx:]:
                    desc_end_idx = min(desc_end_idx, course_info.index(possible_desc_end, desc_start_idx))
            if 'Prerequisite' in course_info:
                desc_end_idx = min(desc_end_idx, course_info.index('Prerequisite'))
            course_desc = course_info[desc_start_idx:desc_end_idx]
            course_description_map.append({
                course_name: course_desc
            })
            print(course_name)

    append_to_json('descriptions.json', course_description_map)
            
def append_to_json(json_file_path, new_data):
    with open(json_file_path, 'r+') as file:
        data = json.load(file)
        data.extend(new_data)
        file.seek(0)
        json.dump(data, file, indent=4)
