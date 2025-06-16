from llm_helper import llm
from few_shot import FewShotPosts

fs=FewShotPosts()

def get_lengthgth_str(length):
    if(length =="Short"):
        return "1 to 5 lines"
    elif(length=="Medium"):
        return "6 to 10 lines"
    return "11 to 15 lines"

def get_prompt(length, lang, topic):
    length_str=get_lengthgth_str(length)

    prompt = f'''
        Generate a LinkedIn post using the below information. No preamble.
        1. Topic: {topic}
        2. Language: {lang}
        3. lengthgth: {length_str}

        If Language is Hinglish, it means it is a mix of Hindi and English.
        The script for the generated post should always be in English.
    '''

    examples=fs.get_filtered_posts(length, lang, topic)
    if len(examples)>0:
        prompt+="4. Use the writing style as per the below examples: "
        for i, post in enumerate(examples):
            post_text=post['text']
            prompt+=f"\n Example {i+1}:\n{post_text}\n\n"
            
            if i==1:
                break
    # print(f"The example prompt is: {prompt}")
    return prompt

def generate_post(length, lang, topic):
    prompt = get_prompt(length, lang, topic)
    response = llm.invoke(prompt)
    return response.content

if __name__=="__main__":
    post=generate_post("Medium", "English", "Happiness")
    print(post)