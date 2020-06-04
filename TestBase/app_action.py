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
    【 获取'Android'驱动、设备名称 】
    :param pro_name
    :param current_thread_name_index: 当前线程名字的索引
    :param connected_android_device_list: 已连接设备信息列表
    [ { "thread_index": 1, "device_name": "小米5S",  "device_udid": "192.168.31.136:5555"} } ,
      { "thread_index": 2, "device_name": "坚果Pro", "device_udid": "192.168.31.253:4444" } } ]
    :return:

    【 步 骤 】
    1.通过'当前线程名索引' 获取已连接设备列表中对应的'Android'设备信息和'Appium'服务
    2.获取设备驱动
    """

    # 通过'当前线程名索引' 获取已连接设备列表中对应的'Android'设备信息
    device_name = None
    device_udid = None
    for connected_android_devices_dict in connected_android_device_list:
        if current_thread_name_index == connected_android_devices_dict["thread_index"]:
            device_udid = connected_android_devices_dict["device_udid"]
            device_name = connected_android_devices_dict["device_name"]
            break
    log.info("\n\n")
    log.info("device_name -> " + device_name)
    log.info("device_udid -> " + device_udid)
    log.info("\n\n")

    driver = None
    try:
        # 连接设备 ADB_WIFI
        driver = uiautomator2.connect_adb_wifi(device_udid)

        # 连接设备 WIFI
        # driver = uiautomator2.connect('192.168.31.136')
        # driver = uiautomator2.connect_wifi('192.168.31.136')

        # 连接设备 USB
        # driver = uiautomator2.connect('15a6c95a')
        # driver = uiautomator2.connect_usb('15a6c95a')

        # 配置accessibility服务的最大空闲时间，超时将自动释放
        driver.set_new_command_timeout(gv.NEW_COMMAND_TIMEOUT)

        # 设置 client 默认的元素定位超时时间 (注：在本框架中作用不大，见 find_ele 方法)
        # driver.implicitly_wait(gv.IMPLICITY_WAIT)

        # 解锁（点亮屏幕）相当于点击了home健
        driver.unlock()

    except Exception as e:
        log.error(("显示异常：" + str(e)))
        if "Uiautomator started failed" in str(e):
            error_msg = pro_name + " 项目 " + device_name + " 设备 启动 ATX 服务时 未授权"
        else:
            error_msg = pro_name + "项目 " + device_name + " 设备 启动 ATX 服务的其他异常情况"
        send_DD_for_FXC(title=pro_name, text="#### " + error_msg + "")
        raise Exception(error_msg)
    finally:
        return driver, device_name


class Base(object):

    def __init__(self, case_instance):
        self.case_instance = case_instance    # 测试用例的实例对象
        self.driver = case_instance.driver    # 操作 Android 设备
        self.session = case_instance.session  # 操作 APP 应用
        self.device_name = case_instance.device_name
        self.log = log

    def find_ele(self, **kwargs):
        ele = self.session(**kwargs)
        if ele.wait(timeout=gv.IMPLICITY_WAIT, exists=True):  # 设置 Session 定位等待时间
            return ele
        else:
            raise Exception("元素定位失败")

    def find_ele_by_child_text(self, text, class_name, **kwargs):
        """
        通过子元素的text查找
        :param text:
        :param class_name:
        :return:
        """
        ele = self.find_ele(**kwargs).child_by_text(text, className=class_name)
        if ele.wait(timeout=gv.IMPLICITY_WAIT, exists=True):  # 设置 Session 定位等待时间
            return ele
        else:
            raise Exception("text = \"" + text + "\" 的元素未找到")

    def click(self, *args):
        self.find_ele(*args).click()

    def click_exists(self, timeout, *args):
        """
        定位的元素若存在，则进行点击操作（设置等待时间）
        :param timeout: 等待元素超时时间
        :param args:
        :return:
        """
        self.find_ele(*args).click_exists(timeout)

    # 判断页面内容是否存在
    def content_is_exist(self, content, time_out):
        time_init = 1   # 初始化时间
        polling_interval = 1  # 轮询间隔时间
        while content not in self.session.dump_hierarchy():
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
        self.session.screenshot(current_test_path + image_name)
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
        while content not in self.session.dump_hierarchy():
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
        self.session.tap(x, y)

    # 获得机器屏幕大小x,y
    def get_size(self):
        x = self.session.window_size()[0]
        y = self.session.window_size()[1]
        # log.info(x, y)
        return x, y

    # 屏幕向上滑动（效果：屏幕往'下'翻动）
    def swipe_up(self):
        l = self.get_size()
        x = int(l[0] * 0.5)  # 固定 x 坐标
        y1 = int(l[1] * 0.75)  # 起始 y 坐标
        y2 = int(l[1] * 0.25)  # 终点 y 坐标
        self.session.swipe(x, y1, x, y2)

    # 屏幕向下滑动（效果：屏幕往'上'翻动）
    def swipe_down(self):
        l = self.get_size()
        x = int(l[0] * 0.5)  # 固定 x 坐标
        y1 = int(l[1] * 0.25)  # 起始 y 坐标
        y2 = int(l[1] * 0.75)  # 终点 y 坐标
        self.session.swipe(x, y1, x, y2)

    # 屏幕向左滑动（效果：屏幕往'右'翻动）
    def swip_left(self):
        l = self.get_size()
        y = int(l[1] * 0.5)  # 固定 y 坐标
        x1 = int(l[0] * 0.75)  # 起始 x 坐标
        x2 = int(l[0] * 0.05)  # 终点 x 坐标
        self.session.swipe(x1, y, x2, y)

    # 屏幕向右滑动（效果：屏幕往'左'翻动）
    def swip_right(self):
        l = self.get_size()
        y = int(l[1] * 0.5)  # 固定 y 坐标
        x1 = int(l[0] * 0.05)  # 起始 x 坐标
        x2 = int(l[0] * 0.75)  # 终点 x 坐标
        self.session.swipe(x1, y, x2, y)

    # 回退
    def to_back(self):
        self.session.press("back")

    # home健
    def to_home(self):
        self.session.press("home")


if __name__ == "__main__":
    print(project_path())

