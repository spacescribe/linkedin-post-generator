import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm


def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path, 'r', encoding='utf-8') as file:
        posts=json.load(file)
        for post in posts:
            metadata = extract_metadata(post)
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)
        
        for epost in enriched_posts:
            print(epost)

def extract_metadata(post):
    template = '''
        You are given a LinkedIn post. Extract the the number of lines, language and the tags in this **exact** format and return **only a valid JSON**. No explanation, no code block.

        Requirements:
        1. Return a valid JSON with **no preamble**, **no explanation**, **no markdown**.
        2. JSON object should have exactly three keys: line_count, language and tags. 
        3. tags is an array of text tags. Extract maximum two tags.
        4. Language should be English or Hinglish (Hinglish means hindi + english)

        Here is the actual post:
        {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException as e:
        raise OutputParserException("Failed to parse the Json output: " + str(e))
    return res

if __name__== "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")