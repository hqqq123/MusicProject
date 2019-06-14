"""
文件名: $NAME.py
日期: 22  
作者: lvah
联系: xc_guofan@qq.com
代码描述: 



"""

import socket
# 1. 创建一个socket对象;
# family指定使用IP协议的版本: IPV4:AF_INET;  ipv6: AF_INET6
# type指定传输层使用的协议类型:TCP(SOCKET.SOCK_STREAM), UDP(SOCK_DGRAM)
client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

# 2. 连接服务端(ip, port)
client.connect(('172.25.254.62', 4006))
while True:
    # 3. 给服务端回复消息, send(self, data: **bytes***, flags: int = ...) -> int: ...
    sendData = input('client:>> ')
    if not sendData:
        continue
    if sendData == 'quit':
        print("聊天结束.....")
        break

    client.send(sendData.encode('utf-8'))

    # 4. 接收服务端回复的消息
    recvData = client.recv(1024)
    print("客户端接收的消息:", recvData.decode('utf-8'))

# 7. 关闭客户端socket对象
client.close()