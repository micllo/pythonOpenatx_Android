
【 用 例 编 写 注 意 事 项 】

1.在'Project'下创建'项目名称'目录：Project > pro_demo_1
2.在'项目名称'目录下创建两个目录：page_object、test_case
3.在'page_object'目录下提供：元素定位、页面操作方法
4.在'case_test'目录下提供：测试用例
5.在'Config > pro_config.py'文件中进行项目配置：
（1）get_test_class_list：         通过'项目名'获取'测试类'列表
（2）pro_exist：                   判断项目名称是否存在
（3）get_login_accout：            通过'线程名的索引' 获取登录账号
（4）get_app_info：                通过项目名称 获取APP信息 （ appPackage ）
（5）config_android_device_list：  配置 Android 设备信息列表


【 未 解 决 的 问 题 】
偶尔的问题：小米5S 若长时间未亮屏，第一次执行时，会有问题
暂时的方案：设置默认等待时间30秒


【 关于 本地 gulp 部 署 后 的 注 意 事 项 】
1.第一次 adb 连接 Android 设备 需要在设备上授权
2.第一次 安装 ATXserver 服务到设备 需要在设备上授权


########################################################################################################################


【 本 地 配 置 项 目 开 发 环 境 】

1.配置本地 venv 虚拟环境
（1）修改：requirements_init.txt
（2）执行：sh -x venv_install.sh

2.配置 gulpfile 依赖
（1）修改：gulpfile_install.sh
（2）删除：原有的 package.json 文件
（3）执行：sh -x gulpfile_install.sh

3.配置 Nginx -> python_openatx_android.conf

upstream api_server_Openatx_Android{
  server 127.0.0.1:5001 weight=1 max_fails=2 fail_timeout=30s;
  ip_hash;
}

server {
  listen 5010;
  server_name localhost;

  location /test_report_local/ {
        sendfile off;
        expires off;
        gzip on;
        gzip_min_length 1000;
        gzip_buffers 4 8k;
        gzip_types application/json application/javascript application/x-javascript text/css application/xml;
        add_header Cache-Control no-cache;
        add_header Cache-Control 'no-store';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header REMOTE-HOST $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        alias /Users/micllo/Documents/works/GitHub/pythonOpenatx_Android/Reports/;
       }

  location /api_local/ {
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header REMOTE-HOST $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504 http_404;
         proxy_pass http://api_server_Openatx_Android/;
         #proxy_pass http://127.0.0.1:5001/;
         proxy_redirect default;
  }
}

【 备 注 】
MAC本地安装的 nginx 相关路径
默认安装路径：/usr/local/Cellar/nginx/1.15.5/
默认配置文件路径：/usr/local/etc/nginx/
sudo nginx
sudo nginx -t
sudo nginx -s reload



########################################################################################################################


【 配 置 Openatx/uiautomator2 Android 环 境 】

1.安装工具
（1）安装 android-sdk 工具（提供adb命令连接真机或模拟器、提供uiautomatorviewer 定位元素）
（2）安装 uiautomator2 工具：pip3 install -U uiautomator2（提供openatx服务）

2.连接设备
（1）adb连真机：adb connect 192.168.31.136:5555 < 小米5S >
              adb connect 192.168.31.253:4444 < 坚果Pro >

（2）安装ATXserver服务到设备：python3 -m uiautomator2 init
    （ 在设备上安装的用于保持设备与电脑通信的服务 ）
    （ 注：第一次需要在真机上进行授权，可同时安装多个已连接的设备 ）


########################################################################################################################



【 本地 Mac 相关 】

1.uWSGI配置文件：./vassals/mac_app_uwsgi.ini
（1）启动 uWSGI 命令 在 ./start_uwsgi_local.sh 脚本
（2）停止 uWSGI 命令 在 ./stop_uwsgi.sh 脚本

2.上传 GitHub 需要被忽略的文件
（1）Logs、Reports -> 临时生产的 日志、报告
（2）vassals_local、venv -> 本地的 uWSGI配置、python3虚拟环境
（3）node_modules、gulpfile.js、package.json、package-lock.json -> 供本地启动使用的gulp工具

3.访问地址（ server.py 启动 ）：
（1）接口地址 -> http://127.0.0.1:5002/
               http://127.0.0.1:5002/API/index
               http://127.0.0.1:5002/API/get_project_case_list/<pro_name>

4.访问地址（ uwsgi 启动 ）：
（1）用例页面 -> http://localhost:5010/api_local/Android/index
（2）测试报告 -> http://127.0.0.1:5010/test_report_local/<pro_name>/[Android_report]<pro_name>.html
（3）接口地址 -> http://127.0.0.1:5010/api_local/
               http://127.0.0.1:5010/api_local/Android/sync_run_case
               http://127.0.0.1:5010/api_local/Android/get_img/5e5cac9188121299450740b3
   （ 备注：uwgsi 启动 5001 端口、nginx 配置 5010 反向代理 5001 ）

