from selenium import webdriver
from PIL import Image
from selenium.webdriver.chrome.service import Service
import time
import os
import datetime
import re
from urllib.parse import quote

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def capture_scroll_screenshot(job_name, targets, save_path, start_time, end_time):
    service = Service(r'/Users/huangdan/Downloads/work/googleDriver/chromedriver')
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument("--force-device-scale-factor=1")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    try:
        start_time_timestamp13 = datetime_to_timestamp13(start_time)
        end_time_timestamp13 = datetime_to_timestamp13(end_time)
        print('start_time' + start_time)
        print('start_time' + end_time)
        print('start_time_timestamp13=' + start_time_timestamp13)
        print('end_time_timestamp13' + end_time_timestamp13)
        url = 'http://172.20.10.5:3000/d/xfpJB9FGz/node-exporter-dashboard-en-20201010-starsl-cn?orgId=1&from=' + start_time_timestamp13 + '&to=' + end_time_timestamp13 + '&var-origin_prometheus=&var-job=' + chinese_to_url_encoded(
            job_name) + '&var-hostname=All' + build_query_string_nodes(
            targets) + '&var-device=All&var-interval=2m&var-maxmount=%2F&' + '&var-total=' + str(len(targets))
        print(url)
        driver.get(url)
        text_email_username = driver.find_element(By.XPATH,
                                                  "//*[@id='reactRoot']/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input")
        text_email_username.send_keys("viewer")
        text_password = driver.find_element(By.XPATH, "//*[@id='current-password']")
        text_password.send_keys("Password02!")
        button_login = driver.find_element(By.XPATH,
                                           "//*[@id='reactRoot']/div/main/div[3]/div/div[2]/div/div/form/button")
        button_login.click()
        time.sleep(5)

        button_cpubasic = driver.find_element(By.XPATH,
                                              "//*[@id='reactRoot']/div/main/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[16]/div/div[1]/header/div/h2")
        driver.execute_script("arguments[0].scrollIntoView();", button_cpubasic)
        time.sleep(1)

        save_dir = r"/Users/huangdan/Downloads/work"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        full_page_path1 = os.path.join(save_dir, job_name + "_" + build_query_string_nodes_picture(
            targets) + "_full_page1.png")
        cropped_region_path1 = os.path.join(save_dir, job_name + "_" + build_query_string_nodes_picture(
            targets) + "_1.png")
        driver.save_screenshot(full_page_path1)
        x1, y1 = 120, 115
        x2, y2 = 2765, 1320
        im = Image.open(full_page_path1)
        region = im.crop((x1, y1, x2, y2))
        region.save(cropped_region_path1)
        print(f"指定区域截图已保存至：{cropped_region_path1}")
        try:
            os.remove(full_page_path1)
            print(f"文件 {full_page_path1} 已成功删除。")
        except FileNotFoundError:
            print(f"错误：文件 {full_page_path1} 不存在。")
        except PermissionError:
            print(f"错误：没有权限删除文件 {full_page_path1}。")
        except Exception as e:
            print(f"删除文件时发生未知错误：{e}")

        button_cpubasic = driver.find_element(By.XPATH,
                                              "//*[@id='reactRoot']/div/main/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[22]/div/div[1]/header/div/h2")
        driver.execute_script("arguments[0].scrollIntoView();", button_cpubasic)
        time.sleep(1)

        save_dir = r"/Users/huangdan/Downloads/work"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        full_page_path2 = os.path.join(save_dir, job_name + "_" + build_query_string_nodes_picture(
            targets) + "_full_page2.png")
        cropped_region_path2 = os.path.join(save_dir, job_name + "_" + build_query_string_nodes_picture(
            targets) + "_2.png")
        driver.save_screenshot(full_page_path2)
        x1, y1 = 120, 182
        x2, y2 = 2767, 1480
        im = Image.open(full_page_path2)
        region = im.crop((x1, y1, x2, y2))
        region.save(cropped_region_path2)
        print(f"指定区域截图已保存至：{cropped_region_path2}")
        try:
            os.remove(full_page_path2)
            print(f"文件 {full_page_path2} 已成功删除。")
        except FileNotFoundError:
            print(f"错误：文件 {full_page_path2} 不存在。")
        except PermissionError:
            print(f"错误：没有权限删除文件 {full_page_path2}。")
        except Exception as e:
            print(f"删除文件时发生未知错误：{e}")

    finally:
        driver.quit()


