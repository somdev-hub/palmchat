import google.generativeai as palm
from dotenv import load_dotenv
import os

load_dotenv()


palm.configure(api_key=os.getenv("GOOGLE_PALM_API_KEY"))


def chat(messages):
    response = palm.chat(messages=messages)
    return response.last


if __name__ == '__main__':
    response = palm.chat(messages="hello")
    print(response.last)
