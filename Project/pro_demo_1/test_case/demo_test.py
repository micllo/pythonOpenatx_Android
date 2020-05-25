import time
from Common.com_func import log
from Project.pro_demo_1.page_object.search_page import SearchPage
from TestBase.test_case_unit import ParaCase
from TestBase.app_action import Base


class YybTest(ParaCase):

    """ 应 用 宝 用 例 集"""

    def test_search_hszz(self):
        """ 测试搜索'皇室战争'(通过)  """
        log.info("user(test_search_hszz): " + self.user)
        log.info("passwd(test_search_hszz): " + self.passwd)

        # 根据不同用例特定自定义设置（也可以不设置）
        # self.driver.implicitly_wait(5)

        # 通过Base类调用实例方法 ：self（测试用例实例对象）
        Base.screenshot(self, "home.png")

        search_page = SearchPage(self)
        search_page.search_hszz("皇室战争")
        # self.assertIn('test_search', "test_search", "test_search用例测试失败")

    def test_search_wx(self):
        """ 测试搜索'微信'(失败)  """
        log.info("user(test_search_wx): " + self.user)
        log.info("passwd(test_search_wx): " + self.passwd)

        search_page = SearchPage(self)
        search_page.search_wx("微信")

    def test_search_bd(self):
        """ 测试搜索'百度'(错误)  """
        log.info("user(test_search_bd): " + self.user)
        log.info("passwd(test_search_bd): " + self.passwd)

        search_page = SearchPage(self)
        search_page.search_bd("百度")

