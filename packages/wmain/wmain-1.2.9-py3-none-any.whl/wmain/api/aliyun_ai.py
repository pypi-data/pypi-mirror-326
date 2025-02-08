api_key = "sk-d6fde88bb1ab4a429e3b746aed3372f6"
from openai import OpenAI


class WAliyunAI:
    
    def __init__(self, qwen_model, ):
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key=api_key,  # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        ) 
completion = client.chat.completions.create(
    model=QWEN_MODEL,  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=self.msg_list,
    extra_body={"enable_search": True},
    max_tokens=MAX_TOKENS,
)
print(completion.choices[0].message.content)
