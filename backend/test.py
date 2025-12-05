import os
import httpx
from openai import OpenAI
from dotenv import load_dotenv
import base64

# 加载环境变量
load_dotenv()

print("开始初始化...")

# 初始化客户端 - 使用自定义 HTTP 客户端
try:
    # 创建自定义 HTTP 客户端
    http_client = httpx.Client()

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        http_client=http_client,  # 显式传递 HTTP 客户端
    )
    print("OpenAI客户端初始化成功")
except Exception as e:
    print(f"OpenAI客户端初始化失败: {e}")
    import traceback

    traceback.print_exc()
    client = None


def test_text_model():
    """测试文本模型是否工作"""
    if client is None:
        print("客户端未初始化，跳过测试")
        return False

    try:
        print("测试文本模型...")
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "user", "content": "你好，请回复'测试成功'"}
            ],
            max_tokens=50
        )
        print(f"文本模型测试成功: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"文本模型测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_vision_model_with_base64():
    """测试视觉模型使用base64图片数据"""
    if client is None:
        print("客户端未初始化，跳过测试")
        return False

    try:
        print("测试视觉模型（使用base64图片数据）...")

        # 使用一个16x16红色像素图片的base64编码，确保尺寸满足模型要求
        # 图片尺寸大于10x10像素，符合API要求
        base64_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAjSURBVChTYxjx8j7/3NnzBwg4MjAwMAQCAcQHwBZQwD8QnQAAAABJRU5ErkJggg=="

        response = client.chat.completions.create(
            model="qwen-vl-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "描述这张图片的颜色和大小"},
                        {"type": "image_url", "image_url": {"url": base64_image}}
                    ]
                }
            ],
            max_tokens=100
        )
        print(f"视觉模型测试成功: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"视觉模型测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_vision_model_with_valid_url():
    """测试视觉模型使用有效的图片URL"""
    if client is None:
        print("客户端未初始化，跳过测试")
        return False

    try:
        print("测试视觉模型（使用有效图片URL）...")

        # # 使用一个已知有效的图片URL（来自阿里云官方文档示例）
        # valid_image_url = "https://dashscope.aliyuncs.com/cn/upload/2024/01/18/9d17d345-67a6-4b1a-8a7f-6c5b9e9b9e9e.png"

        # 或者使用一个简单的公开图片
        valid_image_url = "https://ts1.tc.mm.bing.net/th/id/R-C.8a18ef2da35c1ada00045d93196ac8af?rik=h1bkecHoshfhaA&riu=http%3a%2f%2fpic.baike.soso.com%2fp%2f20130625%2f20130625170650-1038001012.jpg&ehk=2QEf1EiDJVn5BNbacNMGPw140MsSWrvbS7Y8RpDS7ko%3d&risl=&pid=ImgRaw&r=0"  # 替换为实际可访问的图片URL

        response = client.chat.completions.create(
            model="qwen-vl-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "描述这张图片"},
                        {"type": "image_url", "image_url": {"url": valid_image_url}}
                    ]
                }
            ],
            max_tokens=100
        )
        print(f"视觉模型测试成功: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"视觉模型测试失败: {e}")
        print("注意：这个测试需要可公开访问的图片URL")
        return False


if __name__ == "__main__":
    print("开始测试API连接...")
    print(f"API Key 前10位: {os.getenv('OPENAI_API_KEY')[:10]}...")

    if client:
        text_success = test_text_model()

        # 先测试base64图片
        vision_success = test_vision_model_with_base64()

        # 如果base64失败，再测试URL（可选）
        if not vision_success:
            print("Base64图片测试失败，尝试使用URL图片...")
            vision_success = test_vision_model_with_valid_url()

        if text_success and vision_success:
            print("所有测试都成功！")
        else:
            print("部分测试失败，请检查配置。")
    else:
        print("客户端初始化失败，无法进行测试")