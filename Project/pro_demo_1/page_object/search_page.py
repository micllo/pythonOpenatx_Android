# -*- coding:utf-8 -*-
from TestBase.app_action import Base
from selenium.webdriver.common.by import By
import time


class SearchPage(Base):

    """
        【 元 素 定 位 】
    """

    # 触摸点击'我知道了'按钮
    def touch_iknow_btn(self):
        self.touch_click(250, 1300)

    # 相关'允许'按钮
    def allowed_btn(self):
        return self.find_ele(By.ID, "android:id/button1")

    # 相关'X'按钮
    def close_btn(self):
        return self.find_ele(By.ID, "com.tencent.android.qqdownloader:id/b3f")

    # 搜索文本框1
    def search_field_1(self):
        return self.find_ele(By.ID, "com.tencent.android.qqdownloader:id/awt")
        # self.touch_click(150, 120)

    # 搜索文本框2
    def search_field_2(self):
        return self.find_ele(By.ID, "com.tencent.android.qqdownloader:id/yv")

    # 搜索按钮
    def search_btn(self):
        return self.find_ele(By.ID, "com.tencent.android.qqdownloader:id/a5t")

    # 获取"搜索内容"tab (通过text文本定位的第二个)
    def get_search_ele(self, content):
        search_ele_list = self.find_eles_by_text(content)
        self.log.info("hszz_ele_list -> " + str(search_ele_list))
        return search_ele_list[1]


    """
        【 页 面 功 能 】
    """

    def xiao_mi_5s_step(self):
        """
        小米5S 需要执行的步骤
        :return:
        """

        # 触摸点击'我知道了'按钮
        self.screenshot(image_name="iknow_btn.png")
        self.touch_iknow_btn()
        time.sleep(2)

        # 点击相关'允许'按钮
        self.screenshot(image_name="allowed_btn1.png")
        self.allowed_btn().click()
        time.sleep(2)
        self.screenshot(image_name="allowed_btn2.png")
        self.allowed_btn().click()
        time.sleep(5)

        # 点击相关'X'按钮
        self.screenshot(image_name="close_btn.png")
        self.close_btn().click()
        time.sleep(2)

    def smartisan_pro_step(self):
        """
        坚果pro 需要执行的步骤
        :return:
        """
        # 点击相关'X'按钮
        self.screenshot(image_name="close_btn.png")
        self.close_btn().click()
        time.sleep(2)

    def search_hszz(self, content):
        """
        搜索功能(皇室战争)
        :return:
        """

        if self.device_name == "小米5S":
            self.xiao_mi_5s_step()
        else:
            self.smartisan_pro_step()

        # 获取搜索文本框1，并点击
        self.screenshot(image_name="hszz_1_search_field.png")
        self.search_field_1().click()
        time.sleep(2)

        # 获取搜索文本框2，并输入内容
        search_field = self.search_field_2()
        search_field.send_keys(content)
        time.sleep(2)
        self.screenshot(image_name="hszz_2_search_field.png")

        # 获取搜索按钮，并点击
        self.search_btn().click()
        time.sleep(2)

        # 上滑
        self.swipe_up()
        time.sleep(2)

        # 下滑
        self.swipe_down()
        time.sleep(2)

        # 获取"皇室战争"tab，并点击
        hszz_tab = self.get_search_ele(content)
        self.log.info("hszz_tab.text : " + hszz_tab.text)
        self.log.info("hszz_tab.location : " + str(hszz_tab.location))  # {'x': 144, 'y': 90}
        self.log.info("text : " + hszz_tab.get_attribute("text"))
        self.log.info("bounds : " + str(hszz_tab.get_attribute("bounds")))  # str -> [144,90][780,198]
        hszz_tab.click()

        # 判断页面内容是否存在，同时截屏、然后断言
        self.assert_content_and_screenshot(image_name="hszz_2_target_page.png", content=content, error_msg="页面跳转失败！- 找不到'"+content+"'内容")

        # 回退上一页
        # self.back()
        # time.sleep(5)

    def search_wx(self, content):
        """
        搜索功能(微信)
        :return:
        """

        if self.device_name == "小米5S":
            self.xiao_mi_5s_step()
        else:
            self.smartisan_pro_step()

        # 获取搜索文本框1，并点击
        self.screenshot(image_name="wx_1_search_field.png")
        self.search_field_1().click()
        time.sleep(2)

        # 获取搜索文本框2，并输入内容
        search_field = self.search_field_2()
        search_field.send_keys(content)
        time.sleep(2)
        self.screenshot(image_name="wx_2_search_field.png")

        # 获取搜索按钮，并点击
        self.search_btn().click()
        time.sleep(2)

        # 上滑
        self.swipe_up()
        time.sleep(2)

        # 下滑
        self.swipe_down()
        time.sleep(2)

        # 获取"微信"tab，并点击
        wx_tab = self.get_search_ele(content)
        wx_tab.click()

        # 判断页面内容是否存在，同时截屏、然后断言
        self.assert_content_and_screenshot(image_name="wx_2_target_page.png", content="哈哈哈", error_msg="页面跳转失败！- 找不到'哈哈哈'内容")

    def search_bd(self, content):
        """
        搜索功能(百度)
        :return:
        """

        if self.device_name == "小米5S":
            self.xiao_mi_5s_step()
        else:
            self.smartisan_pro_step()

        # 获取搜索文本框1，并点击
        self.screenshot(image_name="bd_1_search_field.png")
        self.search_field_1().click()
        time.sleep(2)

        # 获取搜索文本框2，并输入内容
        search_field = self.search_field_2()
        search_field.send_keys(content)
        time.sleep(2)
        self.screenshot(image_name="bd_2_search_field.png")

        # 获取搜索按钮，并点击
        self.search_btn().click()
        time.sleep(2)

        # 上滑
        self.swipe_up()
        time.sleep(2)

        # 下滑
        self.swipe_down()
        time.sleep(2)

        # 获取"百度"tab，并点击
        wx_tab = self.get_search_ele("哈哈哈")
        wx_tab.click()

        # 判断页面内容是否存在，同时截屏、然后断言
        self.assert_content_and_screenshot(image_name="bd_2_target_page.png", content=content, error_msg="页面跳转失败！- 找不到'" + content + "'内容")

