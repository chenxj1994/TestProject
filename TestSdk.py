import os
import unittest
import time

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, expected_conditions

from mobile_detect import get_serial_no


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUp(self):
        serial_no = get_serial_no()
        print('选择的设备序列号是:', serial_no)

        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = serial_no
        desired_caps['udid'] = serial_no
        desired_caps['appPackage'] = 'com.cmic.testerapp'
        desired_caps['appActivity'] = 'com.cmic.testerapp.MainActivity'
        desired_caps['noReset'] = 'true'
        desired_caps['unicodeKeyboard'] = True
        desired_caps['app'] = os.path.abspath('..') + '/app-release.apk'

        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver = driver

    def stop_msg(self):
        pass

    def test_01(self):
        try:
            location = ("xpath", "//*[@text='允许']")
            el = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_element_located(location))
            el.click()
        except:
            pass
        try:
            self.driver.find_element_by_xpath("//*[@text='是']").click()
        except:
            pass

        time.sleep(1)
        self.driver.find_element_by_android_uiautomator("text(\"导入短信\")").click()
        time.sleep(1)

        for i in range(2):
            loc = ("xpath", "//*[@text='允许']")
            try:
                e = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_element_located(loc))
                e.click()
            except:
                pass
        el = self.driver.find_element_by_id("com.cmic.testerapp:id/et_package_name")
        self.driver.set_value(el, "com.example.app.debug")
        time.sleep(1)
        self.driver.find_element_by_android_uiautomator("text(\"导入配置文件\")").click()
        # 获取不到Toast
        time.sleep(1)
        e_success = self.driver.find_element_by_xpath("//*[@text='导入配置文件成功']")
        self.driver.find_element_by_xpath("//*[@text='好的']").click()
        time.sleep(1)
        self.driver.start_activity("com.example.app", ".MainActivity")
        time.sleep(2)
        # 正式发版前要修改，因为集成到别的apk上面是直接跳到列表页的
        self.driver.find_element_by_id('com.example.app:id/btn_system_sms').click()
        self.driver.find_element_by_android_uiautomator("text(\"通知短信\")").click()
        ua_scroll = 'new UiScrollable(new UiSelector().className("android.support.v7.widget.RecyclerView")).scrollIntoView(new UiSelector().text("口碑网"))'
        self.driver.find_element_by_android_uiautomator(ua_scroll)
        time.sleep(1)
        self.driver.start_activity("com.cmic.testerapp", "com.cmic.testerapp.MainActivity")
        time.sleep(1)
        # el = self.driver.find_element_by_id("com.cmic.testerapp:id/et_package_name")
        # self.driver.set_value(el, "com.example.app.debug")
        # time.sleep(1)
        self.driver.find_element_by_android_uiautomator("text(\"测试结果\")").click()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
