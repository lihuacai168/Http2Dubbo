# Http2Dubbo

## 1、介绍
封装Telnet命令，并使用django提供http转发dubbo接口

## 2、安装教程

1. 拉取代码放在Http2Dubbo这个文件夹 `git clone https://gitee.com/lihuacai/http2-dubbo.git Http2Dubbo`
2. 进入项目目录，并安装依赖`cd Http2Dubbo && pip3 install -r requirements.txt`
3. 把模型映射到数据库中，只需要执行一次，后续重启服务不需要再执行`python3 manage.py migrate --settings=Http2Dubbo.settings.dev`
4. 启动服务 `python3 manage.py runserver --settings=Http2Dubbo.settings.dev`
5. 访问服务`http://127.0.0.1:8000/swagger/`



## 3、启动和测试Dubbo服务
[参考这里](https://github.com/lihuacai168/dubbo-docker.git)


## 4、Http接口调用Dubbo服务
### 查询Dubbo服务
![输入图片说明](https://images.gitee.com/uploads/images/2020/1004/180827_00918537_136413.png "屏幕截图.png")
![输入图片说明](https://images.gitee.com/uploads/images/2020/1004/180913_74a49a14_136413.png "屏幕截图.png")

### 调用接口
![输入图片说明](https://images.gitee.com/uploads/images/2020/1004/181025_db8cdb17_136413.png "屏幕截图.png")
![输入图片说明](https://images.gitee.com/uploads/images/2020/1004/181049_969b8b2c_136413.png "屏幕截图.png")
