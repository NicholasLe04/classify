from os import getenv
import json

from dotenv import load_dotenv
from pymilvus import connections, Collection

from embedding import generate_desc_embedding

load_dotenv()

connections.connect(
  alias='default', 
  uri=getenv('CLUSTER_ENDPOINT'),
  token=getenv('CLUSTER_API_KEY'), 
)

collection = Collection("Courses")

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

def semantic_search(input_embedding):
    search_param = {
        "data": [input_embedding],
        "anns_field": "course_desc_embedding",
        "param": {"metric_type": "L2"},
        "limit": 5
    }
    res = collection.search(**search_param)
    hits = res[0]
    print(f"- Total hits: {len(hits)}, hits ids: {hits.ids} ")
    for hit in hits:
        print(f"- Top1 hit id: {hit.id}, distance: {hit.distance}, score: {hit.score} ")

def insert_all_courses(json_file_path):
    courses = collection.query(expr='', limit=16383)
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        for course in data:
            course_code = list(course.keys())[0]
            if ({ 'course_code':course_code } in courses):
                print(f'{course_code} already exists')
                continue
            course_desc = list(course.values())[0]
            embedding = generate_desc_embedding(course_desc)
            insert_into_db(course_code, embedding)

def find_related_courses(query):
    embedding = generate_desc_embedding(query)
    semantic_search(embedding)

if __name__ == '__main__':
    insert_all_courses('descriptions.json')
    # find_related_courses('I am really interested in space!')
    # delete_course("AE 180 - Individual Studies")