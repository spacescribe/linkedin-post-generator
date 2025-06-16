from llm_helper import llm

def get_length_str(len):
    if(len =="Short"):
        return "1 to 5 lines"
    elif(len=="Medium"):
        return "6 to 10 lines"
    return "11 to 15 lines"

def generate_post(len, lang, topic):
    len_str=get_length_str(len)

    prompt = f'''
        Generate a LinkedIn post using the below information. No preamble.
        1. Topic: {topic}
        2. Language: {lang}
        3. Length: {len_str}

        If Language is Hinglish, it means it is a mix of Hindi and English.
        The script for the generated post should always be in English.
    '''
    response = llm.invoke(prompt)
    return response.content

if __name__=="__main__":
    post=generate_post("Short", "English", "Mental Health")
    print(post)