import google.generativeai as palm

palm.configure(api_key='AIzaSyDVayFnx5Gu39VSMQCcwXWmNNSBoopaFSY')


def chat(messages):
    response = palm.chat(messages=messages)
    return response.last


if __name__ == '__main__':
    response = palm.chat(messages="hello")
    print(response.last)
