from PIL import Image, ImageDraw, ImageFont
import os

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_icon(size, output_path):
    # 创建一个新的图片
    img = Image.new('RGB', (size, size), '#667EEA')
    draw = ImageDraw.Draw(img)
    
    # 绘制简单的图标
    padding = size // 4
    draw.rectangle([padding, padding, size-padding, size-padding], outline='white', width=size//20)
    draw.line([size//2, padding, size//2, size-padding], fill='white', width=size//20)
    
    # 绘制两个圆
    circle_radius = size // 8
    circle_y = size // 2
    draw.ellipse([size//3-circle_radius, circle_y-circle_radius, 
                  size//3+circle_radius, circle_y+circle_radius], fill='white')
    draw.ellipse([2*size//3-circle_radius, circle_y-circle_radius, 
                  2*size//3+circle_radius, circle_y+circle_radius], fill='white')
    
    # 保存图片
    img.save(output_path, 'PNG')

def create_splash_screen(width, height, output_path):
    # 创建一个新的图片，使用渐变色背景
    img = Image.new('RGB', (width, height), '#667EEA')
    draw = ImageDraw.Draw(img)
    
    # 在中心绘制图标
    icon_size = min(width, height) // 4
    icon_x = (width - icon_size) // 2
    icon_y = (height - icon_size) // 2
    
    # 绘制图标背景
    draw.rectangle([icon_x, icon_y, icon_x+icon_size, icon_y+icon_size], 
                  outline='white', width=icon_size//20)
    draw.line([icon_x+icon_size//2, icon_y, icon_x+icon_size//2, icon_y+icon_size], 
              fill='white', width=icon_size//20)
    
    # 绘制圆形
    circle_radius = icon_size // 8
    circle_y = icon_y + icon_size // 2
    draw.ellipse([icon_x+icon_size//3-circle_radius, circle_y-circle_radius,
                  icon_x+icon_size//3+circle_radius, circle_y+circle_radius], fill='white')
    draw.ellipse([icon_x+2*icon_size//3-circle_radius, circle_y-circle_radius,
                  icon_x+2*icon_size//3+circle_radius, circle_y+circle_radius], fill='white')
    
    # 添加文字
    try:
        font_size = min(width, height) // 30
        font = ImageFont.truetype('Arial', font_size)
        text = "漫画阅读"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (width - text_width) // 2
        text_y = icon_y + icon_size + font_size
        draw.text((text_x, text_y), text, font=font, fill='white')
    except:
        # 如果找不到字体，就跳过文字渲染
        pass
    
    # 保存图片
    img.save(output_path, 'PNG')

def generate_icons():
    icon_sizes = [
        (152, 152),  # iPad
        (167, 167),  # iPad Pro
        (180, 180),  # iPhone
    ]
    
    ensure_dir('icons')
    
    for width, height in icon_sizes:
        output_path = f'icons/icon-{width}.png'
        create_icon(width, output_path)
        print(f"Generated icon: {output_path}")

def generate_splash_screens():
    splash_sizes = [
        ('iphone5_splash', 640, 1136),
        ('iphone6_splash', 750, 1334),
        ('iphoneplus_splash', 1242, 2208),
        ('iphonex_splash', 1125, 2436),
        ('iphonexr_splash', 828, 1792),
        ('iphonexsmax_splash', 1242, 2688),
        ('ipad_splash', 1536, 2048),
        ('ipadpro1_splash', 1668, 2224),
        ('ipadpro2_splash', 1668, 2388),
        ('ipadpro3_splash', 2048, 2732),
    ]
    
    ensure_dir('splash')
    
    for name, width, height in splash_sizes:
        output_path = f'splash/{name}.png'
        create_splash_screen(width, height, output_path)
        print(f"Generated splash screen: {output_path}")

if __name__ == '__main__':
    print("Generating app assets...")
    generate_icons()
    generate_splash_screens()
    print("Done!") 