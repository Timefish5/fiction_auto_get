from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from get_informations import getNextChapter_url, getFirstChapter, getCurrentChapter_information
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

downloaded_book= {
    "https://www.22biqu.com/biqu69445/38205432_2.html": "蓝银草攻略, 作者-问珺归.txt",
    'https://www.xbiqugu.com/wapbook/76778/38314120_2.html': '海盗王权, 作者-北海牧鲸.txt'
}

# def findFirstChapter(url):
#     driver.get(url)
#     time.sleep(2)
#     first_chapter_information = getFirstChapter(url)
#     driver.quit()
#     return first_chapter_information

def writeIn_currentChapter_content(url, pre_title, book_name, author_name, driver):

    while url:
        try:
            driver.get(url)
            # 等待元素加载完毕
            content = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "content")),
            )
            next_chapter_url_a = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "next_url"))
            )
            cur_title = getCurrentChapter_information(url)

            if cur_title is None:
                print("获取标题失败")
                continue
            # Write into file
            with open(f"{book_name}, 作者-{author_name}.txt", "a", encoding="utf-8") as f:
                if pre_title != cur_title:
                    f.write("\n")
                    f.write("#" * 50)
                    f.write(cur_title)
                    f.write("\n")
                    f.write("\n")
                f.write(content.text)
                f.write("\n")

            print(cur_title + "已完成!")
            pre_title = cur_title
            # Get next chapter url
            url = next_chapter_url_a.get_attribute('href')
            if url is None:
                print("已经是最后一章了")
                driver.quit()
                downloaded_book.update({url: f"{book_name}, 作者-{author_name}.txt"})
                break
        except (NoSuchElementException, TimeoutException):
            print(f"在 {url} 找不到元素，重试中...")
            # 忽略错误并继续重新尝试当前 URL
            continue
        except Exception as e:
            print(f"发生错误: {e}")
            continue



# 下载，从目录页找到第一章，然后开始下载
def download_book(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 无头模式，不会显示浏览器窗口
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    firstChapter_information = getFirstChapter(url)
    firstChapter_url = firstChapter_information["first_chapter_url"]
    book_name = firstChapter_information["book_name"]
    author_name = firstChapter_information["author"]

    with open(f"{book_name}, 作者-{author_name}.txt", "a", encoding="utf-8") as f:
        f.write(f"{book_name}, 作者:{author_name}")
        f.write("\n")

    writeIn_currentChapter_content("https://www.22biqu.com/biqu5456/5472032_2.html", '', book_name, author_name, driver)

start_time = time.time()

download_book('https://www.22biqu.com/biqu5456/')
print(downloaded_book)





# urls = ['https://www.22biqu.com/biqu5456/', 'https://www.22biqu.com/biqu5689/','https://www.22biqu.com/biqu256/']
# for i in urls:
#     download_book(i)
#     print(downloaded_book)

end_time = time.time()
total_time = end_time - start_time
print(f"总共用时：{total_time}s")

with open("downloaded_book.txt", "w", encoding="utf-8") as f:
    for key, value in downloaded_book.items():
        f.write(f"{key}: {value}")
        f.write("\n")