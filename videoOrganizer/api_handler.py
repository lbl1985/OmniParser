import os
from openai import AzureOpenAI

class APIHandler:
    def __init__(self):
        endpoint = os.getenv("ENDPOINT_URL", "https://jynllm3164666857.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview")
        deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")
        subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "")

        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=subscription_key,
            api_version="2024-05-01-preview",
        )
        self.deployment = deployment

    def call_api(self, user_input):
        constant_input = [{"type": "text", "text": "请只输出结果。不需要说明"}]
        if not isinstance(user_input, list):
            content_input = [{"type": "text", "text": user_input}] + constant_input
        else:
            content_input = [{"type": "text", "text": text} for text in user_input] + constant_input 
 
        chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "生成如下表格式的信息，根据提供的路径提取相关字段并整理好，供您在 Excel 中使用：\n\n---\n\n# 文件分析任务\n\n根据提供的文件路径，提取关键字段并整理格式：`文件名、粉碎物料、产业、客户、机型、材质、细度、产量`。\n\n# 条件说明\n\n1. 按路径文件名提取出各字段信息。\n2. 通用字段定义：\n   - **文件名**：路径中最后一部分的文件名，去掉扩展名。\n   - **粉碎物料**：文件名中的主要物料关键字。\n   - **产业**：依据具体常见物料用途进行归类。若路径未明确，尽量结合上下文推测。\n   - **客户**：依据路径的说明或默认值（如暂未知写“未知”）。\n   - **机型**：提取包含设备信息数值段。\n   - **材质**：若无其他说明，则默认不写材质或填写“未知”。\n   - **细度**：从文件名或路径获取过筛目数，通常为“XX目”。\n   - **产量**：从文件名或路径获取产量，通常为“XX吨每小时”。\n\n# 输出格式\n\n请输出以下字段，使用分号间隔的结构：  \n**文件名;粉碎物料;产业;客户;机型;材质;细度**\n\n# 示例输入及解析\n\n\n### 输入路径  \n`30-18.5M富里酸亚铁视频300目;富里酸亚铁;兽药，农药，肥料;山东氨纶多海洋生物原料;30-185M;不锈钢+碳钢;300目`\n`C:\\JYN\\2024-08-06\\1.0制药系统\\1.1演示图片\\1客户\\视频\\3五谷杂粮\\玉米90%过80目90-90产量：3-4吨-小时\\90-90玉米视频.mp4`\n`C:\\JYN\\2024-08-06\\1.0制药系统\\1.1演示图片\\1客户\\视频\\5肥料视频\\氨基酸视频\\粉碎视频（80-120目产量360公,小时主机50hz空分18hz风机11KW11A.mp4`\n\n### 示例输出  \n`30-18.5M富里酸亚铁视频300目;富里酸亚铁;兽药，农药，肥料;山东氨纶多海洋生物原料;30-185M;不锈钢+碳钢;300目;未知`\n`90-90玉米视频;玉米;五谷杂粮;未知;90-90;未知;80目;3-4吨每小时`\n`氨基酸粉碎视频（80-120目）;氨基酸;肥料;未知;主机50hz空分18hz风机11KW11A;未知;80-120目;360公斤/小时`"
                    }
                ]
            },
            {
                "role": "user",
                "content": content_input
            }
        ]

        try:
            completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=chat_prompt,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""

        return self.parse_output(completion)

    def parse_output(self, completion):
        
        if completion is None or not hasattr(completion, 'choices') or not completion.choices:
            print("No valid completion received.")
            return ""
        return completion.choices[0].message.content

# Example usage
if __name__ == "__main__":
    handler = APIHandler()
    user_input = ["C:\\JYN\\2024-08-06\\1.0制药系统\\1.1演示图片\\1客户\\视频\\3五谷杂粮\\玉米90%过80目90-90产量：304吨-小时\\90-90玉米视频.mp4"]
    result = handler.call_api(user_input)
    print(result)
