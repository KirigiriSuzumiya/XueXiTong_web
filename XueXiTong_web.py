import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
import sys
import threading
from datetime import datetime, timedelta

exitFlag = False

# 配置所刷课程的url和学习通的用户名密码 - 控制台输入
args = sys.argv
url = args[1]
username = args[2]
password = args[3]
print("自定义多标签任务点tag内容：不明白什么意思可以参阅README")
tag_video = args[4]
tag_test = args[5]


class myThread(threading.Thread):
    def __init__(self, threadID, name, delay, duration):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay
        self.duration = duration

    def run(self):
        print("开始打印进度线程：" + self.name)
        query_progress(self.name, self.delay, self.duration)
        print("退出打印进度线程：" + self.name)


def query_progress(thread_name, delay, duration):
    global exitFlag
    while True:
        if exitFlag:
            break
        javascript_to_execute = "return document.getElementById('video_html5_api').currentTime"
        current_time = chrome.execute_script(javascript_to_execute)
        now_time = datetime.now()
        print("[%s]:视频播放中:总时长：%s秒,当前进度:%s秒" % (
            now_time.strftime("%Y-%m-%d %H:%M:%S"), duration, current_time))
        sleep(delay)


# 以下是题目页的破解与答题
def question_resource(courseid, workid):
    options = Options()
    options.add_argument("headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    s = Service('chromedriver.exe')
    chrome_answer = webdriver.Chrome(service=s, options=options)
    chrome_answer.get("https://mooc1.chaoxing.com/api/selectWorkQuestion?workId=%s&courseId=%s" % (workid, courseid))
    qsts = chrome_answer.find_elements(By.CLASS_NAME, 'TiMu')
    answers = []
    for qst in qsts:
        qst = qst.find_element(By.TAG_NAME, 'div')
        qst = qst.find_element(By.TAG_NAME, 'div')
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
    s = Service('chromedriver.exe')
    options = Options()
    options.add_argument("headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    chrome = webdriver.Chrome(service=s, desired_capabilities=desired_capabilities, options=options)
    chrome.get("https://cx.icodef.com/query.html?q=")
    wait = WebDriverWait(chrome, 100)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    chrome.execute_script('window.stop()')
    chrome.find_element(By.TAG_NAME, "input").send_keys(question_text)
    chrome.find_element(By.TAG_NAME, "input").send_keys(Keys.ENTER)
    answer = []
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "success")))
    for i in chrome.find_elements(By.CLASS_NAME, "success"):
        answer.append(i.text)
    print("答案为：", answer)
    return answer


def chapter_test():
    chrome.switch_to.frame(chrome.find_element(By.TAG_NAME, "iframe"))
    chrome.switch_to.frame(chrome.find_element(By.TAG_NAME, "iframe"))
    chrome.switch_to.frame(chrome.find_element(By.TAG_NAME, "iframe"))
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='ZyTop']//span")))
    if chrome.find_element(By.XPATH, "//div[@class='ZyTop']//span").text == "已完成":
        chrome.switch_to.parent_frame()
        chrome.switch_to.parent_frame()
        chrome.switch_to.parent_frame()
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='goback']/a")))
        chrome.find_element(By.XPATH, "//div[@class='goback']/a").click()
        print("该章节测试已提交，不用查题！")
        return
    workid = chrome.find_element(By.ID, "oldWorkId").get_attribute("value")
    courseid = chrome.find_element(By.ID, "courseId").get_attribute("value")
    print("作业id：%s\t课程id：%s" % (workid, courseid))
    answers = question_resource(courseid, workid)
    qsts = chrome.find_elements(By.CLASS_NAME, 'TiMu')
    count = 0
    for qst in qsts:
        qst = qst.find_elements(By.TAG_NAME, 'li')
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
    print("该章节题目已答完！冷却%.2f秒后提交！" % wait_time)
    chrome.find_element(By.CLASS_NAME, 'Btn_blue_1').click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='bluebtn ']")))
    sleep(wait_time)
    chrome.find_element(By.XPATH, "//a[@class='bluebtn ']").click()
    chrome.switch_to.parent_frame()
    chrome.switch_to.parent_frame()
    chrome.switch_to.parent_frame()


