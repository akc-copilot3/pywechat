# 微信动态回复功能说明

## 概述

`auto_reply_messages` 方法已经升级，现在支持两种回复模式：

1. **固定内容模式**：使用预设的固定内容进行回复
2. **动态内容模式**：通过异步函数根据收到的消息动态决定回复内容

## 新功能特性

### 1. 动态回复函数支持
- 支持传入异步函数来决定回复内容
- 函数可以访问收到的消息、发送者、聊天类型等信息
- 支持返回 `None` 或空字符串来表示不回复

### 2. 智能消息处理
- 自动获取收到的消息内容
- 区分好友和群聊的不同处理逻辑
- 支持异常处理和错误恢复

### 3. 异步处理
- 使用 `asyncio` 支持异步操作
- 可以集成AI服务、数据库查询等异步操作
- 保持原有的同步兼容性

## 使用方法

### 基本用法

#### 固定内容模式（原有功能）
```python
from pywechat.WechatAuto import AutoReply

# 使用固定内容回复
AutoReply.auto_reply_messages(
    content="您好，我现在不在，稍后回复您。",
    duration="30min",
    max_pages=5
)
```

#### 动态内容模式（新功能）
```python
import asyncio
from pywechat.WechatAuto import AutoReply

# 定义动态回复函数
async def my_reply_func(received_message: str, sender: str, chat_type: str) -> str:
    if "你好" in received_message:
        return f"你好 {sender}！很高兴收到你的消息。"
    elif "再见" in received_message:
        return f"再见 {sender}，期待下次聊天！"
    else:
        return f"收到你的消息：{received_message}，我会尽快回复你。"

# 使用动态回复函数
AutoReply.auto_reply_messages(
    reply_func=my_reply_func,
    duration="30min",
    max_pages=5
)
```

### 高级用法

#### AI集成示例
```python
import asyncio
import aiohttp
from pywechat.WechatAuto import AutoReply

async def ai_reply_func(received_message: str, sender: str, chat_type: str) -> str:
    # 调用AI服务生成回复
    async with aiohttp.ClientSession() as session:
        # 这里可以调用ChatGPT、文心一言等AI服务
        # 示例代码...
        return "AI生成的回复内容"

AutoReply.auto_reply_messages(
    reply_func=ai_reply_func,
    duration="1h",
    max_pages=3
)
```

#### 条件回复示例
```python
async def conditional_reply_func(received_message: str, sender: str, chat_type: str) -> str:
    # 某些好友不回复
    if sender in ["张三", "李四"]:
        return None  # 不回复
    
    # 某些关键词不回复
    if any(keyword in received_message for keyword in ["广告", "推销"]):
        return None  # 不回复
    
    # 正常回复
    return f"自动回复：收到来自 {sender} 的消息"

AutoReply.auto_reply_messages(
    reply_func=conditional_reply_func,
    duration="2h",
    max_pages=5
)
```

## 函数签名

### 动态回复函数签名
```python
async def reply_func(received_message: str, sender: str, chat_type: str) -> str:
    """
    动态回复函数
    
    Args:
        received_message: 收到的消息内容
        sender: 发送者名称
        chat_type: 聊天类型（'好友' 或 '群聊'）
    
    Returns:
        str: 要回复的消息内容
        None 或空字符串: 不回复
    """
    pass
```

### 主方法签名
```python
def auto_reply_messages(
    content=None,                    # 固定回复内容
    reply_func=None,                 # 动态回复函数
    duration: str = "",              # 运行时长
    dontReplytoGroup: bool = False,  # 是否不回复群聊
    max_pages: int = 5,              # 最大遍历页数
    never_reply: list = [],          # 不回复的账号列表
    scroll_delay: int = 0,           # 滚动延迟
    wechat_path: str = None,         # 微信路径
    is_maximize: bool = True,        # 是否全屏
    close_wechat: bool = True        # 是否关闭微信
) -> None:
```

## 参数说明

### 新增参数

- **content**: 固定回复内容（与 reply_func 二选一）
- **reply_func**: 动态回复函数（与 content 二选一）

### 原有参数

- **duration**: 运行时长，格式：'s'、'min'、'h'
- **dontReplytoGroup**: 是否不回复群聊
- **max_pages**: 遍历会话列表的页数
- **never_reply**: 不回复的账号列表
- **scroll_delay**: 滚动延迟（秒）
- **wechat_path**: 微信程序路径
- **is_maximize**: 是否全屏显示
- **close_wechat**: 是否关闭微信

## 注意事项

### 1. 参数验证
- `content` 和 `reply_func` 必须提供其中一个
- 不能同时提供两个参数
- `reply_func` 必须是异步函数
- `duration` 参数不能为空

### 2. 异常处理
- 动态回复函数中的异常会被捕获并打印错误信息
- 不会影响整个自动回复流程
- 建议在回复函数中添加适当的异常处理

### 3. 性能考虑
- 异步函数应该尽快返回结果
- 避免在回复函数中执行耗时操作
- 如果需要调用外部API，建议设置超时时间

### 4. 安全性
- 确保回复内容符合微信使用规范
- 避免发送敏感信息
- 建议对输入消息进行过滤和验证

## 示例文件

项目包含以下示例文件：

1. **dynamic_reply_example.py**: 基础动态回复示例
2. **ai_integration_example.py**: AI服务集成示例

## 兼容性

- 新功能完全向后兼容
- 原有的固定内容模式保持不变
- 可以无缝升级到新版本

## 更新日志

### v2.0.0
- 新增动态回复函数支持
- 支持异步操作
- 增强错误处理
- 改进文档和示例 