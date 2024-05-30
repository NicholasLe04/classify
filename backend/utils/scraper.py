from time import sleep

from bs4 import BeautifulSoup
import requests

# from utils.db import insert_into_db

def scrape_sjsu_catalog():
    for i in range(1, 57):
        page_url = f"https://catalog.sjsu.edu/content.php?catoid=13&catoid=13&navoid=4972&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D={i}#acalog_template_course_filter"
        page = requests.get(page_url)

        soup = BeautifulSoup(page.content, "html.parser")
        rows = soup.find_all("table", class_="table_default")[6].find_all("tr")

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
                
                # insert_into_db(school_name, course_name, course_desc, catoid, coid)
                print(course_name)
        print(f"Page {i} done")

            
if __name__ == "__main__":
    print("Done scraping.")