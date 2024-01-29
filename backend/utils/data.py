from os import getenv
import json

from dotenv import load_dotenv
from pymilvus import connections, Collection

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

def insert_courses_from_json(json_file_path):
    collection_dict = collection.query(expr='', limit=16383)
    keys = [list(el.values())[0] for el in collection_dict]

    with open(json_file_path, 'r') as file:
        data = json.load(file)
        for course_code in data:
            course_num = course_code.split(' ')[1][:3]
            if (course_code in keys or 'Project' in course_code or 'Thesis' in course_code or 'Special' in course_code or
                (course_num[0] == "2" and len(course_num) == 3 and course_num[-1].isnumeric())):
                print(f'{course_code} already exists')
                continue
            course_info = f'{course_code}: {data[course_code]}'
            course_info = course_info[course_info.index('- ')+2:]
            embedding = generate_desc_embedding(course_info)
            insert_into_db(course_code, embedding)
            print(f'{course_code} inserted.')

def find_related_courses(query,limit):
    embedding = generate_desc_embedding(query)
    return semantic_search(embedding, limit)

def add_descriptions(json_file_path, course_list):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    output = []

    for course in course_list:
        output.append(
            {
                "course_code": course,
                "course_description": data[course]
            }
        )

    return output
