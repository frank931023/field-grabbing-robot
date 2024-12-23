import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

# Open a new Chrome browser
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://17fit.com/account?show_fb=1&success_url=https://17fit.com/authorization/jwt?success_url=https://17fit.com/&fail_url=https://17fit.com/&cancel_url=https://17fit.com/")

def login():
    # Go to login page
    try:
        goToLoginPageButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[4]/div/div[2]/button"))
        )
        goToLoginPageButton.click()
    except Exception as e:
        print("Error go to login page:", e)

    # Input gmail
    try:
        gmail_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input.st-mb-0.st-text-black.st-p-3.st-w-full.st-border-none.st-bg-transparent"))
        )
        gmail_input.clear()
        gmail_input.send_keys("frank931023@gmail.com")

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'st-bg-primary') and contains(., '下一步')]"))
        )
        next_button.click()

    except Exception as e:
        print("Error in input gmail page:", e)

    # Input password
    try:
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )

        password_input.clear()
        password_input.send_keys("X10739y31248")  

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'st-bg-primary') and contains(., '登入')]"))
        )

        login_button.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), '我的帳戶')]"))  # 使用 "我的帳戶" 的文本
        )
        print("Login successful.")

    except Exception as e:
        print("Error in input pw page:", e)

    # Go to appointment page
    try:
        driver.get("https://17fit.com/NCUsportscenter/01?tab=appointments")
        print("Go to appointment page.")
    except Exception as e:
        print("Error in go appointment page:", e)

def click_next_button():
    try:
        # 查找"往右"按鈕並點擊
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'btn-right')]"))
        )
        next_button.click()
        print("點擊了往右按鈕。")
        time.sleep(1)  # 等待1秒以便更新頁面
    except Exception as e:
        print("錯誤: 無法找到往右按鈕:", e)


def appointment():
    # Go to badminton page
    try:
        # reservation_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/section/div[3]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div[2]/span[2]/a"))
        # )

        reservation_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/section/div[3]/div/div[2]/div/div[1]/div[2]/div/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/span[2]/a"))
        )
        reservation_button.click()

    except Exception as e:
        print("Error in clicking badminton button:", e)

    # Select court
    try:
        court_name = "室內籃球場A"
        court_item = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//h6[text()='{court_name}']/.."))
        )
        print(f"Find court: {court_name}")

        select_button = WebDriverWait(court_item, 10).until(
            EC.element_to_be_clickable((By.XPATH, ".//ancestor::div[contains(@class, 'staff_box')]//a[contains(@class, 'price')]"))
        )
        select_button.click()

    except Exception as e:
        print("Error selecting court:", e)

    # Select date
    while True:
        try:
            date_str = "10/12"
            # 查找特定日期的按鈕
            date_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH,  f"//div[@data-date='2024/{date_str}']"))
            )
            date_button.click()  # 點擊按鈕
            print(f"點擊了日期: {date_str} 的按鈕。")
            break  # 退出循環

        except Exception as e:
            print("未找到日期按鈕，嘗試按往右按鈕:", e)
            click_next_button()  # 點擊往右按鈕

    # Select time
    try:
        time_str = " 09:00 "

        # 滾動頁面確保所有元素加載
        # print("滾動頁面以確保所有時間都加載...")
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(2)
        # driver.execute_script("window.scrollTo(0, 0);")

        # 使用 XPath 查找時間，並找到對應的選擇按鈕

        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "service-flow"))
        )
        print("D")
        # small_table = WebDriverWait(table, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[@class='pt_datetime']"))
        # )
        small_table = WebDriverWait(table, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pt_datetime"))
        )
        print("E")
        # 查找所有的時間元素，避免單一查找出錯
        time_elements = small_table.find_elements(By.CLASS_NAME, "stime")
        print(f"找到 {len(time_elements)} 個時間元素")
        print("F")
        for time_element in time_elements:
            print(time_element.text.strip())

        # 遍歷找到具體時間 09:00 的元素
        # for time_element in time_elements:
        #     if time_element.text.strip() == "09:00":
        #         print("找到時間: 09:00")
        #         # 找到對應的選擇按鈕並點擊
        #         select_button = time_element.find_element(By.XPATH, "./following-sibling::a")
        #         select_button.click()
        #         print("成功點擊 09:00 的選擇按鈕")
        #         break
        # time_element = WebDriverWait(small_table, 10).until(
        #     EC.presence_of_element_located((By.XPATH, f"//div[@class='stime' and text()='09:00']"))
        # )
        # print("C")
        # select_button = time_element.find_element(By.XPATH, "./following-sibling::a")
        # print("A")
        # select_button.click()  # 點擊 "選擇" 按鈕
        # print("B")
        # time.sleep(5)

    except Exception as e:
        print(f"選擇時間時發生錯誤: {e}")



# start the process
login()
appointment()

