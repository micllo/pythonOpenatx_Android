import uiautomator2
import time

# 获得机器屏幕大小x,y
def getSize(driver):
    x = driver.window_size()[0]
    y = driver.window_size()[1]
    print(x, y)
    return x, y


# 屏幕向上滑动（效果：屏幕往'下'翻动）< 左上角为坐标原点 >
def swipeUp(driver):
    l = getSize(driver)
    x = int(l[0] * 0.5)    # 固定 x 坐标
    y1 = int(l[1] * 0.75)  # 起始 y 坐标
    y2 = int(l[1] * 0.25)  # 终点 y 坐标
    driver.swipe(x, y1, x, y2)


# 屏幕向下滑动（效果：屏幕往'上'翻动）
def swipeDown(driver):
    l = getSize(driver)
    x = int(l[0] * 0.5)    # 固定 x 坐标
    y1 = int(l[1] * 0.25)  # 起始 y 坐标
    y2 = int(l[1] * 0.75)  # 终点 y 坐标
    driver.swipe(x, y1, x, y2)


# 屏幕向左滑动（效果：屏幕往'右'翻动）
def swipLeft(driver):
    l = getSize(driver)
    y = int(l[1] * 0.5)     # 固定 y 坐标
    x1 = int(l[0] * 0.75)   # 起始 x 坐标
    x2 = int(l[0] * 0.05)   # 终点 x 坐标
    driver.swipe(x1, y, x2, y)


# 屏幕向右滑动（效果：屏幕往'左'翻动）
def swipRight(driver):
    l = getSize(driver)
    y = int(l[1] * 0.5)    # 固定 y 坐标
    x1 = int(l[0] * 0.05)  # 起始 x 坐标
    x2 = int(l[0] * 0.75)  # 终点 x 坐标
    driver.swipe(x1, y, x2, y)


# 【 设 备 连 接 】

# 连接设备(小米 5S) ADB_WIFI
d = uiautomator2.connect_adb_wifi('192.168.31.136:5555')
# 连接设备(锤子 pro) ADB_WIFI
# d = uiautomator2.connect_adb_wifi('192.168.31.253:4444')


# 连接设备(小米 5S) WIFI
# d = uiautomator2.connect('192.168.31.136')
# d = uiautomator2.connect_wifi('192.168.31.136')

# 连接设备(锤子 旧) USB
# d = uiautomator2.connect('15a6c95a')
# d = uiautomator2.connect_usb('15a6c95a')

# 配置accessibility服务的最大空闲时间，超时将自动释放。默认3分钟(180)
d.set_new_command_timeout(300)  # 设置5分钟

# 全局默认的元素定位超时时间5秒
d.implicitly_wait(5.0)

# 解锁（点亮屏幕）相当于点击了home健
d.unlock()

# 应用宝 appPackage
appPackage = "com.tencent.android.qqdownloader"


# with d.session(appPackage) as sess:
#     # 获取当前APP的信息 {'package': '', 'activity': ''}
#     print(d.app_current())
#     print(sess.app_current())
#
#     # 获取搜索文本框1，并点击
#     # sess.tap(150, 120)
#     el = sess(resourceId="com.tencent.android.qqdownloader:id/awt")
#     print(el.info)
#     el.click()
#     time.sleep(2)
#
#     # 获取搜索文本框2，并输入内容
#     search_filed = sess(resourceId="com.tencent.android.qqdownloader:id/yv")
#     # search_filed = sess(text="58同城", className="android.widget.EditText")
#     search_filed.send_keys("皇室战争")
#     time.sleep(2)
#
#     # 获取搜索按钮，并点击
#     # sess(resourceId="com.tencent.android.qqdownloader:id/a5t").click_exists(3.0)
#     search_filed = sess(text="搜索", className="android.widget.TextView").click()  #
#     # search_filed = sess(textContains="索", className="android.widget.TextView").click()  # 匹配text文本包含的内容
#     # search_filed = sess(textStartsWith="搜", className="android.widget.TextView").click()  # 匹配text文本的开头
#     time.sleep(2)
#
#     # 上滑
#     swipeUp(sess)
#     time.sleep(2)
#
#     # 下滑
#     swipeDown(sess)
#     time.sleep(2)
#
#     # 获取"皇室战争"tab，并点击
#     sess(textMatches="皇室战争", className="android.widget.TextView").click_exists(3.0)
#
#     # sess(className="android.widget.LinearLayout", resourceId="com.tencent.android.qqdownloader:id/a78") \
#     #     .child_by_text("皇室战争", className="android.widget.TextView") \
#     #     .click()
#
#     time.sleep(2)

sess = d.session(appPackage)
# 获取当前APP的信息 {'package': '', 'activity': ''}
print(d.app_current())
print(sess.app_current())

