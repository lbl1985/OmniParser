import os  
import base64
from openai import AzureOpenAI  

endpoint = os.getenv("ENDPOINT_URL", "https://jynllm3164666857.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "")  

# Initialize Azure OpenAI Service client with key-based authentication    
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",
)
    
    
# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

#Prepare the chat prompt 
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "生成如下表格式的信息，根据提供的路径提取相关字段并整理好，供您在 Excel 中使用：\n\n---\n\n# 文件分析任务\n\n根据提供的文件路径，提取关键字段并整理格式：`文件名、粉碎物料、产业、客户、机型、材质、细度`。\n\n# 条件说明\n\n1. 按路径文件名提取出各字段信息。\n2. 通用字段定义：\n   - **文件名**：路径中最后一部分的文件名，去掉扩展名。\n   - **粉碎物料**：文件名中的主要物料关键字。\n   - **产业**：依据具体常见物料用途进行归类。若路径未明确，尽量结合上下文推测。\n   - **客户**：依据路径的说明或默认值（如暂未知写“未知”）。\n   - **机型**：提取包含的产量、设备信息数值段。\n   - **材质**：若无其他说明，则默认不写材质或填写“未知”。\n   - **细度**：从文件名或路径获取过筛目数，通常为“XX目”。\n\n# 输出格式\n\n请输出以下字段，使用分号间隔的结构：  \n**文件名;粉碎物料;产业;客户;机型;材质;细度**\n\n# 示例输入及解析\n\n\n### 输入路径  \n`30-18.5M富里酸亚铁视频300目;富里酸亚铁;兽药，农药，肥料;山东氨纶多海洋生物原料;30-185M;不锈钢+碳钢;300目`\n`C:\\JYN\\2024-08-06\\1.0制药系统\\1.1演示图片\\1客户\\视频\\3五谷杂粮\\玉米90%过80目90-90产量：304吨-小时\\90-90玉米视频.mp4`\n\n### 示例输出  \n`30-18.5M富里酸亚铁视频300目;富里酸亚铁;兽药，农药，肥料;山东氨纶多海洋生物原料;30-185M;不锈钢+碳钢;300目`\n`90-90玉米视频;玉米;五谷杂粮;未知;90-90;未知;80目`"
            }
        ]
    },
    {
        "role": "user",
        "content": [
                        {
                "type": "text",
                "text": "`C:\\JYN\\2024-08-06\\1.0制药系统\\1.2兽药及农药、肥料\\6 肥料\\1不锈钢+碳钢\\新疆展会40-37二氢钾视频.mp4`"
            },
            {
                "type": "text",
                "text": "`C:\\JYN\\2024-08-06\\1.0制药系统\\1.2兽药及农药、肥料\\6 肥料\\1不锈钢+碳钢\\30-18.5M粉碎二氢钾1000公斤+微量视频.mp4`"
            },
            {
                "type": "text",
                "text": "`C:\\JYN\\2024-08-06\\1.0制药系统\\江苏神华\\黄源胶原料.mp4`"
            },
            {
                "type": "text",
                "text": "请只输出结果。不需要说明"
            }
        ]
    }
] 
    
# Include speech result if speech is enabled  
messages = chat_prompt  
    
# Generate the completion  
completion = client.chat.completions.create(  
    model=deployment,
    messages=messages,
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,
    stop=None,  
    stream=False
)

print(completion.to_json())  
    