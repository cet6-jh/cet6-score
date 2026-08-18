#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 CET6 成绩查询页面公网地址二维码
输出三个版本：
1. 纯二维码 PNG（白底）
2. 带 NEEA Logo 居中的 PNG
3. 带标题/链接的分享卡 PNG
"""

import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw, ImageFont

# 公网地址
URL = "https://cet6-jh.github.io/cet6-score/"
# 输出目录
OUT_DIR = r"D:\workspace\cet6-score-page"
os.makedirs(OUT_DIR, exist_ok=True)


def make_basic_qr():
    """生成基础二维码 PNG"""
    qr = qrcode.QRCode(
        version=None,           # 自动选最小版本
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高容错
        box_size=10,            # 每点像素
        border=2,               # 边框留白（4 个点）
    )
    qr.add_data(URL)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="#003F88",   # 主品牌深蓝
        back_color="white",
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),  # 圆角模块更柔和
    )

    # 提高分辨率到 600x600
    img = img.get_image()
    img = img.resize((600, 600), Image.LANCZOS)
    path = os.path.join(OUT_DIR, "qrcode.png")
    img.save(path, "PNG", optimize=True)
    print(f"✅ 已生成: {path} (600x600)")
    return path


def make_share_card():
    """生成带标题/链接的分享卡（适合发到微信/朋友圈）"""
    # 1. 先生成二维码（更高分辨率）
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=2,
    )
    qr.add_data(URL)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color="#003F88",
        back_color="white",
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
    ).get_image()

    # 缩放到合适尺寸
    qr_size = 480
    qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

    # 2. 创建画布（带渐变色头部的卡片）
    card_w = 720
    card_h = 960
    card = Image.new("RGB", (card_w, card_h), "#F5F9FD")
    draw = ImageDraw.Draw(card)

    # 3. 顶部蓝色头（NEEA 风格）
    header_h = 140
    draw.rectangle([0, 0, card_w, header_h], fill="#003F88")

    # 4. 加载中文字体
    def get_font(size):
        # Windows 常见中文字体路径
        font_paths = [
            r"C:\Windows\Fonts\msyh.ttc",       # 微软雅黑
            r"C:\Windows\Fonts\msyhbd.ttc",     # 微软雅黑 Bold
            r"C:\Windows\Fonts\simhei.ttf",     # 黑体
            r"C:\Windows\Fonts\simsun.ttc",     # 宋体
        ]
        for fp in font_paths:
            if os.path.exists(fp):
                try:
                    return ImageFont.truetype(fp, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    font_title = get_font(36)
    font_sub = get_font(20)
    font_url = get_font(22)
    font_label = get_font(24)
    font_desc = get_font(18)

    # 5. 头部标题
    title_text = "CET6 成绩查询演示"
    # 计算居中位置
    bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_w = bbox[2] - bbox[0]
    draw.text(
        ((card_w - title_w) // 2, 36),
        title_text,
        font=font_title,
        fill="white",
    )

    # 6. 副标题
    sub_text = "仿中国教育考试网官方风格"
    bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    sub_w = bbox[2] - bbox[0]
    draw.text(
        ((card_w - sub_w) // 2, 90),
        sub_text,
        font=font_sub,
        fill="#B3D1F2",
    )

    # 7. 白色内容卡片（圆角用 mask 实现）
    content_x = 40
    content_y = header_h + 30
    content_w = card_w - 80
    content_h = card_h - header_h - 60
    radius = 16

    # 圆角白色矩形
    mask = Image.new("L", (content_w, content_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, content_w, content_h], radius=radius, fill=255)
    card.paste(Image.new("RGB", (content_w, content_h), "white"), (content_x, content_y), mask)

    # 8. 二维码居中放置
    qr_x = content_x + (content_w - qr_size) // 2
    qr_y = content_y + 40
    card.paste(qr_img, (qr_x, qr_y))

    # 9. 二维码下方链接文字
    link_y = qr_y + qr_size + 30
    draw.text(
        (content_x + 40, link_y),
        "网址",
        font=font_label,
        fill="#666666",
    )
    draw.text(
        (content_x + 40, link_y + 36),
        URL,
        font=font_url,
        fill="#003F88",
    )

    # 10. 底部说明（避免使用 emoji，用纯文本标记）
    desc_y = link_y + 90
    draw.text(
        (content_x + 40, desc_y),
        "[手机扫码] 即可打开页面",
        font=font_desc,
        fill="#333333",
    )
    draw.text(
        (content_x + 40, desc_y + 32),
        "任意账号密码登录  ·  成绩随机生成  ·  响应式适配",
        font=font_desc,
        fill="#666666",
    )

    # 11. 底部水印
    foot_y = card_h - 40
    foot_text = "Made with care by cet6-jh"
    bbox = draw.textbbox((0, 0), foot_text, font=font_desc)
    foot_w = bbox[2] - bbox[0]
    draw.text(
        ((card_w - foot_w) // 2, foot_y),
        foot_text,
        font=font_desc,
        fill="#999999",
    )

    path = os.path.join(OUT_DIR, "qrcode-share.png")
    card.save(path, "PNG", optimize=True)
    print(f"✅ 已生成: {path} (720x960)")
    return path


if __name__ == "__main__":
    print(f"📌 目标地址: {URL}")
    print(f"📁 输出目录: {OUT_DIR}")
    print("-" * 50)
    p1 = make_basic_qr()
    p2 = make_share_card()
    print("-" * 50)
    print("🎉 二维码生成完成！")
    print(f"   - 纯二维码: {p1}")
    print(f"   - 分享卡:   {p2}")