#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import random
import time
import getpass
import re
import logging
import os
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.errors import SessionPasswordNeededError, AuthRestartError

# ===== 日志配置 =====
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# ===== Emoji分类库 =====
EMOJI_CATEGORIES = {
    "basic": ["😊", "❤️", "⭐", "🔥", "🚀", "🎉", "✨", "👏", "👍", "👌"],
    "faces": ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😇", "🙂"],
    "hearts": ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💕"],
    "stars": ["⭐", "🌟", "✨", "💫", "🌠", "☄️", "🌌", "🔯"],
    "animals": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯"],
    "transport": ["🚗", "🚙", "🚌", "🚎", "🏎️", "🚓", "🚑", "🚒", "🚐", "🚀"],
    "all": None  # 特殊标记，使用时动态组合
}

# ===== 字体转换库 =====
FONT_CONVERTERS = {
    "Sans-serif Bold": {
        'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚',
        'H': '𝗛', 'I': '𝗜', 'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡',
        'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨',
        'V': '𝗩', 'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭',
        'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴',
        'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻',
        'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂',
        'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇',
        '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲',
        '7': '𝟳', '8': '𝟴', '9': '𝟵'
    },
    "MonoSpace Regular": {
        'A': 'Ａ', 'B': 'Ｂ', 'C': 'Ｃ', 'D': 'Ｄ', 'E': 'Ｅ', 'F': 'Ｆ', 'G': 'Ｇ',
        'H': 'Ｈ', 'I': 'Ｉ', 'J': 'Ｊ', 'K': 'Ｋ', 'L': 'Ｌ', 'M': 'Ｍ', 'N': 'Ｎ',
        'O': 'Ｏ', 'P': 'Ｐ', 'Q': 'Ｑ', 'R': 'Ｒ', 'S': 'Ｓ', 'T': 'Ｔ', 'U': 'Ｕ',
        'V': 'Ｖ', 'W': 'Ｗ', 'X': 'Ｘ', 'Y': 'Ｙ', 'Z': 'Ｚ',
        'a': 'ａ', 'b': 'ｂ', 'c': 'ｃ', 'd': 'ｄ', 'e': 'ｅ', 'f': 'ｆ', 'g': 'ｇ',
        'h': 'ｈ', 'i': 'ｉ', 'j': 'ｊ', 'k': 'ｋ', 'l': 'ｌ', 'm': 'ｍ', 'n': 'ｎ',
        'o': 'ｏ', 'p': 'ｐ', 'q': 'ｑ', 'r': 'ｒ', 's': 'ｓ', 't': 'ｔ', 'u': 'ｕ',
        'v': 'ｖ', 'w': 'ｗ', 'x': 'ｘ', 'y': 'ｙ', 'z': 'ｚ',
        '0': '０', '1': '１', '2': '２', '3': '３', '4': '４', '5': '５', '6': '６',
        '7': '７', '8': '８', '9': '９'
    }
}

# ===== 全局配置 =====
GLOBAL_CONFIG = {
    "api_id": "TG_API_ID",          # 请替换为真实值
    "api_hash": "TG_API_HASH",      # 请替换为真实值
    "font": "Sans-serif Bold",
    "emoji_set": "basic",
    "current_time_updates": [28],
    "next_minute_updates": [58]
}

# ===== 账号配置 =====
ACCOUNTS = [
    {   # 使用全局默认配置
        "phone": "登录手机号"  
    },
    {   # 使用特定分类
        "phone": "登陆手机号2",
        "emoji_set": ["stars", "animals", "faces", "🎯", "💎"]  # 混合分类和具体emoji
    },
    {   # 使用所有emoji 以及所有自定义配置项
        "phone": "登录手机号3",
        "emoji_set": "transport"
#        "session_name": "work_account",
#        "font": "MonoSpace Regular",
#        "emoji_set": ["all", "⚡"],  # 所有emoji+自定义
#        "time_format": "%H:%M:%S",
#        "current_time_updates": [0, 15, 30, 45],
#        "next_minute_updates": [40, 50, 55],
#        "update_interval": 0.2,
#        "auto_restart": False,
#        "max_retries": 5,
#        "proxy": {"protocol": "socks5", "host": "proxy.example.com", "port": 1080}
    }
]

def mask_phone_number(phone):
    """手机号脱敏处理（保留前4后4位）"""
    clean_phone = ''.join(filter(str.isdigit, phone))
    if len(clean_phone) <= 8:
        return phone  # 太短的号码不做处理
    return f"{clean_phone[:4]}****{clean_phone[-4:]}"

def phone_to_session_name(phone):
    """生成安全的session文件名"""
    return f"account_{''.join([c for c in phone if c.isdigit()])}"

def get_emoji_set(config):
    """获取emoji集合"""
    if config == "all":
        return [emoji for category in EMOJI_CATEGORIES.values() 
               if isinstance(category, list) for emoji in category]
    elif isinstance(config, str):
        return EMOJI_CATEGORIES.get(config, EMOJI_CATEGORIES["basic"])
    elif isinstance(config, list):
        emojis = []
        for item in config:
            if item in EMOJI_CATEGORIES:
                emojis.extend(EMOJI_CATEGORIES[item])
            else:
                emojis.append(item)
        return emojis if emojis else EMOJI_CATEGORIES["basic"]
    return EMOJI_CATEGORIES["basic"]