5.本地相关服务的启动操作（ gulpfile.js 文件 ）
（1）启动服务并调试页面：gulp "html debug"
（2）停止服务命令：gulp "stop env"
（3）部署docker服务：gulp "deploy docker"


【 虚拟环境添加依赖 】
1.创建虚拟环境：virtualenv -p /usr/local/bin/python3 venv （-p：指明python3所在目录）
2.切换到虚拟环境：source venv/bin/activate
3.退出虚拟环境：deactivate
4.添加依赖：
pip3 install -v flask==0.12 -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com


------------------------------------------

【 真 机 连 接 方 式 】

1.无线连接真机(使用一次USB)：
（1）通过USB将真机连接电脑
（2）让真机在5555端口监听TCP/IP连接：adb -s 设备ID tcpip 5555
（3）找到真机的ip地址：设置 -> 关于本机 -> 本机状态信息 -> IP地址
（4）通过ip地址连接真机：adb connect 192.168.31.56:5555
    （ 断开连接设备：adb disconnect 192.168.31.56:5555 ）

2.无线连接真机(无需USB)：
  前提：先将真机刷机获取root权限（ 通过win上使用'奇兔刷机'软件）
       在真机上安装超级终端模拟器（ Terminal_Emulator.apk ）：adb install Terminal_Emulator.apk
（1）使用真机在终端模拟器上输入下面两行
     su
     setprop service.adb.tcp.port 5555
     备注：有些设备（小米 5S）可能需要重启adbd服务：restart adbd（ 若无效 则：先 stop adbd  再 start adbd ）
（2）找到 设备的ip地址：设置 -> 关于本机 -> 本机状态信息 -> IP地址
（3）通过ip地址连接设备：adb connect 192.168.31.136:5555


########################################################################################################################


【 服 务 端 配 置 Openatx/uiautomator2 Android 环 境 】

[ 未 解 决 的 问 题 ]
'Docker'中无法获取通过'USB'连接的真机设备

[ 前 提 条 件 ]
1.生产环境为了减少意外情况，尽量使用无线连接真机
2.刷机成功的真机 可以直接在手机的超级终端上开启监听端口（ 直接无线连接 ）
3.不能刷机的真机 可以使用USB通过电脑为该手机开启监听端口 （ 使用一次USB后，可以无线连接 ）
（ 注：服务器 与 设备 要处于同一网络下 ）

[ 环 境 配 置 方 案 ]
1.在 linux | win10 | mac_mini 上启用一个Docker容器
2.Docker容器包含的工具或服务：Android-SDK工具、uiautomator2工具、监控服务
 ( 注：若 使用 linux 则要确保 linux 与 手机 处于同一网络 )


------------------------------------------


1.uWSGI配置文件：vassals_docker/app_uwsgi.ini
（1）启动 uWSGI 命令 在 ./start_uwsgi.sh 脚本
（2）停止 uWSGI 命令 在 ./stop_uwsgi.sh 脚本

2.服务器目录结构
  /var/log/uwsgi/ 		   -> pid_uwsgi.pid、app_uwsgi.log、emperor.log
  /var/log/nginx/ 		   -> error.log、access.log
  /etc/uwsgi/vassals/	   -> app_uwsgi.ini
  /opt/project/logs/ 	   -> 项目日志
  /opt/project/reports/	   -> 测试报告
  /opt/project/${pro_name} -> 项目
  /opt/project/tmp         -> 临时目录(部署时使用)

3.服务器部署命令：
（1）从GitGub上拉取代码至临时目录
（2）关闭nginx、mongo、uwsgi服务
（3）替换项目、uwsgi.ini配置文件
（4）替换env_config配置文件
（5）启动nginx、mongo、uwsgi服务
（6）清空临时文件

4.部署时的存放位置：
（1）./pythonSelenium -> /opt/project/pythonSelenium
（2）./pythonSelenium/vassals/app_uwsgi.ini -> /etc/uwsgi/vassals/app_uwsgi.ini

5.部署时相关配置文件的替换操作：
（1）将./Env/目录下的 env_config.py 删除
（2）将./Env/目录下的 env_config_docker.py 重命名为 env_config.py

6.访问地址（ Docker 内部 ）：
（1）测试报告 -> http://127.0.0.1:80/test_report/<pro_name>/[Android_report]<pro_name>.html
（2）接口地址 -> http://127.0.0.1:80/api/
               http://127.0.0.1:80/api/Android/sync_run_case
               http://127.0.0.1:80/api/Android/get_img/5e5cac9188121299450740b3
    ( 备注：uwgsi 启动 8081 端口、nginx 配置 80 反向代理 8081 )

