from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.chrome.service import Service
import time
import os

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def capture_scroll_screenshot(url, save_path):
    service = Service(r'/Users/huangdan/Downloads/work/googleDriver/chromedriver')
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument("--force-device-scale-factor=1")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    try:
        driver.get(url)
        text_email_username = driver.find_element(By.XPATH, "//*[@id='reactRoot']/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input")
        text_email_username.send_keys("viewer")
        text_password = driver.find_element(By.XPATH, "//*[@id='current-password']")
        text_password.send_keys("Password02!")
        button_login = driver.find_element(By.XPATH, "//*[@id='reactRoot']/div/main/div[3]/div/div[2]/div/div/form/button")
        button_login.click()
        time.sleep(2)
        button_last30minites = driver.find_element(By.XPATH, "//*[@id='reactRoot']/div/main/div[3]/header/div/div[5]/div/div[1]/button[1]")
        button_last30minites.click()
        text_from = driver.find_element(By.XPATH, "//*[@id='TimePickerContent']/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/input")
        text_from.clear()
        text_from.send_keys("2025-10-17 00:00:00")
        text_to = driver.find_element(By.XPATH, "//*[@id='TimePickerContent']/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[1]/input")
        text_to.clear()
        text_to.send_keys("2025-10-17 23:00:00")
        button_applytimerange = driver.find_element(By.XPATH, "//*[@id='TimePickerContent']/div[1]/div[2]/div[1]/div[2]/button")
        button_applytimerange.click()
        time.sleep(3)



        button_cpubasic = driver.find_element(By.XPATH, "//*[@id='reactRoot']/div/main/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[16]/div/div[1]/header/div/h2")
        driver.execute_script("arguments[0].scrollIntoView();", button_cpubasic)
        time.sleep(1)

        save_dir = r"/Users/huangdan/Downloads/work"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        full_page_path = os.path.join(save_dir, "ecs_resourece_full_page1.png")
        cropped_region_path = os.path.join(save_dir, "ecs_resourece_cropped_region1.png")
        driver.save_screenshot(full_page_path)
        x1, y1 = 120, 115
        x2, y2 = 2765, 1320
        im = Image.open(full_page_path)
        region = im.crop((x1, y1, x2, y2))
        region.save(cropped_region_path)
        print(f"指定区域截图已保存至：{cropped_region_path}")



        button_cpubasic = driver.find_element(By.XPATH, "//*[@id='reactRoot']/div/main/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[22]/div/div[1]/header/div/h2")
        driver.execute_script("arguments[0].scrollIntoView();", button_cpubasic)
        time.sleep(1)

        save_dir = r"/Users/huangdan/Downloads/work"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        full_page_path = os.path.join(save_dir, "ecs_resourece_full_page2.png")
        cropped_region_path = os.path.join(save_dir, "ecs_resourece_cropped_region2.png")
        driver.save_screenshot(full_page_path)
        x1, y1 = 120, 182
        x2, y2 = 2767, 1480
        im = Image.open(full_page_path)
        region = im.crop((x1, y1, x2, y2))
        region.save(cropped_region_path)
        print(f"指定区域截图已保存至：{cropped_region_path}")


        driver.execute_script("document.body.style.zoom='150%'")
        time.sleep(3)

        # 获取页面信息
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")

        # 创建空白画布
        screenshot = Image.new('RGB', (driver.execute_script("return window.innerWidth"), total_height))
        current_position = 0

        while current_position < total_height:
            # 滚动到当前位置
            driver.execute_script(f"window.scrollTo(0, {current_position})")
            time.sleep(0.5)  # 等待滚动稳定

            # 截取当前视口并转换为PIL图像
            screenshot_binary = driver.get_screenshot_as_png()
            img = Image.open(BytesIO(screenshot_binary))

            # 计算本次粘贴的位置
            paste_y = current_position
            # 如果是最后一次滚动，且剩余高度不足一个视口，需要调整粘贴位置
            if current_position + viewport_height > total_height:
                paste_y = total_height - img.height

            screenshot.paste(img, (0, paste_y))
            current_position += viewport_height  # 滚动一个视口高度

        screenshot.save(save_path)
        print(f"滚动拼接截图已保存至：{save_path}")

    finally:
        driver.quit()
