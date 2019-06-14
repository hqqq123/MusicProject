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
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# 2. 绑定一个IP和端口， 供客户端来连接;
server.bind(('172.25.254.62', 4006))
# 3. 监听是否有客户端连接
server.listen(5)
print("服务端正在启动.........")
# 4. 接收客户端的连接, accept() -> (socket object, address info)
clientSocket, address = server.accept()
print("客户端的地址：", address)
while True:
    # 5. 接收客户端发送的消息
    recvData = clientSocket.recv(1024)
    print("服务端接收的消息:", recvData.decode('utf-8'))
    # 6. 给客户端回复消息, send(self, data: **bytes***, flags: int = ...) -> int: ...
    sendData = input('server:>> ')
    if not sendData:
        continue
    if sendData == 'quit':
        print("聊天结束.....")
        break

    clientSocket.send(sendData.encode('utf-8'))
# 7. 关闭服务端socket对象
server.close()
clientSocket.close()



# http:
# nginx: 10K---