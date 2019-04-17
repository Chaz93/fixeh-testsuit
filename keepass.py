#coding=utf-8
import time
import sys
import Logger
import getopt
import TestPrepare
import os

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction


desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '8.0'
desired_caps['deviceName'] = 'lgyhhh'
desired_caps['appPackage'] = 'com.android.keepass'
desired_caps['appActivity'] = '.KeePass'
desired_caps['noReset'] = True

test_app_package = None
test_dir = None


options, args = getopt.getopt(sys.argv[1:],'hp:b:',['help','package=','testdir='])
try:
    for name,value in options:
        if name in ('-h','--help'):
            pass
        if name in ('-p','--package'):
            test_app_package = value
        if name in ('-b','--testdir'):
            test_dir = value
except getopt.GetoptError:
    print('wrong get opt at test case')
    exit(30)

try:
    pre_conductor = TestPrepare.Preparer(err_log_file=os.path.join(test_dir,"err.out"),
                                        base_dir="/storage/emulated/0/keepass",
                                        initial_dir=test_dir)

    logger = Logger.Logger(output_dir=test_dir,app_package_name=test_app_package)
    logger.begin_log()
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    driver.implicitly_wait(5)



    #创建数据库
    driver.find_element_by_id("com.android.keepass:id/create").click()
    time.sleep(2)
    pid = logger.get_pid()
    #输入密码
    driver.find_element_by_id("com.android.keepass:id/pass_password").send_keys("123")
    time.sleep(2)
    #确认密码
    driver.find_element_by_id("com.android.keepass:id/pass_conf_password").send_keys("123")
    time.sleep(2)
    #点击确定
    driver.find_element_by_id("com.android.keepass:id/ok").click()
    time.sleep(2)
    #返回主页面
    driver.press_keycode(4)
    time.sleep(2)

    #打开刚刚创建的文件
    driver.find_element_by_id("com.android.keepass:id/open").click()
    time.sleep(2)
    #输入密码
    driver.find_element_by_id("com.android.keepass:id/password").send_keys("111")
    time.sleep(2)
    #点击确定
    driver.find_element_by_id("com.android.keepass:id/pass_ok").click()
    time.sleep(2)
    #密码错误，重新输入
    driver.find_element_by_id("com.android.keepass:id/password").clear();
    time.sleep(2)
    driver.find_element_by_id("com.android.keepass:id/password").send_keys("123")
    time.sleep(2)
    driver.find_element_by_id("com.android.keepass:id/pass_ok").click()
    time.sleep(2)
    #添加群组
    driver.find_element_by_id("com.android.keepass:id/add_group").click()
    time.sleep(2)
    driver.find_element_by_id("com.android.keepass:id/group_name").send_keys("hahaa")
    time.sleep(2)
    driver.find_element_by_id("com.android.keepass:id/ok").click()
    time.sleep(2)
    #返回主页面
    driver.press_keycode(4)
    time.sleep(2)
    driver.press_keycode(4)
    #删除记录
    el = driver.find_elements_by_class_name("android.widget.TextView")[5]
    TouchAction(driver).long_press(el).perform()
    time.sleep(1)
    driver.find_element_by_id("android:id/title").click()
    time.sleep(1)

    driver.quit()
finally:
    logger.generate_log_file(pid=pid)
    logger.close()

    pre_conductor.clear(test_files=['/storage/emulated/0/keepass/keepass.kdbx'])