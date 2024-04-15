import os
import requests
import threading
from tqdm import tqdm
from retrying import retry

# 创建保存图片的文件夹
folder_path = "6-ppt1"
os.makedirs(folder_path, exist_ok=True)

# 图片所在url
base_url = "https://s3.ananas.chaoxing.com/sv-w9/doc/53/ba/8d/9a8cb8f00d506f3b24abb5edd15306f6/thumb/"

# 图片数量
total_images = 143

print(f"Downloading {total_images} pictures from {base_url}, to directory {os.path.abspath(folder_path)}")

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)

@retry(stop_max_attempt_number=3)
def retry_download_image(url, filename):
    download_image(url, filename)

def download_with_progress(i):
    url = base_url + str(i) + ".png"
    filename = os.path.join(folder_path, f"{i}.png")
    retry_download_image(url, filename)
    pbar.update(1)

# 设置进度条
with tqdm(total=total_images) as pbar:
    # 使用多线程下载图片
    threads = []
    for i in range(1, total_images + 1):
        thread = threading.Thread(target=download_with_progress, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
