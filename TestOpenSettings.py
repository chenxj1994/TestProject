import unittest
from appium import webdriver
import time

class MyTestCase(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '8.0.0'
        desired_caps['deviceName'] = '8DF6R16A10005912'
        desired_caps['appPackage'] = 'com.android.settings'
        desired_caps['appActivity'] = '.HWSettings'
        desired_caps['noReset'] = 'true'
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver = driver

    # 获得机器屏幕大小x,y
    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    # 屏幕向下滚动
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

    # 屏幕滑动到底部
    def swipeToButtom(self):
        list1 = self.driver.find_elements_by_xpath('//*[@resource-id="com.android.settings:id/dashboard_container"]/android.widget.LinearLayout')
        list1[len(list1)-1]

    def test_openAboutPhone(self):
        i = 0
        while (i < 10):
            try:
                self.driver.find_element_by_xpath("//*[@text='系统']/../..").click()
                time.sleep(3)
                self.driver.find_element_by_xpath("//*[@text='关于手机']").click()
                break
            except Exception as e:
                self.swipeUp(1000)
                i = i + 1

        # self.driver.find_element_by_xpath("//*[@text='关于手机']").click()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
