# -*- coding: UTF-8 -*-
import openai
import time
# from lib.ss import AlienHelper

if __name__ == '__main__':

    openai.api_key = "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"


    question_list = ["“ChatGPT仍然是“分而治之”方法的产物，所以难以成为通用的人工智能系统。”假设你是一名科普作家，请对这一判断展开论述，要求层次清晰、逻辑严谨，字数不少于1000字。", ]


    # question = "请详细介绍一下谷歌DeepMind是怎样对人工智能系统进行测试、鉴定的。"

    # n参数确定要生成的响应数量。
    # max_tokens 参数确定生成的响应中标记（即单词或标点符号）的最大数量
    for question in question_list:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            temperature=0.5,
            max_tokens=1024,
            n=1,
            stop=None
        )

        # Print the response
        text = response["choices"][0]["text"]
        # AlienHelper.writeStringToFile(text.encode("utf-8"), "chat.md")
        print(question)
        print(text)
        print("\n====================")
        time.sleep(5)

    print("\n==========回答结束==========")


