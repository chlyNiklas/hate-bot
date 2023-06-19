from gpt4all import GPT4All
from mastodon import Mastodon



def create_rant_about(topic: str):
    rant = {
        "headline": "",
        "text": "",
        "hashtags": ""
    }
    gptj = GPT4All("ggml-gpt4all-j-v1.3-groovy.bin")

    messages = [{"role": "user", "content": "Write a little rant about " + topic + "!"}]
    rant["text"] = gptj.chat_completion(messages)["choices"][0]["message"]["content"]

    messages = [
        {"role": "assistant", "content": rant["text"]},
        {"role": "user", "content": "Write 5 hashtags fitting for your text. Just write the hashtags and separate them "
                                    "ONLY with a space."}
    ]
    rant["hashtags"] = gptj.chat_completion(messages)["choices"][0]["message"]["content"]

    messages = [
        {"role": "assistant", "content": rant["text"]},
        {"role": "user", "content": "Write a headline for your rant!"}
    ]
    rant["headline"] = gptj.chat_completion(messages)["choices"][0]["message"]["content"]

    return rant


print(create_rant_about("peoples"))
