from Project.pro_demo_1.test_case.demo_test import YybTest

# 配置 项目名称列表
pro_name_list = ["pro_demo_1", "pro_demo_2"]


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


def get_app_package(pro_name):
    """
    通过项目名称 获取APP信息 （ appPackage ）
    :param pro_name:
    :return:

    """
    if pro_name == "pro_demo_1":  # 应用宝
        app_package = "com.tencent.android.qqdownloader"
    else:
        app_package = None
    return app_package


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


def config_android_device_list():
    """
    配置 Android 设备信息 列表
    [ { "device_name": "小米5S", "device_udid": "192.168.31.136:5555" } } ,
      { "device_name": "坚果Pro", "device_udid": "192.168.31.253:4444" } } ]
    :return:
    """
    android_device_info_list = []

    xiao_mi_5s = dict()
    xiao_mi_5s["device_name"] = "小米5S"
    xiao_mi_5s["device_udid"] = "192.168.31.136:5555"
    android_device_info_list.append(xiao_mi_5s)

    smartisan_pro = dict()
    smartisan_pro["device_name"] = "坚果Pro"
    smartisan_pro["device_udid"] = "192.168.31.253:4444"
    android_device_info_list.append(smartisan_pro)

    return android_device_info_list