# 获取当前页面内容
print(sess.dump_hierarchy())

# 获取搜索文本框1，并点击
# sess.tap(150, 120)
try:
    el = sess(resourceId="com.tencent.android.qqdownloader:id/awt")
    a = el.info
except Exception as e:
    print("异常 " + str(e))
    if "UiObjectNotFoundException" in str(e):
        print("元素定位失败")
print(el.info)
el.click()
time.sleep(2)


# 获取搜索文本框2，并输入内容
search_filed = sess(resourceId="com.tencent.android.qqdownloader:id/yv")
# search_filed = sess(text="58同城", className="android.widget.EditText")
search_filed.send_keys("皇室战争")
time.sleep(2)

# 获取搜索按钮，并点击
# sess(resourceId="com.tencent.android.qqdownloader:id/a5t").click_exists(3.0)
search_filed = sess(text="搜索", className="android.widget.TextView").click()
# search_filed = sess(textContains="索", className="android.widget.TextView").click()  # 匹配text文本包含的内容
# search_filed = sess(textStartsWith="搜", className="android.widget.TextView").click()  # 匹配text文本的开头
time.sleep(2)

# 上滑
swipeUp(sess)
time.sleep(2)

# 下滑
swipeDown(sess)
time.sleep(2)

# 获取"皇室战争"tab，并点击
hszz_tab = sess(textMatches="皇室战争", className="android.widget.TextView")
print("hszz_tab.text : " + hszz_tab.get_text())
print("bounds : " + str(hszz_tab.bounds()))  # str -> [144,90][780,198]
hszz_tab.click()

# try:
#     sess(className="android.widget.LinearLayout", resourceId="com.tencent.android.qqdownloader:id/a78") \
#         .child_by_text("皇室战争", className="android.widget.TextView") \
#         .click()
# except Exception as e:
#     print("异常 " + str(e))
#     if "UiObjectNotFoundException" in str(e):
#         print("元素定位失败")

time.sleep(2)

# sess.close()
d.app_stop(appPackage)
print("停止应用")

time.sleep(2)


###################################################################################

# # 【 全 局 配 置 】
#
# d.settings['xpath_debug'] = False  # 开启xpath插件的调试功能 （ 显示每个与ATX服务的HTTP请求的信息 ）
# d.debug = False
#
# d.settings['wait_timeout'] = 20.0  # 默认控件等待时间（原生操作，xpath插件的等待时间）
# d.implicitly_wait(10.0)
# print("wait timeout", d.implicitly_wait())
#
# # 配置accessibility服务的最大空闲时间，超时将自动释放。默认3分钟(180)
# d.set_new_command_timeout(300)  # 设置5分钟
#
# print("设备信息：" + str(d.info))
# print("屏幕分辨率：" + str(d.window_size()))
#
# # 解锁（点亮屏幕）相当于点击了home健
# d.unlock()
#
# # 应用宝 appPackage
# appPackage = "com.tencent.android.qqdownloader"
#
# # 获取当前APP的信息 {'package': '', 'activity': ''}
# print(d.app_current())
#
# # 获取当前 ip、设备连接地址
# print("wlan_ip：" + d.wlan_ip)
# print("serial：" + d.serial)
#
# # 设置粘贴板内容
# d.set_clipboard('text')
# print("粘贴板内容：" + d.clipboard)
#
# # 返回主页
# d.press("home")

###################################################################################

# 【 应 用 管 理 】

# # 启动应用 通过 appPackage
# d.app_start(appPackage)
#
# # 等待应用运行 ( front 前台运行)
# pid = d.app_wait(appPackage, front=True, timeout=20.0)
# if pid:
#     print(appPackage + " pid is %d" % pid)
# else:
#     print(appPackage + " is not runngin")
#
# # 获取应用信息
# app_info = d.app_info(appPackage)
# print("APP应用信息：" + str(app_info))
#
# time.sleep(2)
#
# # print("\n显示所有正在运行的APP列表\n")
# # app_list = d.app_list_running()
# # for app in app_list:
# #     print(app)
#
# # 保存 APP icon
# img = d.app_icon(appPackage)
# img.save("test_icon.png")
#
# # 截图
# print(d.screenshot("test_android.png"))
# print(d.screenshot().save("test_android.jpg"))
#
# # 检查并维持设备端守护进程处于运行状态
# d.healthcheck()
#
# # 执行 shell 命令
# output, exit_code = d.shell("pwd", timeout=60)
# print("output: " + output)
# print("exit_code: " + str(exit_code))
#
# # 停止应用
# d.app_stop(appPackage)
#
# # 停止所有正在运行的应用
# # d.app_stop_all()
# # 停止除'应用宝'以外的所有应用
# # d.app_stop_all(excludes=[appPackage])


###################################################################################


