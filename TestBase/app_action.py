# -*- coding:utf-8 -*-
from Common.com_func import project_path, log, mkdir
from Env import env_config as cfg
from Config import global_var as gv
import time
from Tools.mongodb import MongoGridFS
from Common.test_func import send_DD_for_FXC
import uiautomator2


def get_android_driver(pro_name, current_thread_name_index, connected_android_device_list):
    """
    【 获取 Android 设备驱动 】
    :param pro_name
    :param current_thread_name_index: 当前线程名字的索引
    :param connected_android_device_list: 已连接设备信息列表
    [ { "thread_index": 1, "device_name": "小米5S", "platform_version": "7.0", "device_udid": "192.168.31.136:5555", "appium_server": "http://127.0.0.1:4724/wd/hub" } } ,
      { "thread_index": 2, "device_name": "坚果Pro", "platform_version": "7.1.1", "device_udid": "192.168.31.253:4444", "appium_server": "http://127.0.0.1:4723/wd/hub" } } ]
    :return:

    【 步 骤 】
    1.获取 Appium 服务启动应用所需的能力参数 (指定设备，指定应用)
    2.通过'当前线程名索引' 获取已连接设备列表中对应的'Android'设备信息和'Appium'服务
    3.获取设备驱动
    """

    # 通过'当前线程名索引' 获取已连接设备列表中对应的'Android'设备信息和'Appium'服务
    device_name = None
    for connected_android_devices_dict in connected_android_device_list:
        if current_thread_name_index == connected_android_devices_dict["thread_index"]:
            desired_caps["platformVersion"] = connected_android_devices_dict["platform_version"]
            desired_caps["deviceName"] = connected_android_devices_dict["device_udid"]
            device_name = connected_android_devices_dict["device_name"]
            appium_server = connected_android_devices_dict["appium_server"]
            break
    log.info("\n\n")
    log.info("device_name -> " + device_name)
    log.info("\n\n")

    try:
        # 连接设备 ADB_WIFI
        driver = uiautomator2.connect_adb_wifi('192.168.31.136:5555')

        # 连接设备 WIFI
        # driver = uiautomator2.connect('192.168.31.136')
        # driver = uiautomator2.connect_wifi('192.168.31.136')

        # 连接设备 USB
        # driver = uiautomator2.connect('15a6c95a')
        # driver = uiautomator2.connect_usb('15a6c95a')

        # 配置accessibility服务的最大空闲时间，超时将自动释放
        driver.set_new_command_timeout(gv.NEW_COMMAND_TIMEOUT)

        # 全局默认的元素定位超时时间
        driver.implicitly_wait(gv.IMPLICITY_WAIT)

        # 解锁（点亮屏幕）相当于点击了home健
        driver.unlock()
    except Exception as e:
        log.error(("显示异常：" + str(e)))
        error_msg = "启动 ATX 服务的其他异常情况"
        send_DD_for_FXC(title=pro_name, text="#### " + error_msg + "")
        raise Exception(error_msg)

    return driver, device_name


