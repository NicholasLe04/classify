from os import getenv

from dotenv import load_dotenv
from pymilvus import connections, Collection

from utils.db import get_course_info, get_courses
from utils.embedding import generate_desc_embedding

load_dotenv()

connections.connect(
  alias='default', 
  uri=getenv('CLUSTER_ENDPOINT'),
  token=getenv('CLUSTER_API_KEY'), 
)

collection = Collection(getenv('COLLECTION'))

def insert_into_db(course_code, embedding):
    data = [
        [course_code], 
        [embedding]
    ]
    collection.insert(data)
    print(f'{course_code} inserted')

def delete_course(course_code:str):
    collection.delete(f'course_code=="{course_code}"')
    print(f'{course_code} deleted')

def already_exists(course_code:str):
    return collection.query(expr=f'course_code == "{course_code}"')

def semantic_search(input_embedding, limit):
    search_param = {
        "data": [input_embedding],
        "anns_field": "course_desc_embedding",
        "param": {"metric_type": "L2"},
        "limit": limit
    }
    res = collection.search(**search_param)
    hits = res[0]
    result = []

    for hit in hits:
        result.append(hit.id)

    return result

# OBSOLETE
def insert_courses_from_sql():
    collection_dict = collection.query(expr='', limit=16383)
    keys = [list(el.values())[0] for el in collection_dict]

    for (course_code, course_desc, _, _) in get_courses():
        course_num = course_code.split(' ')[1][:3]
        if (course_code in keys or 'Project' in course_code or 'Thesis' in course_code or 'Special' in course_code or
            (course_num[0] == "2" and len(course_num) == 3 and course_num[-1].isnumeric())):
            print(f'{course_code} already exists')
            continue
        course_info = f'{course_code}: {course_desc}'
        course_info = course_info[course_info.index('- ')+2:]
        embedding = generate_desc_embedding(course_info)
        insert_into_db(course_code, embedding)
        print(f'{course_code} inserted.')

    # with open(json_file_path, 'r') as file:
    #     data = json.load(file)
    #     for course_code in data:
    #         course_num = course_code.split(' ')[1][:3]
    #         if (course_code in keys or 'Project' in course_code or 'Thesis' in course_code or 'Special' in course_code or
    #             (course_num[0] == "2" and len(course_num) == 3 and course_num[-1].isnumeric())):
    #             print(f'{course_code} already exists')
    #             continue
    #         course_info = f'{course_code}: {data[course_code]["course_description"]}'
    #         course_info = course_info[course_info.index('- ')+2:]
    #         embedding = generate_desc_embedding(course_info)
    #         insert_into_db(course_code, embedding)
    #         print(f'{course_code} inserted.')

def find_related_courses(query,limit):
    embedding = generate_desc_embedding(query)
    return semantic_search(embedding, limit)

def add_course_data(course_list):
    output = []

    for course in course_list:
        course_code, description, catoid, coid = get_course_info(course)
        output.append(
            {
                "course_code": course_code,
                "course_description": description,
                "catoid": catoid,
                "coid": coid
            }
        )

    return output
