from openai import OpenAI
from local import config

api_key = config.DevelopmentConfig.OPENAI_KEY
client = OpenAI(api_key=api_key)


def generate_response(prompt):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    """"
    different roles we can assign example :
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  
    """
    question = {"role": "user", "content": prompt}
    messages.append(question)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    try:
        answer = response["choices"][0]["message"]["content"]
    except:
        answer = "Try again later"
    return answer
