import os
from typing import List, Dict

from dotenv import load_dotenv
from openai import OpenAI

# 加载.evn中的环境变量
load_dotenv()


class HelloAgentsLLM:
    def __init__(self, model: str = None, api_key: str = None, base_url: str = None, timeout: int = None):
        """
        初始化客户端，优先使用传入的参数
        """
        self.model = model or os.getenv('LLM_MODEL_ID')
        api_key = api_key or os.getenv('LLM_API_KEY')
        base_url = base_url or os.getenv('LLM_BASE_URL')
        timeout = timeout or int(os.getenv('LLM_TIMEOUT', 60))
        if not all([self.model, api_key, base_url]):
            raise ValueError("模型ID、ApiKey或服务地址未配置")
        self.open_ai_client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)

    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        调用大模型
        """
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.open_ai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True
            )
            # 处理流式响应
            print("✅ 大语言模型响应成功:")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print("")
            return "".join(collected_content)
        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            return None


if __name__ == '__main__':
    try:
        llm = HelloAgentsLLM()
        exampleMessages = [
            {"role": "system", "content": "你是一个精通python的专家"},
            {"role": "user", "content": "写一个冒泡排序算法"}
        ]
        print("调用LLM...")
        responseText = llm.think(messages=exampleMessages, temperature=0)
        if responseText:
            print("\n\n完整响应信息")
            print(responseText)

    except Exception as e:
        print(e)
