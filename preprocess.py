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
        
    unified_tags=get_unified_tags(enriched_posts)

    for post in enriched_posts:
        curr_tags=post['tags']
        new_tags={unified_tags[tag] for tag in curr_tags}
        post['tags']=list(new_tags)
    
    with open(processed_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(enriched_posts, outfile, indent=4)

def get_unified_tags(posts_with_metadata):
    unique_tags=set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])
    
    unique_tags_list = ', '.join(unique_tags)

    template=''' I will give you a list of tags. You need to unify those tags with the below requirements with no explanation and no code block.
        1. Tags are unified and merged to create a shorter list. 
            Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
            Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
            Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
            Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
        2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
        3. Output should be a JSON object, No preamble
        3. Output should have mapping of original tag and the unified tag. 
        For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}
            
    Here is the list of tags: 
    {tags}
    '''
    pt=PromptTemplate.from_template(template)
    chain = pt| llm
    response=chain.invoke(input={"tags": str(unique_tags_list)})

    try:
        json_parser=JsonOutputParser()
        res=json_parser.parse(response.content)
    except OutputParserException as e:
        raise OutputParserException("Failed to parse the Json output: " + str(e))
    return res

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