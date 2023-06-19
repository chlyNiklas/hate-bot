import random
from gpt4all import GPT4All
from dotenv import load_dotenv
from mastodon import Mastodon
import os


def create_rant_about(topic: str):
    rant = {
        "prompt": "Write a little and aggressive rant about " + topic + "! Respond very SHORT, maximum 3 sentences. " +
                  "If you can't add any thing from importance to this Topic, write a rant anyway.",
        "text": "",
        "hashtags": ""
    }
    gptj = GPT4All("ggml-gpt4all-j-v1.3-groovy.bin", )

    messages = [{"role": "user", "content": rant["prompt"]}]
    rant["text"] = gptj.chat_completion(messages, verbose=False)["choices"][0]["message"]["content"]

    #Shorten if neccecary
    split_up_text = rant["text"].split(".")
    rant["text"] = ""
    for i in range(0, len(split_up_text)):
        if i > 2:
            break

        rant["text"] += split_up_text[i] + "."

    print(rant["text"])


    messages = [
        {"role": "assistant", "content": rant["text"]},
        {"role": "user", "content": "Write exactly 5 hashtags fitting for your text. Just write the hashtags and separate them "
                                    "ONLY with a space."}
    ]
    rant["hashtags"] = gptj.chat_completion(messages, verbose=False)["choices"][0]["message"]["content"]

    return rant


def get_topic():
    with open('topics.txt') as f:
        lines = f.readlines()
        return random.choice(lines).split("\n")[0]


load_dotenv()

mastodon = Mastodon(
    client_id=os.getenv("client_key"),
    client_secret=os.getenv("client_secret"),
    access_token=os.getenv("access_token"),
    api_base_url="https://mastodon.social"
)
rant = create_rant_about(get_topic())
print(rant)
mastodon.status_post(rant["text"] + "\n" + rant["hashtags"],
                     spoiler_text="This is an AI generated post. More in Bio")
