import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

def question_resource(courseid, workid):
    chrome_answer = webdriver.Chrome(executable_path="chromedriver.exe")
    chrome_answer.get("https://mooc1.chaoxing.com/api/selectWorkQuestion?workId=%s&courseId=%s" % (workid, courseid))
    qsts = chrome_answer.find_elements(By.CLASS_NAME, 'TiMu')
    answers = []
    for qst in qsts:
        qst = qst.find_element_by_tag_name("div")
        qst = qst.find_element_by_tag_name("div")
        question_text = qst.text.replace('\n', '')
        print(question_text)
        answer = get_answer(question_text)
        answers.append(answer)
    return answers


def get_answer(question_text):
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    # get直接返回，不再等待界⾯加载完成
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    chrome = webdriver.Chrome(executable_path="chromedriver.exe", desired_capabilities=desired_capabilities)
    chrome.get("https://cx.icodef.com/query.html?q=")
    wait = WebDriverWait(chrome, 100)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    chrome.execute_script('window.stop()')
    chrome.find_element(By.TAG_NAME, "input").send_keys(question_text[question_text.find('】')+1:])
    chrome.find_element(By.TAG_NAME, "input").send_keys(Keys.ENTER)
    answer = []
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "success")))
    for i in chrome.find_elements(By.CLASS_NAME, "success"):
        answer.append(i.text)
    print("答案为：", answer)
    if mode:
        fp = open("answer.txt", "a+")
        fp.writelines('\n' + question_text + '\n')
        fp.writelines(answer)
    return answer


def chapter_test_esp():
    sleep(3)
    #wait.until(EC.presence_of_element_located(chrome.find_element(By.TAG_NAME, "iframe")))
    for iframe1 in chrome.find_elements(By.TAG_NAME, "iframe"):
        #wait.until(EC.presence_of_element_located(chrome.find_element(By.TAG_NAME, "iframe")))
        chrome.switch_to.frame(iframe1)
        try:
            chrome.find_element(By.TAG_NAME, "iframe")
        except:
            continue
        for iframe2 in chrome.find_elements(By.TAG_NAME, "iframe"):
            #wait.until(EC.presence_of_element_located(chrome.find_element(By.TAG_NAME, "iframe")))
            chrome.switch_to.frame(iframe2)
            try:
                chrome.find_element(By.TAG_NAME, "iframe")
            except:
                continue
            for iframe3 in chrome.find_elements(By.TAG_NAME, "iframe"):
                #wait.until(EC.presence_of_element_located(chrome.find_element(By.TAG_NAME, "iframe")))
                chrome.switch_to.frame(iframe3)
                wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='ZyTop']//span")))
                if chrome.find_element(By.XPATH, "//div[@class='ZyTop']//span").text == "已完成":
                    chrome.switch_to.parent_frame()
                    print("该章节测试已提交，不用查题！")
                    continue
                workid = chrome.find_element(By.ID, "oldWorkId").get_attribute("value")
                courseid = chrome.find_element(By.ID, "courseId").get_attribute("value")
                print("作业id：%s\t课程id：%s" % (workid, courseid))
                answers = question_resource(courseid, workid)
                qsts = chrome.find_elements(By.CLASS_NAME, 'TiMu')
                count = 0
                for qst in qsts:
                    qst = qst.find_elements_by_tag_name("li")
                    for answer in answers[count]:
                        if not answer:
                            print("未找到第%d题的答案！！！" % (count + 1))
                        elif answer[0] == 'A':
                            qst[0].click()
                            print("开始选择第%d题的答案：A" % (count + 1))
                        elif answer[0] == 'B':
                            qst[1].click()
                            print("开始选择第%d题的答案：B" % (count + 1))
                        elif answer[0] == 'C':
                            qst[2].click()
                            print("开始选择第%d题的答案：C" % (count + 1))
                        elif answer[0] == 'D':
                            qst[3].click()
                            print("开始选择第%d题的答案：D" % (count + 1))
                        elif answer[0] == '×':
                            qst[1].find_element(By.TAG_NAME, 'input').click()
                            print("开始选择第%d题的答案：×" % (count + 1))
                        elif answer[0] == '√':
                            qst[0].find_element(By.TAG_NAME, 'input').click()
                            print("开始选择第%d题的答案：√" % (count + 1))
                    count += 1
                wait_time = random.randint(50, 150)
                wait_time = float(wait_time) / 10
                if mode:
                    print("该章节题目已答完！冷却%.2f秒后暂时保存！" % wait_time)
                    sleep(wait_time)
                    chrome.find_element(By.CLASS_NAME, 'btnGray_1').click()
                    wait.until(EC.alert_is_present())
                    chrome.switch_to.alert.accept()
                else:
                    print("该章节题目已答完！冷却%.2f秒后提交！" % wait_time)
                    chrome.find_element(By.CLASS_NAME, 'Btn_blue_1').click()
                    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='bluebtn ']")))
                    sleep(wait_time)
                    chrome.find_element(By.XPATH, "//a[@class='bluebtn ']").click()
                chrome.switch_to.parent_frame()
            chrome.switch_to.parent_frame()
        chrome.switch_to.parent_frame()


print("输入网址url：")
url = input()
print("输入学习通用户名：")
username = input()
print("输入学习通密码：")
password = input()
print("是否开启安全模式（输入1开启），（0关闭）：")
mode = input()
if mode == '1':
    mode = True
else:
    mode = False



LOGGER.setLevel(logging.CRITICAL)
options = webdriver.ChromeOptions()
options.add_argument('-ignore-certificate-errors')
options.add_argument('-ignore -ssl-errors')
chrome = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
chrome.get(url)
wait = WebDriverWait(chrome, 10)
chrome.find_element(By.CLASS_NAME, "ipt-tel").send_keys(username)
chrome.find_element(By.CLASS_NAME, "ipt-pwd").send_keys(password)
chrome.find_element(By.ID, "loginBtn").click()
print("登陆成功！")
print("请在切换到题目页后按enter键继续！")
input()
chapter_test_esp()
