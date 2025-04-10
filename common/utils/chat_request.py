import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("ALI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def chat(q="", stream=True, usage=False, prompt=None, model="qwen-math-plus-latest"):
    reasoning_content = ""
    answer_content = ""
    is_answering = False
    if q == "":
        q = r""

    # 动态构建请求参数
    completion_params = {
        "model": model,
        "messages": [],
        "stream": stream,
    }
    # completion_params["messages"].append(
    #     {"role": "system", "content": "不要思考！不要思考！不要思考！直接按照我要求的格式返回！"}
    # )
    if prompt is not None:
        for p in prompt:
            completion_params["messages"].append(p)

    completion_params["messages"].append({"role": "user", "content": q})
    # 仅当 stream=True 时添加 stream_options
    if stream:
        completion_params["stream_options"] = {"include_usage": usage}

    # 创建聊天完成请求
    completion = client.chat.completions.create(**completion_params)
    if stream is False:
        yield completion.choices[0].message.content
    else:
        for chunk in completion:
            # 如果chunk.choices为空，则打印usage
            if not chunk.choices:
                yield "\nUsage:\n"
                yield str(chunk.usage) + "\n"
            else:
                delta = chunk.choices[0].delta
                # 打印思考过程
                if hasattr(delta, "reasoning_content") and delta.reasoning_content != None:
                    yield delta.reasoning_content
                    reasoning_content += delta.reasoning_content
                else:
                    # 开始回复
                    if delta.content != "" and is_answering == False:
                        is_answering = True
                    # 打印回复过程
                    yield delta.content
                    answer_content += delta.content
