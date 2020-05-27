# -*- coding:utf-8 -*-
from TestBase.app_action import Base
import time


class SearchPage(Base):

    """
        【 元 素 定 位 】
    """

    # 搜索文本框1
    def search_field_1(self):
        return self.find_ele(resourceId="com.tencent.android.qqdownloader:id/awt")

    # 搜索文本框2
    def search_field_2(self):
        return self.find_ele(resourceId="com.tencent.android.qqdownloader:id/yv")
        # return self.find_ele(text="58同城", className="android.widget.EditText")

    # 搜索按钮
    def search_btn(self):
        # return self.find_ele(resourceId="com.tencent.android.qqdownloader:id/a5t")
        # return self.find_ele(text="搜索", className="android.widget.TextView")
        return self.find_ele(textContains="索", className="android.widget.TextView")  # 匹配text文本包含的内容
        # return self.find_ele(textStartsWith="搜", className="android.widget.TextView")  # 匹配text文本的开头

    # 获取"搜索内容"tab
    def get_search_ele(self, content):
        # return self.find_ele(textMatches=content, className="android.widget.TextView")
        return self.find_ele_by_child_text(text=content, class_name="android.widget.TextView",
                                           className="android.widget.LinearLayout",
                                           resourceId="com.tencent.android.qqdownloader:id/a78")

    """
        【 页 面 功 能 】
    """
    def search_hszz(self, content):
        """
        搜索功能(皇室战争)
        :return:
        """

        # 获取搜索文本框1，并点击
        # self.touch_click(150, 120)
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
        self.log.info("text : " + hszz_tab.get_text())
        self.log.info("bounds : " + str(hszz_tab.bounds()))  # str -> [144,90][780,198]
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
