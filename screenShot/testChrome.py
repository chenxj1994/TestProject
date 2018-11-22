import unittest
from appium import webdriver

class MyTestCase(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0.1'
        desired_caps['deviceName'] = 'M92QACQCQU3LV'
        desired_caps['appPackage'] = 'com.tencent.mm'
        desired_caps['appActivity'] = '.ui.LauncherUI'
        desired_caps['noReset'] = 'true'
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver = driver

    def test_something(self):
        print(self.driver.contexts)


if __name__ == '__main__':
    unittest.main()
