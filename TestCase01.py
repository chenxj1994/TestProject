import unittest
import time

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.connectiontype import ConnectionType


class MyTestCase(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '8.0.0'
        desired_caps['deviceName'] = '8DF6R16A10005912'
        # desired_caps['platformVersion'] = '6.0.1'
        # desired_caps['deviceName'] = 'M92QACQCQU3LV'
        desired_caps['appPackage'] = 'com.example.app.debug'
        desired_caps['appActivity'] = 'com.example.app.MainActivity'
        desired_caps['noReset'] = 'true'
        desired_caps['recreateChromeDriverSessions'] = True
        desired_caps['chromeOptions'] = {'androidProcess': 'com.tencent.mm:tools'}
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver = driver

    # 获得机器屏幕大小x,y
    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    def swipeUp(self, t):
        screen_size = self.getSize()
        x1 = int(screen_size[0] * 0.5)  # x坐标
        y1 = int(screen_size[1] * 0.75)  # 起始y坐标
        y2 = int(screen_size[1] * 0.25)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    # 屏幕向上滚动
    def swipeDown(self, t):
        screen_size = self.getSize()
        x1 = int(screen_size[0] * 0.5)  # x坐标
        y1 = int(screen_size[1] * 0.25)  # 起始y坐标
        y2 = int(screen_size[1] * 0.75)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    def _find_by_scroll(self,item_name):
        'new UIScrollable'
    # 网络设置
    def test_network(self):
        self.driver.set_network_connection(ConnectionType.DATA_ONLY)
        status = self.driver.network_connection

    def test_open(self):
        # a = self.driver.find_element_by_android_uiautomator("text(\"任何环境初始化模板\")")
        # a.click()
        # time.sleep(3)
        # b = self.driver.find_element_by_android_uiautomator("text(\"必须点击才能初始化\")")
        # b.click()
        # time.sleep(3)
        self.driver.find_element_by_id('com.example.app.debug:id/btn_example_sms').click()
        # 通过父节点找子节点
        sonXpath = '//*[@resource-id="com.example.app.debug:id/rv_sms"]/android.widget.RelativeLayout[1]'
        self.driver.find_element_by_xpath(sonXpath).click()
        time.sleep(3)
        # 通过子节点找父节点
        fatherXpath = '//*[@resource-id="com.example.app.debug:id/tv_mp_menu_item" and @text = "进入邮箱"]/..'
        self.driver.find_element_by_xpath(fatherXpath).click()
        time.sleep(8)
        # 截图
        # self.driver.get_screenshot_as_file("C:\\pyProjects\\TestProject\\screenShot\\我的.png")
        # WebDriverWait(self.driver, 8).until(lambda x:x.find_element_by_class_name('com.tencent.tbs.core.webkit.WebView'))
        print(self.driver.contexts)
        time.sleep(5)
        # 版本号57.0.2987.132
        # 换台手机试试
        self.driver._switch_to.context('WEBVIEW_com.example.app.debug')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
