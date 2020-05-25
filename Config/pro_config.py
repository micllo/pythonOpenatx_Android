from Env import env_config as cfg
from Project.pro_demo_1.test_case.demo_test import YybTest


def get_test_class_list(pro_name):
    """
    通过'项目名'获取'测试类'列表
    :param pro_name:
    :return:
    """
    if pro_name == "pro_demo_1":
        test_class_list = [YybTest]
    else:
        test_class_list = None
    return test_class_list


def pro_exist(pro_name):
    """
    判断项目名称是否存在
    :param pro_name:
    :return:
    """
    pro_name_list = ["pro_demo_1", "pro_demo_2"]
    if pro_name in pro_name_list:
        return True
    else:
        return False


def get_login_accout(current_thread_name_index):
    """
    通过线程名的索引 获取登录账号
    :param current_thread_name_index:
    :return:
    """
    if current_thread_name_index == 1:
        return "user_1", "passwd_1"
    elif current_thread_name_index == 2:
        return "user_2", "passwd_2"
    else:
        return "user_3", "passwd_3"


def get_app_info(pro_name):
    """
    通过项目名称 获取APP信息 （ appPackage、 appActivity ）
    :param pro_name:
    :return:
    """
    app_info = {}
    if pro_name == "pro_demo_1":  # 应用宝
        app_info["appPackage"] = 'com.tencent.android.qqdownloader'
        app_info["appActivity"] = 'com.tencent.pangu.link.SplashActivity'
    else:
        app_info["appPackage"] = None
        app_info["appActivity"] = None
    return app_info


def config_android_device_with_appium_server_list():
    """
    配置 Android 设备信息 以及 对应的 Appium 服务
    [ { "thread_index": 1, "device_name": "小米5S", "platform_version": "7.0", "device_udid": "192.168.31.136:5555", "appium_server": "http://127.0.0.1:4724/wd/hub" } } ,
      { "thread_index": 2, "device_name": "坚果Pro", "platform_version": "7.1.1", "device_udid": "192.168.31.253:4444", "appium_server": "http://127.0.0.1:4723/wd/hub" } } ]

      【 备 注 】
      1.一个Appium服务只能启动一个Android设备，若要使用多线程，则必须要将Android设备与Appium服务绑定起来
      2.<小米5S>已刷机，可以通过无线连接设备，所以使用docker中的appium服务
      3.<坚果Pro>未刷机，需要连接一次USB，所以使用mac中的appium服务
    :return:
    """
    android_device_info_list = []

    xiao_mi_5s = dict()
    xiao_mi_5s["thread_index"] = 1
    xiao_mi_5s["device_name"] = "小米5S"
    xiao_mi_5s["platform_version"] = "7.0"
    xiao_mi_5s["device_udid"] = "192.168.31.136:5555"
    xiao_mi_5s["appium_server"] = cfg.APPIUM_SERVER_DOCKER_4724
    android_device_info_list.append(xiao_mi_5s)

    smartisan_pro = dict()
    smartisan_pro["thread_index"] = 2
    smartisan_pro["device_name"] = "坚果Pro"
    smartisan_pro["platform_version"] = "7.1.1"
    smartisan_pro["device_udid"] = "192.168.31.253:4444"
    smartisan_pro["appium_server"] = cfg.APPIUM_SERVER_MAC_4723
    android_device_info_list.append(smartisan_pro)

    return android_device_info_list
