#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态回复功能使用示例
展示如何使用 auto_reply_messages 方法的动态回复功能
"""

import asyncio
from pywechat.WechatAuto import AutoReply

# 示例1：简单的动态回复函数
async def simple_reply_func(received_message: str, sender: str, chat_type: str) -> str:
    """
    简单的动态回复函数
    Args:
        received_message: 收到的消息内容
        sender: 发送者名称
        chat_type: 聊天类型（'好友' 或 '群聊'）
    Returns:
        要回复的消息内容，返回None或空字符串则不回复
    """
    # 根据消息内容决定回复
    if "你好" in received_message:
        return f"你好 {sender}！很高兴收到你的消息。"
    elif "再见" in received_message:
        return f"再见 {sender}，期待下次聊天！"
    elif "帮助" in received_message:
        return "我可以帮你处理一些简单的问题，请告诉我你需要什么帮助。"
    else:
        return f"收到你的消息：{received_message}，我会尽快回复你。"

# 示例2：智能回复函数（可以接入AI服务）
async def ai_reply_func(received_message: str, sender: str, chat_type: str) -> str:
    """
    智能回复函数（示例：可以接入ChatGPT等AI服务）
    """
    # 这里可以调用AI API，比如OpenAI的ChatGPT
    # 示例实现：
    if chat_type == "群聊":
        # 群聊中的回复
        if "天气" in received_message:
            return "今天天气不错，适合出门走走！"
        elif "时间" in received_message:
            import datetime
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"当前时间是：{current_time}"
        else:
            return f"@{sender} 收到你的消息，我会认真处理的。"
    else:
        # 私聊中的回复
        if len(received_message) < 10:
            return f"收到你的短消息：{received_message}"
        else:
            return f"收到你的长消息，内容很丰富！我会仔细阅读并回复你的。"

# 示例3：条件回复函数
async def conditional_reply_func(received_message: str, sender: str, chat_type: str) -> str:
    """
    条件回复函数：根据发送者和消息内容决定是否回复
    """
    # 某些好友不回复
    if sender in ["张三", "李四"]:
        return None  # 不回复
    
    # 某些关键词不回复
    if any(keyword in received_message for keyword in ["广告", "推销", "垃圾"]):
        return None  # 不回复
    
    # 正常回复
    return f"自动回复：收到来自 {sender} 的消息，内容：{received_message}"

def main():
    """主函数：演示如何使用动态回复功能"""
    
    print("=== 微信自动回复功能演示 ===")
    print("1. 简单动态回复")
    print("2. AI智能回复")
    print("3. 条件回复")
    
    choice = input("请选择回复模式 (1-3): ")
    
    # 设置回复参数
    duration = "5min"  # 运行5分钟
    max_pages = 3      # 遍历3页会话列表
    never_reply = ["微信团队", "微信支付"]  # 不回复的账号
    
    if choice == "1":
        print("启动简单动态回复模式...")
        AutoReply.auto_reply_messages(
            reply_func=simple_reply_func,
            duration=duration,
            max_pages=max_pages,
            never_reply=never_reply,
            scroll_delay=2  # 滚动延迟2秒
        )
    elif choice == "2":
        print("启动AI智能回复模式...")
        AutoReply.auto_reply_messages(
            reply_func=ai_reply_func,
            duration=duration,
            max_pages=max_pages,
            never_reply=never_reply,
            scroll_delay=2
        )
    elif choice == "3":
        print("启动条件回复模式...")
        AutoReply.auto_reply_messages(
            reply_func=conditional_reply_func,
            duration=duration,
            max_pages=max_pages,
            never_reply=never_reply,
            scroll_delay=2
        )
    else:
        print("无效选择，使用默认的简单回复模式...")
        AutoReply.auto_reply_messages(
            reply_func=simple_reply_func,
            duration=duration,
            max_pages=max_pages,
            never_reply=never_reply,
            scroll_delay=2
        )

if __name__ == "__main__":
    main() 