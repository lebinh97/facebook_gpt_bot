import json
from openai import OpenAI


def read_api_key(file_path = 'C:/Users/admin/Facebook bot/gpt_api_key.json'):
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        api_key_json = json.load(file)
    
    # Extract and return the API key
    return api_key_json['api_key']

def chat_gpt(prompt, extra_prompt, history_text):

    api_key = read_api_key()

    client = OpenAI(
    api_key=api_key,
    )

    # Set the context for the conversation
    full_prompt = (
        """1. Lịch sử trò chuyện của bạn và người đối thoại, vui lòng nhớ những thông tin này khi đưa ra câu trả lời:
        {}
        2. Bối cảnh giữa bạn và người đối thoại:
        {}
        Bạn là người Việt Nam, trả lời câu hỏi bằng tiếng Việt. 
        Bạn trả lời câu hỏi trong vòng 50 token.
        3. Câu hỏi như sau:
        {}""".format(history_text, extra_prompt, prompt)
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": full_prompt}],
        max_tokens=220  # Approximate limit for 400 words
    )
    
    return response.choices[0].message.content.strip()





