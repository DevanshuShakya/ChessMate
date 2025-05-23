from openai import OpenAI
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    YOUR_API_KEY = "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"

    # messages = [
    #     {
    #         "role": "system",
    #         "content": (
    #             "You have to collect the recent news about chess and output it into JSON format with summarized version of news in which each news contains a title and the summary"
    #         ),
    #     },
    #     {   
    #         "role": "user",
    #         "content": (
    #             "What are the recent news in the world of chess."
    #         ),
    #     },
    # ]

    messages = [
        {
            "role": "system",
            "content": (
                "You need to give me the array of ingredients of a recipe"
            ),
        },
        {   
            "role": "user",
            "content": (
                "What are the ingredients of the recipe"
            ),
        },
    ]

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    print(response)

    # # chat completion with streaming
    # response_stream = client.chat.completions.create(
    #     model="sonar-pro",
    #     messages=messages,
    #     stream=True,
    # )
    # for response in response_stream:
    #     print(response)
    


    # after receiving the response
    data = response.model_dump()   # or response.dict() in older versions
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)