class Base(object):

    def __init__(self, case_instance):
        self.case_instance = case_instance  # 测试用例的实例对象
        self.driver = case_instance.driver
        self.device_name = case_instance.device_name
        self.log = log

    def find_ele(self, *args):
        try:
            self.log.info("通过" + args[0] + "定位，元素是 " + args[1])
            return self.driver.find_element(*args)
        except Exception:
            raise Exception(args[1] + " 元素定位失败！")

    def find_ele_by_text(self, content):
        """
        通过text找到元素（唯一）
        :param content:
        :return:
        """
        try:
            return self.driver.find_element_by_android_uiautomator('new UiSelector().text("' + content + '")')
        except Exception:
            raise Exception("text = \"" + content + "\" 的元素未找到")

    def find_eles_by_text(self, content):
        """
        通过text找到元素（多个）
        :param content:
        :return:
        """
        try:
            return self.driver.find_elements_by_android_uiautomator('new UiSelector().text("' + content + '")')
        except Exception:
            raise Exception("text = \"" + content + "\" 的元素未找到")

    def click(self, *args):
        self.find_ele(*args).click()

    def send_key(self, *args, value):
        self.find_ele(*args).send_keys(value)

    def js(self, str):
        self.driver.execute_script(str)

    def url(self):
        return self.driver.current_url

    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def quit(self):
        self.driver.quit()

    # 判断页面内容是否存在
    def content_is_exist(self, content, time_out):
        time_init = 1   # 初始化时间
        polling_interval = 1  # 轮询间隔时间
        while content not in self.driver.page_source:
            time.sleep(polling_interval)
            time_init = time_init + 1
            if time_init >= time_out:
                return False
        return True

    def screenshot(self, image_name):
        """
         截 图、保 存 mongo、记录图片ID
        :param image_name: 图片名称

        【 使 用 case_instance 逻 辑 】
        1.若'Base类的子类实例对象'调用该方法（在 object_page 中使用）：则使用该实例对象本身的 self.case_instance 属性（测试用例实例对象）
        2.若'Base类'调用该方法（在 test_case 中使用）：则使用该 self 测试用例实例对象本身
        3.由于'Base'类和'测试用例类'都含有'driver'属性，所以不影响self.driver的使用
        :return:
        """
        # 判断当前的'实例对象'是否是'Base'类型（考虑子类的继承关系）
        case_instance = isinstance(self, Base) and self.case_instance or self
        # 获取当前测试用例的路径 -> ../类名/方法名/
        current_test_path = cfg.SCREENSHOTS_DIR + case_instance.pro_name + "/" + case_instance.class_method_path
        mkdir(current_test_path)
        self.driver.get_screenshot_as_file(current_test_path + image_name)
        mgf = MongoGridFS()
        files_id = mgf.upload_file(img_file_full=current_test_path + image_name)
        case_instance.screen_shot_id_list.append(files_id)

    def assert_content_and_screenshot(self, image_name, content, error_msg):
        """
        断言内容是否存在、同时截屏
        :param image_name: 图片名称
        :param content: 需要轮询的内容
        :param error_msg: 断言失败后的 错误提示
        :return:
        """
        is_exist = True
        time_init = 1   # 初始化时间
        polling_interval = 1  # 轮询间隔时间
        while content not in self.driver.page_source:
            time.sleep(polling_interval)
            time_init = time_init + 1
            if time_init >= gv.POLLING_CONTENT_TIME_OUT:
                is_exist = False
                break
        self.screenshot(image_name)
        self.case_instance.assertTrue(is_exist, error_msg)

    def touch_click(self, x, y):
        """
        触摸点击
        :param x: 横坐标（从左上角开始）
        :param y: 从坐标（从左上角开始）
        :return:
        """
        self.driver.tap([(x, y)])

    # 获得机器屏幕大小x,y
    def get_size(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        # log.info(x, y)
        return x, y

    # 屏幕向上滑动（效果：屏幕往'下'翻动）
    def swipe_up(self, t=1000):
        l = self.get_size()
        x = int(l[0] * 0.5)  # 固定 x 坐标
        y1 = int(l[1] * 0.75)  # 起始 y 坐标
        y2 = int(l[1] * 0.25)  # 终点 y 坐标
        self.driver.swipe(x, y1, x, y2, t)

    # 屏幕向下滑动（效果：屏幕往'上'翻动）
    def swipe_down(self, t=1000):
        l = self.get_size()
        x = int(l[0] * 0.5)  # 固定 x 坐标
        y1 = int(l[1] * 0.25)  # 起始 y 坐标
        y2 = int(l[1] * 0.75)  # 终点 y 坐标
        self.driver.swipe(x, y1, x, y2, t)

    # 屏幕向左滑动（效果：屏幕往'右'翻动）
    def swip_left(self, t=1000):
        l = self.get_size()
        y = int(l[1] * 0.5)  # 固定 y 坐标
        x1 = int(l[0] * 0.75)  # 起始 x 坐标
        x2 = int(l[0] * 0.05)  # 终点 x 坐标
        self.driver.swipe(x1, y, x2, y, t)

    # 屏幕向右滑动（效果：屏幕往'左'翻动）
    def swip_right(self, t=1000):
        l = self.get_size()
        y = int(l[1] * 0.5)  # 固定 y 坐标
        x1 = int(l[0] * 0.05)  # 起始 x 坐标
        x2 = int(l[0] * 0.75)  # 终点 x 坐标
        self.driver.swipe(x1, y, x2, y, t)


if __name__ == "__main__":
    print(project_path())

