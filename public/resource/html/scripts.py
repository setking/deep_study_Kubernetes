# 批量下载html文件里面的图片
# 命令行运行 python scripts.py ./, 批量处理当前目录下的html文件
import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib
import mimetypes


def download_image(img_url, img_folder, base_url):
    """
    下载图片并返回本地保存路径
    """
    try:
        # 处理相对URL
        full_url = urljoin(base_url, img_url)

        # 发送请求下载图片
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(full_url, headers=headers, timeout=10)
        response.raise_for_status()

        # 获取文件扩展名
        content_type = response.headers.get('content-type', '')
        ext = mimetypes.guess_extension(content_type.split(';')[0])
        if not ext:
            # 尝试从URL获取扩展名
            parsed_url = urlparse(full_url)
            ext = os.path.splitext(parsed_url.path)[1]
            if not ext:
                ext = '.jpg'  # 默认扩展名

        # 使用URL的hash作为文件名,避免重复和特殊字符问题
        filename = hashlib.md5(full_url.encode()).hexdigest() + ext
        filepath = os.path.join(img_folder, filename)

        # 保存图片
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"✓ 下载成功: {full_url} -> {filename}")
        return filename

    except Exception as e:
        print(f"✗ 下载失败: {img_url} - {str(e)}")
        return None


def process_html(html_file, output_file=None, img_folder='img'):
    """
    处理HTML文件,下载图片并替换路径
    """
    # 创建图片文件夹
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
        print(f"创建文件夹: {img_folder}")

    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 获取基础URL(用于处理相对路径)
    base_url = f"file://{os.path.abspath(os.path.dirname(html_file))}/"
    base_tag = soup.find('base')
    if base_tag and base_tag.get('href'):
        base_url = base_tag.get('href')

    # 查找所有img标签
    images = soup.find_all('img')
    print(f"\n找到 {len(images)} 个图片标签")

    downloaded_count = 0

    # 处理每个图片
    for img in images:
        src = img.get('src')
        if not src:
            continue

        # 跳过base64图片
        if src.startswith('data:'):
            print(f"跳过 base64 图片")
            continue

        # 下载图片
        local_filename = download_image(src, img_folder, base_url)

        if local_filename:
            # 替换为本地路径
            img['src'] = f"{img_folder}/{local_filename}"
            downloaded_count += 1

    # 同样处理CSS中的background-image
    style_tags = soup.find_all('style')
    for style in style_tags:
        if style.string:
            # 简单的正则替换(更复杂的情况可能需要CSS解析器)
            original = style.string
            # 这里只做演示,实际可能需要更复杂的处理
            style.string = original

    # 保存修改后的HTML
    if output_file is None:
        output_file = html_file.replace('.html', '_modified.html')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"\n完成! 成功下载 {downloaded_count} 张图片")
    print(f"修改后的HTML已保存到: {output_file}")


def batch_process_html(folder_path, img_folder='img', output_suffix='_modified', recursive=False):
    """
    批量处理文件夹中的所有HTML文件

    参数:
        folder_path: 包含HTML文件的文件夹路径
        img_folder: 图片保存文件夹名称
        output_suffix: 输出文件的后缀
        recursive: 是否递归处理子文件夹
    """
    import glob

    # 查找HTML文件
    if recursive:
        pattern = os.path.join(folder_path, '**', '*.html')
        html_files = glob.glob(pattern, recursive=True)
        html_files += glob.glob(os.path.join(folder_path, '**', '*.htm'), recursive=True)
    else:
        pattern = os.path.join(folder_path, '*.html')
        html_files = glob.glob(pattern)
        html_files += glob.glob(os.path.join(folder_path, '*.htm'))

    if not html_files:
        print(f"在 '{folder_path}' 中没有找到HTML文件")
        return

    print(f"找到 {len(html_files)} 个HTML文件\n")
    print("=" * 60)

    success_count = 0
    for i, html_file in enumerate(html_files, 1):
        print(f"\n[{i}/{len(html_files)}] 处理: {html_file}")
        print("-" * 60)

        try:
            # 生成输出文件名
            base_name = os.path.splitext(html_file)[0]
            output_file = f"{base_name}{output_suffix}.html"

            # 为每个HTML文件创建独立的图片文件夹(可选)
            # 或者使用统一的图片文件夹
            file_img_folder = os.path.join(os.path.dirname(html_file), img_folder)

            process_html(html_file, output_file, file_img_folder)
            success_count += 1
        except Exception as e:
            print(f"✗ 处理失败: {str(e)}")

    print("\n" + "=" * 60)
    print(f"批量处理完成! 成功处理 {success_count}/{len(html_files)} 个文件")


if __name__ == "__main__":
    import sys

    print("HTML图片下载器 - 支持单文件和批量处理\n")

    # 使用示例
    if len(sys.argv) > 1:
        path = sys.argv[1]

        # 判断是文件还是文件夹
        if os.path.isfile(path):
            # 单文件处理
            html_file = path
            output_file = sys.argv[2] if len(sys.argv) > 2 else None
            img_folder = sys.argv[3] if len(sys.argv) > 3 else 'img'

            print("模式: 单文件处理\n")
            process_html(html_file, output_file, img_folder)

        elif os.path.isdir(path):
            # 批量处理
            folder_path = path
            img_folder = sys.argv[2] if len(sys.argv) > 2 else 'img'
            output_suffix = sys.argv[3] if len(sys.argv) > 3 else '_modified'
            recursive = '--recursive' in sys.argv or '-r' in sys.argv

            print("模式: 批量处理")
            print(f"递归处理: {'是' if recursive else '否'}\n")
            batch_process_html(folder_path, img_folder, output_suffix, recursive)
        else:
            print(f"错误: '{path}' 不是有效的文件或文件夹")
            sys.exit(1)
    else:
        # 默认参数 - 处理当前目录
        print("未指定参数,处理当前目录下的所有HTML文件\n")
        batch_process_html('.', 'img', '_modified', False)

    print("\n使用方法:")
    print("  单文件: python script.py <html文件> [输出文件] [图片文件夹]")
    print("  批量:   python script.py <文件夹> [图片文件夹] [输出后缀] [-r]")
    print("\n示例:")
    print("  python script.py index.html")
    print("  python script.py ./html_files")
    print("  python script.py ./html_files images _new")
    print("  python script.py ./html_files img _modified -r  # 递归处理子文件夹")