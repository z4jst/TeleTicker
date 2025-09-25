# Telegram 多账号时间更新器

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Telethon](https://img.shields.io/badge/Telethon-1.25+-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

基于 [xyou365/Telegram-Name-Updating](https://github.com/xyou365/Telegram-Name-Updating) 项目改进的多账号时间自动更新工具，支持自定义字体样式、Emoji组合和触发时间点。

## ✨ 功能特性

- **多账号管理**：同时运行多个Telegram账号
- **时间动态更新**：在指定秒数自动更新显示时间
- **样式自定义**：
  - 10+种特殊字体（数学符号、等宽字体等）
  - 200+个分类Emoji（基础表情、爱心、星星、动物等）
- **隐私保护**：自动脱敏显示手机号
- **稳定运行**：崩溃自动恢复+网络重连

## 📦 安装依赖

bash
pip install telethon==1.28.0

## 环境配置
python3 -m venv venv
# 激活虚拟环境
source venv/bin/activate
# 然后在虚拟环境中安装依赖
pip install -r requirements.txt
# 运行脚本
python TeleTicker.py
# 完成后退出虚拟环境
deactivate

## ⚙️ 配置教程

### 1. 基础配置

编辑脚本中的全局配置部分：

python
GLOBAL_CONFIG = {
    "api_id": 1234567,              # 从 https://my.telegram.org/app 获取
    "api_hash": "abcdef1234567890", # 同上
    "font": "Sans-serif Bold",     # 默认字体
    "emoji_set": "basic",          # 默认emoji分类
    "current_time_updates": [0],    # 在每分钟的第0秒更新
    "next_minute_updates": [55]    # 在每分钟的第55秒预更新下一分钟
}


### 2. 账号配置

在`ACCOUNTS`列表中添加您的账号：

python
ACCOUNTS = [
    {   # 极简配置
        "phone": "+8613123456789"
    },
    {   # 自定义配置
        "phone": "+8613987654321",
        "font": "MonoSpace Regular",
        "emoji_set": ["hearts", "stars", "🚀"],
        "current_time_updates": [5, 25],
        "next_minute_updates": [50, 55]
    }
]


### 3. Emoji分类说明

内置分类（完整列表见代码）：
- `basic`: 😊 ❤️ ⭐ 🔥 🚀 🎉 ✨ 👏 👍 👌
- `hearts`: ❤️ 🧡 💛 💚 💙 💜 🖤 🤍 🤎 💕
- `stars`: ⭐ 🌟 ✨ 💫 🌠 ☄️ 🌌 🔯
- `animals`: 🐶 🐱 🐭 🐹 🐰 🦊 🐻 🐼 🐨 🐯
- `all`: 所有emoji组合

## 🚀 使用教程

### 首次运行

bash
python TeleTicker.py


按提示输入：
1. 短信验证码
2. 二次验证密码（如启用）

### 查看运行状态

成功登录后会显示：

✅ 账号 86136789 已启动:
▸ 字体: Sans-serif Bold
▸ Emoji数量: 78
▸ 时间触发点: [0]和[55]秒


### 日志示例


Thu Sep 26 15:00:00 2024 | 86136789 更新: 𝟭𝟱:𝟬𝟬 🚀
Thu Sep 26 15:00:55 2024 | 86136789 预更新: 𝟭𝟱:𝟬𝟭 ⭐


### 停止运行

按 `Ctrl+C` 安全退出所有账号

## 🛠️ 高级定制

### 添加自定义字体

在`FONT_CONVERTERS`中添加：

python
FONT_CONVERTERS["My Font"] = {
    'A': 'ᗩ', 'B': 'ᗷ',  # 自定义字符映射
    # ...
}


### 创建Emoji组合

python
EMOJI_CATEGORIES["my_set"] = ["⚡", "💎", "🪄"]


## 📜 版权声明

本项目基于 [xyou365/Telegram-Name-Updating](https://github.com/xyou365/Telegram-Name-Updating) 二次开发，特别感谢原作者的创意贡献！

## 💡 常见问题

**Q：如何解决登录失败问题？**
A：检查：
1. API_ID和HASH是否正确
2. 手机号是否包含国家代码（如+86）
3. 是否开启二次验证（需要密码）

**Q：如何彻底删除账号数据？**
A：删除对应的 `.session` 文件即可

**Q：支持Telegram机器人账号吗？**
A：需要修改为使用bot_token方式登录

## 📁 文件结构


TeleTicker/
├── TeleTicker.py    # 主程序文件
├── account_*.session     # 自动生成的会话文件（首次运行后）
└── README.md            # 说明文档


## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进本项目！

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

> 📮 如有其他问题，欢迎提交Issue或联系开发者