def video_play():
    global exitFlag
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    chrome.switch_to.frame(chrome.find_element(By.TAG_NAME, "iframe"))
    try:
        chrome.find_element(By.CLASS_NAME, "ans-job-finished")
    except:
        chrome.switch_to.frame(chrome.find_element(By.TAG_NAME, "iframe"))
        try:
            # 屏蔽弹窗题目
            wait_flow = WebDriverWait(chrome, 2)
            wait_flow.until(EC.presence_of_all_elements_located((By.ID, 'ext-comp-1041')))
            element = chrome.find_element(By.ID, 'ext-comp-1041')
            chrome.execute_script("""
                var element = arguments[0];
                element.parentNode.removeChild(element);
                """, element)
            wait_flow.until(EC.presence_of_all_elements_located((By.ID, 'ext-comp-1042')))
            element = chrome.find_element(By.ID, 'ext-comp-1042')
            chrome.execute_script("""
                var element = arguments[0];
                element.parentNode.removeChild(element);
                """, element)
            print("弹窗题目已屏蔽！")
        except:
            print("未发现有弹窗题目！")
            pass
        chrome.execute_script("window.focus();")
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[@class='vjs-big-play-button']")))
        chrome.find_element(By.XPATH, "//button[@class='vjs-big-play-button']").click()

        sleep(3)
        javascript_to_execute = "return document.getElementById('video_html5_api').duration"
        duration = chrome.execute_script(javascript_to_execute)
        javascript_to_execute = "return document.getElementById('video_html5_api').currentTime"
        current_time = chrome.execute_script(javascript_to_execute)
        # javascript_to_execute = "document.getElementById('video_html5_api').playbackRate=16"
        # chrome.execute_script(javascript_to_execute)
        # 获取当前北京时间
        now_time = datetime.now()
        print("[%s]:开始播放视频:总时长：%s秒,当前进度:%s秒,预计完成时间:%s" % (
            now_time.strftime("%Y-%m-%d %H:%M:%S"), duration, current_time,
            now_time + timedelta(seconds=duration - current_time)))

        exitFlag = False
        thread1 = myThread(1, "Thread-1", 15, duration)
        thread1.start()
        # 自动恢复播放
        while True:
            wait_video = WebDriverWait(chrome, 10000)
            wait_video.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "vjs-paused")))
            sleep(0.5)
            control_button = chrome.find_elements(By.CLASS_NAME, "vjs-paused")[1]
            if control_button.get_property("title") == "播放":
                print("播放被暂停，继续播放")
                control_button.click()
            elif control_button.get_attribute("title") == "重播":
                exitFlag = True
                break
        chrome.switch_to.parent_frame()
    chrome.switch_to.parent_frame()
    wait_time = random.randint(50, 100)
    wait_time = float(wait_time) / 10
    print("视频点已完成！冷却%.2f秒后进入章节测试！" % wait_time)
    exitFlag = True
    sleep(wait_time)


# 以下是视频播放及页面切换
LOGGER.setLevel(logging.CRITICAL)
options = Options()
options.add_argument('-ignore-certificate-errors')
options.add_argument('-ignore -ssl-errors')
# options.add_argument("headless") # 无头模式
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
s = Service('chromedriver.exe')
chrome = webdriver.Chrome(service=s, options=options)
chrome.get(url)
chrome.find_element(By.CLASS_NAME, "ipt-tel").send_keys(username)
chrome.find_element(By.CLASS_NAME, "ipt-pwd").send_keys(password)
chrome.find_element(By.ID, "loginBtn").click()
wait = WebDriverWait(chrome, 10)
wait.until(EC.title_is("学习进度页面"))
print("登陆成功！")
while (True):
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "orange")))
    task_point = chrome.find_element(By.CLASS_NAME, "orange")
    task_point.click()
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h1')))
    print("章节标题：", chrome.find_element(By.TAG_NAME, 'h1').text)

    # 完成章节测验单任务点
    if chrome.find_element(By.TAG_NAME, 'h1').text == "章节测验":
        print("页面状态：章节测验单任务点")
        chapter_test()
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='goback']/a")))
        chrome.find_element(By.XPATH, "//div[@class='goback']/a").click()
        continue

    # 完成tabtags多任务点
    try:
        tabtags = chrome.find_element(By.CLASS_NAME, "tabtags")
        tabs = tabtags.find_elements(By.TAG_NAME, "span")
        judge = 0
        for tab in tabs:
            if tab.text == tag_video:
                print("页面状态：tabtags多任务点")
                print("切换到视频播放标签")
                tab.click()
                video_play()
                judge = 1
            elif tab.text == tag_test:
                print("页面状态：tabtags多任务点")
                print("切换到章节测试标签")
                tab.click()
                chapter_test()
                judge = 1
        if judge == 1:
            wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='goback']/a")))
            chrome.find_element(By.XPATH, "//div[@class='goback']/a").click()
            continue
    except:
        pass
    # 完成视频单任务点
    print("页面状态：视频单任务点")
    video_play()
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='goback']/a")))
    chrome.find_element(By.XPATH, "//div[@class='goback']/a").click()
