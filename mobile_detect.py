# coding:utf-8
import io
import locale
import os
import subprocess
import sys
from time import sleep


# get coding type
# print(locale.getdefaultlocale())  # ('zh_CN', 'cp936')

# set coding type
# locale.setlocale(locale.LC_ALL, locale='zh_CN.UTF-8')
# print(locale.getlocale())  # ('zh_CN', 'gb2312')
# print(locale.getdefaultlocale())
# print(locale.getpreferredencoding())


def str_sub(content, num):
    ct = content.replace('[', "").replace(']', '')
    return ct.split(':')[num].strip()


def input_brand(devices_info):
    # python3使用input取代raw_input
    brand = input(' \n -> Please input correct mobile brand to connect:')
    if brand in devices_info.keys():
        return devices_info[brand]
    else:
        return input_brand(devices_info)


def get_serial_no():
    """
    Objective:解决当多个手机连接电脑，Android adb shell命令使用问题.
    当只有一台手机时，自动连接。
    """
    # []代表list列表数据类型，列表是一种可变序列
    phone_brand = []
    serial_num = []

    # adb get-state 获取设备的连接状态
    # 多个设备时，控制台打印：error: more than one device/emulator， os.popen('adb get-state').read()返回空字符串
    f = os.popen('adb get-state')
    state = f.read().strip()
    f.close()
    print(state)
    if state != 'device':
        # 没有设备连接的时候，重启adb服务
        print('没有设备连接或者多个设备连接的时候，重启adb服务')
        os.popen('adb kill-server')
        os.popen('adb start-server')
        sleep(2)
    # 获取设备列表
    #  例如：
    #  List of devices attached
    #  90c4d6d2 device product:hero2qltezc model:SM_G9550 device:hero2qltechn transport_id:1
    #  10c4d6d2 device product:hero2qltezc model:SM_G9551 device:hero2qltechn transport_id:2
    f = os.popen('adb devices -l')
    device_list = f.read().strip()  # strip 去掉前后空格
    f.close()

    if 'model' not in device_list:
        print('-> Did not detect any devices.')
        sys.exit()
    else:
        # c = [ i for i in a if i%2==0 ]  //遍历a，在i为偶数时返回
        # split()当不带参数时以空格进行分割，当代参数时，以该参数进行分割。
        # 切割\n，去掉List一行，切割空格取出序列表
        serial_num = [sn.split()[0] for sn in device_list.split('\n') if sn and not sn.startswith('List')]
        for sn in serial_num:
            print("设备序列号：", sn)
            # 对齐格式化
            # print('{0},{1}'.format('zhangk', 32))
            # 获取Android系统属性 adb -s 序列号：指定特定设备进行操作
            # locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
            # print(locale.getdefaultlocale())
            # print(locale.getpreferredencoding())

            # popen = subprocess.Popen('adb -s {0} shell getprop'.format(sn), shell=False, stdin=subprocess.PIPE)
            # # print(popen.stdout)
            # stdout, stderr = popen.communicate()
            # print(stdout.decode('utf-8'))

            cmd = 'adb -s {0} shell getprop'.format(sn)

            f = os.popen(cmd)
            try:
                prop_list = f.read().split("\n")
                for mi in prop_list:
                    # for mi in f:
                    # 例如：
                    # [ro.build.display.id]: [R16NW.G9350ZCU2CRF5 Norma O8]
                    # [ro.build.fingerprint]: [samsung/hero2qltezc/hero2qltechn:8.0.0/R16NW/G9350ZCU2CRF5:user/release-keys]
                    # [ro.build.flavor]: [hero2qltezc-user]
                    # 系统指纹的属性
                    if 'ro.build.fingerprint' in mi:
                        # 取出指纹的属性值
                        model = str_sub(mi, 1).split('/')
                        # 手机品牌
                        phone_brand.append(model[0])
                f.close()
            except UnicodeDecodeError as e:
                f.close()
                # 包含中文os.popen解析是用gbk编码的，会出错
                proc = subprocess.Popen(cmd,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        bufsize=-1)
                pout = proc.stdout
                prop_list = pout.read().decode(encoding='utf-8').split("\n")
                proc.communicate()
                for mi in prop_list:
                    if 'ro.build.fingerprint' in mi:
                        # 取出指纹的属性值
                        model = str_sub(mi, 1).split('/')
                        # 手机品牌
                        phone_brand.append(model[0])
                pout.close()
                print(e)

    # 利用zip函数将两个列表(list)组成字典(dict)
    # keys = ['a', 'b', 'c'] values = [1, 2, 3] dictionary = dict(zip(keys, values)) 输出:{'a': 1, 'c': 3, 'b': 2}
    # print(phone_brand)
    # print(serial_num)
    # 这里输出“手机型号：序列号”字典
    devices_info = dict(zip(phone_brand, serial_num))

    if len(devices_info.keys()) > 1:
        print(devices_info)
        return input_brand(devices_info)
    elif len(devices_info.keys()) == 1:
        # python3 需要将字典的keys或values转成list才能取元素
        return list(devices_info.values())[0]


if __name__ == '__main__':
    # printDb()
    print('设备序列号：', get_serial_no())