def capture_scroll_screenshot_jvm(job_name, target, start_time, end_time):
    service = Service(r'/Users/huangdan/Downloads/work/googleDriver/chromedriver')
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument("--force-device-scale-factor=1")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    try:
        start_time_timestamp13 = datetime_to_timestamp13(start_time)
        end_time_timestamp13 = datetime_to_timestamp13(end_time)
        print('start_time' + start_time)
        print('start_time' + end_time)
        print('start_time_timestamp13=' + start_time_timestamp13)
        print('end_time_timestamp13' + end_time_timestamp13)
        url = 'http://172.20.10.5:3000/d/chanjarster-jvm-dashboard/jvmjian-kong?orgId=1&var-datasource=Prometheus&var-job=' + chinese_to_url_encoded(
            job_name) + '&var-instance=' + target + '&var-mempool=All&var-memarea=All&from=' + start_time_timestamp13 + '&to=' + end_time_timestamp13

        print('url' + url)
        driver.get(url)
        text_email_username = driver.find_element(By.XPATH,
                                                  "//*[@id='reactRoot']/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input")
        text_email_username.send_keys("viewer")
        text_password = driver.find_element(By.XPATH, "//*[@id='current-password']")
        text_password.send_keys("Password02!")
        button_login = driver.find_element(By.XPATH,
                                           "//*[@id='reactRoot']/div/main/div[3]/div/div[2]/div/div/form/button")
        button_login.click()
        time.sleep(3)

        button_cpubasic = driver.find_element(By.XPATH,
                                              "//*[@id='reactRoot']/div/main/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[9]/div/div[1]/header/div/h2")
        driver.execute_script("arguments[0].scrollIntoView();", button_cpubasic)
        time.sleep(3)

        save_dir = r"/Users/huangdan/Downloads/work"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        full_page_path = os.path.join(save_dir, job_name + "_" + target + "_full_page.png")
        cropped_region_path = os.path.join(save_dir, job_name + "_" + target + ".png")
        driver.save_screenshot(full_page_path)
        x1, y1 = 120, 115
        x2, y2 = 2765, 1240
        im = Image.open(full_page_path)
        region = im.crop((x1, y1, x2, y2))
        region.save(cropped_region_path)
        print(f"指定区域截图已保存至：{cropped_region_path}")
        try:
            os.remove(full_page_path)
            print(f"文件 {full_page_path} 已成功删除。")
        except FileNotFoundError:
            print(f"错误：文件 {full_page_path} 不存在。")
        except PermissionError:
            print(f"错误：没有权限删除文件 {full_page_path}。")
        except Exception as e:
            print(f"删除文件时发生未知错误：{e}")


    finally:
        driver.quit()


# 获取秒级时间戳并转换为毫秒级（13位）
def datetime_to_timestamp13(datetime_str):
    """
    入参:
    2025-10-24 19:55:44
    返回:
    1761306944000
    """
    dt_object = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    timestamp_13 = int(dt_object.timestamp() * 1000)
    return str(timestamp_13)


# 将包含中文的字符串转换为URL编码格式
def chinese_to_url_encoded(text):
    """
    入参:
    渤e短网址平台信创改造UAT服务器
    返回:
    %E6%B8%A4e%E7%9F%AD%E7%BD%91%E5%9D%80%E5%B9%B3%E5%8F%B0%E4%BF%A1%E5%88%9B%E6%94%B9%E9%80%A0UAT%E6%9C%8D%E5%8A%A1%E5%99%A8
    """
    encoded_text = str(quote(text))
    return encoded_text


# 从 Prometheus YAML 配置内容中提取 job_name 和对应的 targets
def extract_prometheus_with_regex(yaml_content):
    """
    入参:
    - job_name: "虚拟机尾号5"
    static_configs:
    - targets: ["172.20.10.5:8100","172.20.10.6:8100","172.20.10.7:8100"]
    返回:
    虚拟机尾号5
    ['172.20.10.5:8100', '172.20.10.6:8100', '172.20.10.7:8100']
    """
    try:
        # 提取job_name
        job_match = re.search(r'job_name:\s*"([^"]+)"', yaml_content)
        job_name = job_match.group(1) if job_match else "unknown_job"

        # 提取targets - 支持多组static_configs
        targets = []
        targets_blocks = re.finditer(r'static_configs:\s*(?:-?\s*targets:\s*\[([^\]]+)\])', yaml_content)

        for match in targets_blocks:
            targets.extend([t.strip(' "\'') for t in match.group(1).split(',')])

        return job_name, targets

    except Exception as e:
        print(f"YAML解析错误: {e}")
        return "error_job", []


# 将包含节点地址的列表拼接成URL查询参数字符串
def build_query_string_nodes(targets_list):
    """
    入参:
    ['172.30.36.148:8100', '172.30.36.149:8100', '172.30.52.148:8100', '172.30.52.149:8100']
    返回:
    &var-node=172.30.36.148:8100&var-node=172.30.36.149:8100&var-node=172.30.52.148:8100&var-node=172.30.52.149:8100
    """
    if not targets_list:
        return ""
    query_string = '&var-node='.join(targets_list)
    return '&var-node=' + query_string


# 将包含节点地址的列表拼接成图片命名的字符串
def build_query_string_nodes_picture(targets_list):
    """
    入参:
    ['172.30.36.148:8100', '172.30.36.149:8100', '172.30.52.148:8100', '172.30.52.149:8100']
    返回:
    &var-node=172.30.36.148:8100&var-node=172.30.36.149:8100&var-node=172.30.52.148:8100&var-node=172.30.52.149:8100
    """
    if not targets_list:
        return ""
    query_string = '_'.join(targets_list)
    return '' + query_string
