from selenium import webdriver
import time
import os


# 临时操作
with open('./config/urls_pdf_for_download.txt', 'r', encoding="utf8") as f:
    lines = f.readlines()
file_list = [line.strip() for line in lines]

url_list = file_list

# 定义需要下载的链接列表
# url_list = [ ]

opt = webdriver.ChromeOptions()
# opt.set_headless()
opt.add_experimental_option('prefs', {
    'plugins.always_open_pdf_externally': True,
    'download.default_directory': '.'
})

driver = webdriver.Chrome(options=opt)


pdf_count = 0
# 遍历根目录下的所有文件和文件夹
for root, dirs, files in os.walk('D:\\用户目录\\下载'):
    for file in files:
        if file.endswith('.pdf'):  # 如果文件以.pdf为扩展名，则计数器加1
            pdf_count += 1
print(pdf_count)

# 循环遍历链接列表
for url in url_list:
    # 使用Chrome浏览器打开链接
    try:
        driver.get(url)
        max_wait = 0
        while True:
            time.sleep(1)
            pdf_count_new = 0
            for root, dirs, files in os.walk('D:\\用户目录\\下载'):
                for file in files:
                    if file.endswith('.pdf'):  # 如果文件以.pdf为扩展名，则计数器加1
                        pdf_count_new += 1
            if pdf_count_new > pdf_count or max_wait > 60:
                pdf_count = pdf_count_new
                break
            else:
                max_wait += 1

        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 's')
        # driver.find_element_by_class_name('saveAs').click()
        # driver.find_element_by_id('save').click()

        # driver.execute_script("chrome.downloads.setPromptBehavior('allow');")

        # # 获取链接中的文件名
        # file_name = url.split('/')[-1]

        # # 下载文件到指定路径
        # with open(file_name, 'wb') as f:
        #     f.write(driver.find_element_by_tag_name('embed').get_attribute('src').split(',')[1].encode('utf-8'))

        # print(file_name)
        # print("============已下载")
        # time.sleep(4)

    except:
        print("爬取失败:", end='')
        print(url)
        continue

time.sleep(200)
# 关闭浏览器
driver.quit()