def get_account_config(account):
    """合并全局和账号配置"""
    config = GLOBAL_CONFIG.copy()
    config.update({k: v for k, v in account.items() if v is not None})
    config["emoji_set"] = get_emoji_set(config["emoji_set"])
    return config

async def secure_login(account_config):
    """安全登录流程"""
    session_name = phone_to_session_name(account_config["phone"])
    masked_phone = mask_phone_number(account_config["phone"])
    client = None
    
    try:
        client = TelegramClient(
            session=session_name,
            api_id=GLOBAL_CONFIG["api_id"],
            api_hash=GLOBAL_CONFIG["api_hash"],
            connection_retries=None,
            request_retries=0
        )
        
        # 禁用journal文件
        if os.path.exists(f"{session_name}.session-journal"):
            os.remove(f"{session_name}.session-journal")
        
        await client.connect()
        
        if not await client.is_user_authorized():
            print(f"\n▄ 正在登录账号: {masked_phone}")
            print("▀"*40)
            
            while True:
                try:
                    sent_code = await client.send_code_request(account_config["phone"])
                    break
                except AuthRestartError:
                    print("⚠️ 授权过程需要重启...")
                    continue
                
            for attempt in range(3):
                try:
                    code = input("↳ 请输入短信验证码: ").strip()
                    await client.sign_in(account_config["phone"], code, phone_code_hash=sent_code.phone_code_hash)
                    break
                except SessionPasswordNeededError:
                    password = getpass.getpass("↳ 请输入账户登录密码(输入时会隐藏): ")
                    await client.sign_in(password=password)
                    break
                except Exception as e:
                    if attempt < 2:
                        print(f"⚠️ 验证错误 ({str(e)}), 剩余尝试次数: {2-attempt}")
                    else:
                        raise
                        
            print(f"✅ 登录成功 | Session文件: {session_name}.session")
        else:
            print(f"✅ 自动登录成功 | 账号: {masked_phone}")
            
        return client
        
    except Exception as e:
        print(f"❌ {masked_phone} 登录失败: {str(e)}")
        if client:
            await client.disconnect()
        return None

async def account_worker(account_config, client):
    """账号主工作循环"""
    try:
        font_map = FONT_CONVERTERS.get(account_config["font"], {})
        font_convert = lambda text: ''.join([font_map.get(c, c) for c in text])
        
        masked_phone = mask_phone_number(account_config["phone"])
        print(f"\n⏰ 账号 {masked_phone} 已启动:")
        print(f"▸ 字体: {account_config['font']}")
        print(f"▸ Emoji数量: {len(account_config['emoji_set'])}")
        print(f"▸ 时间触发点: {account_config['current_time_updates']}和{account_config['next_minute_updates']}秒")
        
        last_second = -1
        
        while True:
            try:
                now = time.localtime()
                current_second = now.tm_sec
                
                if current_second != last_second:
                    last_second = current_second
                    
                    # 当前时间更新
                    if current_second in account_config["current_time_updates"]:
                        current_time = time.strftime("%H:%M", now)
                        styled_time = font_convert(current_time)
                        last_name = f"{styled_time} {random.choice(account_config['emoji_set'])}"
                        await client(UpdateProfileRequest(last_name=last_name))
                        print(f"{time.ctime()} | {masked_phone} 更新: {last_name}")
                    
                    # 下一分钟更新
                    if current_second in account_config["next_minute_updates"]:
                        next_min = now.tm_min + 1
                        next_hour = now.tm_hour
                        if next_min >= 60:
                            next_min = 0
                            next_hour += 1
                            if next_hour >= 24:
                                next_hour = 0
                        next_time = f"{next_hour:02d}:{next_min:02d}"
                        styled_time = font_convert(next_time)
                        last_name = f"{styled_time} {random.choice(account_config['emoji_set'])}"
                        await client(UpdateProfileRequest(last_name=last_name))
                        print(f"{time.ctime()} | {masked_phone} 预更新: {last_name}")
                
                await asyncio.sleep(0.1)
                
            except Exception as e:
                print(f"⚠️ {masked_phone} 工作循环错误: {str(e)}")
                await asyncio.sleep(10)
    except Exception as e:
        print(f"❌ {masked_phone} 工作循环崩溃: {str(e)}")

async def main():
    print("="*50)
    print("▌ Telegram多账号时间更新器")
    print("▌ 安全配置说明:")
    print(f"▸ API_ID: {mask_phone_number(str(GLOBAL_CONFIG['api_id']))}")
    print(f"▸ 默认字体: {GLOBAL_CONFIG['font']}")
    print(f"▸ 默认Emoji分类: {GLOBAL_CONFIG['emoji_set']}")
    print(f"▸ 时间触发点: {GLOBAL_CONFIG['current_time_updates']}和{GLOBAL_CONFIG['next_minute_updates']}秒")
    print("="*50)
    
    tasks = []
    for acc in ACCOUNTS:
        acc_cfg = get_account_config(acc)
        client = await secure_login(acc_cfg)
        if client:
            tasks.append(account_worker(acc_cfg, client))
        else:
            masked_phone = mask_phone_number(acc["phone"])
            print(f"⚠️ 跳过账号 {masked_phone}")
    
    if not tasks:
        print("❌ 没有账号登录成功")
        return
    
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\n▌ 正在安全退出...")
    finally:
        print("✅ 程序已终止")

if __name__ == '__main__':
    asyncio.run(main())