7.访问地址（ 外部访问 ）：
（1）用例页面 -> http://192.168.31.10:1080/api/Android/index
（2）测试报告 -> http://192.168.31.10:1080/test_report/<pro_name>/[Android_report]<pro_name>.html
（3）接口地址 -> http://192.168.31.10:1080/api/
               http://192.168.31.10:1080/api/Android/sync_run_case
               http://192.168.31.10:1080/api/Android/get_img/5e5cac9188121299450740b3
    ( 备注：docker 配置 1080 映射 80 )

8.关于部署
    1.通过'fabric'工具进行部署 -> deploy.py
     （1）将本地代码拷贝入临时文件夹，并删除不需要的文件目录
     （2）将临时文件夹中的该项目压缩打包，上传至服务器的临时文件夹中
     （3）在服务器中进行部署操作：停止nginx、mongo、uwsgi服务 -> 替换项目、uwsgi.ini配置文件 -> 替换config配置文件 -> 启动nginx、mongo、uwsgi服务
     （4）删除本地的临时文件夹
      命令：gulp "deploy docker" -> 编译后 部署docker服务
    2.手动检测并确认
     （1）检查：Android 设备在Docker中是否正确连接 ： docker exec -it android_openatx_auto_test adb devices
     （2）若 第一次 安装 ATXserver 服务到设备，则需要在设备上进行授权操作


########################################################################################################################


【 框 架 工 具 】
 Python3 + Openatx/uiautomator2 + unittest + Flask + uWSGI + Nginx + Bootstrap + MongoDB + Docker + Fabric + Gulp


【 框 架 结 构 】（ 提高代码的：可读性、重用性、易扩展性 ）
 1.Api层：       对外接口、原静态文件
 2.Build层：     编译后的静态文件
 3.Common层：    通用方法、测试方法
 4.Config层：    错误码映射、全局变量、定时任务、项目配置、测试地址配置
 5.Env层：       环境配置
 6.Project层：   区分不同项目、page_object(页面操作方法、元素定位)、test_case(测试用例)
 7.TestBase层：  封装了浏览器驱动操作方法、提供'测试用例'父类第基础方法(继承’unittest.TestCase')、测试报告生成、同步执行用例方法
 8.Tools层：     工具函数
 9.其他：
 （1）vassals/ -> 服务器的'uWSGI配置'
 （2）vassals_local/、venv/ -> 本地的'uWSGI配置、python3虚拟环境'
 （3）Logs/、Reports/、Screenshot/ -> 临时生产的 日志、报告、截图
 （4）node_modules/、gulpfile.js、package.json、package-lock.json -> 供本地启动使用的gulp工具
 （5）deploy.py、start_uwsgi_local.sh、stop_uwsgi_local.sh、tmp_uwsgi_pid.txt -> 本地部署文件及相关命令和临时文件

【 功 能 点 】

1.使用 Python3 + Openatx/uiautomator2 + unittest + Bootstrap:
（1）使用'unittest'作为测试用例框架
（2）通过动态修改和添加'unittest.TestSuite'类中的方法和属性，实现启用多线程同时执行多条测试用例
（3）通过修改'HTMLTestRunner'文件并结合'unittest'测试框架，优化了测试报告的展示方式，并提供了每个测试用例的截图显示
（4）所有用例执行后，若有'失败'或'错误'的用例，则发送钉钉和邮件通知
（5）提供日志记录功能：按照日期区分
（6）提供定时任务：定时删除过期(一周前)的文件：日志、报告、截图文件(mongo数据)，定时执行测试用例
（7）提供页面展示项目用例，实现用例上下线、批量执行用例、显示报告、用例运行进度等功能
（8）多线程并发处理方式：先通过adb命令查看Android设备连接情况(已连接|未连接|未授权)、再将'已连接'的设备列表数量 作为 并发线程数量

2.使用 Flask ：
（1）提供 执行用例的接口
（2）提供 获取截图的接口：供测试报告页面调用

3.使用 Nginx ：
（1）提供测试报告的查看地址
（2）反向代理相关接口、解决测试报告调用'获取截图接口'时的跨域访问问题

4.使用 uWSGI :
（1）用作 web 服务器
（2）使用'emperor'命令进行管理：监视和批量启停 vassals 目录下 uwsgi 相关的 .ini 文件

5.使用 Docker：
（1）使用Dockerfile构建centos7镜像：提供项目所需的相关配置环境
（2）使用'docker-compose' 一键管理多个容器

6.使用 MongoDB ：
（1）使用'GridFS'进行图片文件的保存与读取

7.使用 Fabric ：
（1）配置相关脚本，实现一键部署

8.使用 NodeJS 的 Gulp 命令 ：
（1）配置本地启动的相关服务，实现一键启动或停止
（2）编译静态文件，防止浏览器缓存js问题
（3）实时监听本地调试页面功能

9.使用的工具和服务：Android-SDK 工具、uiautomator2 工具 ( ATX 服务 )
