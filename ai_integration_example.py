#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI集成示例
展示如何将ChatGPT等AI服务集成到微信自动回复中
"""

import asyncio
import aiohttp
import json
from pywechat.WechatAuto import AutoReply

# 配置AI服务（以OpenAI为例）
OPENAI_API_KEY = "your_openai_api_key_here"  # 请替换为你的API密钥
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

class AIService:
    """AI服务类，用于调用各种AI API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or OPENAI_API_KEY
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_chatgpt_response(self, message: str, context: str = "") -> str:
        """
        调用ChatGPT API获取回复
        Args:
            message: 用户消息
            context: 上下文信息
        Returns:
            AI生成的回复
        """
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return "AI服务未配置，请设置正确的API密钥"
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": f"你是一个友好的微信自动回复助手。请用简洁、友好的语气回复用户消息。{context}"
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            async with self.session.post(OPENAI_API_URL, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"].strip()
                else:
                    return f"AI服务调用失败，状态码：{response.status}"
                    
        except Exception as e:
            return f"AI服务调用出错：{str(e)}"

# 智能AI回复函数
async def ai_smart_reply_func(received_message: str, sender: str, chat_type: str) -> str:
    """
    智能AI回复函数
    使用ChatGPT等AI服务生成回复内容
    """
    # 创建AI服务实例
    async with AIService() as ai_service:
        # 构建上下文信息
        context = f"发送者：{sender}，聊天类型：{chat_type}。请根据消息内容生成合适的回复。"
        
        # 调用AI服务
        ai_response = await ai_service.get_chatgpt_response(received_message, context)
        
        # 如果AI服务不可用，使用备用回复
        if "AI服务未配置" in ai_response or "AI服务调用失败" in ai_response:
            return get_fallback_reply(received_message, sender, chat_type)
        
        return ai_response

def get_fallback_reply(received_message: str, sender: str, chat_type: str) -> str:
    """
    备用回复函数，当AI服务不可用时使用
    """
    # 简单的关键词匹配回复
    keywords = {
        "你好": f"你好 {sender}！很高兴收到你的消息 😊",
        "再见": f"再见 {sender}，期待下次聊天！👋",
        "谢谢": f"不客气 {sender}！很高兴能帮到你 😄",
        "帮助": "我可以帮你处理一些问题，请告诉我你需要什么帮助？",
        "时间": "抱歉，我无法获取实时时间，建议你查看手机或电脑的时间显示。",
        "天气": "抱歉，我无法获取实时天气信息，建议你查看天气APP或网站。"
    }
    
    # 检查消息中是否包含关键词
    for keyword, reply in keywords.items():
        if keyword in received_message:
            return reply
    
    # 默认回复
    if chat_type == "群聊":
        return f"@{sender} 收到你的消息，我会认真处理的！"
    else:
        return f"收到你的消息：{received_message}，我会尽快回复你的。"

# 多轮对话AI回复函数
class ConversationManager:
    """对话管理器，用于维护多轮对话上下文"""
    
    def __init__(self):
        self.conversations = {}  # 存储每个用户的对话历史
    
    def add_message(self, sender: str, message: str, is_user: bool = True):
        """添加消息到对话历史"""
        if sender not in self.conversations:
            self.conversations[sender] = []
        
        role = "user" if is_user else "assistant"
        self.conversations[sender].append({
            "role": role,
            "content": message,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        # 保持对话历史在合理长度内（最多10轮对话）
        if len(self.conversations[sender]) > 20:
            self.conversations[sender] = self.conversations[sender][-20:]
    
    def get_conversation_history(self, sender: str) -> list:
        """获取用户的对话历史"""
        return self.conversations.get(sender, [])

# 创建全局对话管理器实例
conversation_manager = ConversationManager()

async def multi_turn_ai_reply_func(received_message: str, sender: str, chat_type: str) -> str:
    """
    多轮对话AI回复函数
    维护对话上下文，提供更连贯的对话体验
    """
    # 添加用户消息到对话历史
    conversation_manager.add_message(sender, received_message, is_user=True)
    
    # 获取对话历史
    history = conversation_manager.get_conversation_history(sender)
    
    # 构建包含历史对话的上下文
    context_messages = []
    for msg in history[-6:]:  # 只使用最近6条消息作为上下文
        context_messages.append(f"{msg['role']}: {msg['content']}")
    
    context = f"对话历史：\n" + "\n".join(context_messages) + f"\n\n当前发送者：{sender}，聊天类型：{chat_type}。请根据对话历史生成合适的回复。"
    
    # 创建AI服务实例
    async with AIService() as ai_service:
        # 调用AI服务
        ai_response = await ai_service.get_chatgpt_response(received_message, context)
        
        # 如果AI服务可用，添加AI回复到对话历史
        if "AI服务未配置" not in ai_response and "AI服务调用失败" not in ai_response:
            conversation_manager.add_message(sender, ai_response, is_user=False)
            return ai_response
        else:
            # 使用备用回复
            fallback_reply = get_fallback_reply(received_message, sender, chat_type)
            conversation_manager.add_message(sender, fallback_reply, is_user=False)
            return fallback_reply

def main():
    """主函数：演示AI集成功能"""
    
    print("=== AI集成微信自动回复功能演示 ===")
    print("1. 基础AI回复（单轮对话）")
    print("2. 多轮对话AI回复")
    print("3. 备用回复模式")
    
    choice = input("请选择回复模式 (1-3): ")
    
    # 设置回复参数
    duration = "10min"  # 运行10分钟
    max_pages = 3       # 遍历3页会话列表
    never_reply = ["微信团队", "微信支付", "微信运动"]  # 不回复的账号
    
    if choice == "1":
        print("启动基础AI回复模式...")
        AutoReply.auto_reply_messages(
            reply_func=ai_smart_reply_func,
            duration=duration,
            max_pages=max_pages,
            never_reply=never_reply,
            scroll_delay=3  # 滚动延迟3秒
        )
    elif choice == "2":
        print("启动多轮对话AI回复模式...")
        AutoReply.auto_reply_messages(
            reply_func=multi_turn_ai_reply_func,
            duration=duration,
            max_pages=max_pages,
            never_reply=never_reply,
            scroll_delay=3
        )
    elif choice == "3":
        print("启动备用回复模式...")
        AutoReply.auto_reply_messages(
            reply_func=lambda msg, sender, chat_type: get_fallback_reply(msg, sender, chat_type),
            duration=duration,
            max_pages=max_pages,
            never_reply=never_reply,
            scroll_delay=3
        )
    else:
        print("无效选择，使用默认的备用回复模式...")
        AutoReply.auto_reply_messages(
            reply_func=lambda msg, sender, chat_type: get_fallback_reply(msg, sender, chat_type),
            duration=duration,
            max_pages=max_pages,
            never_reply=never_reply,
            scroll_delay=3
        )

if __name__ == "__main__":
    main() 