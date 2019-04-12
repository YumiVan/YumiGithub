import socket
import threading
import sys
import framework
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s:%(message)s',
                    filename='log.txt',filemode='w')
class Fuwuqi():
    def __init__(self,dongsocket):
        bigsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#big_socker总端口
        bigsocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
        bigsocket.bind(('',dongsocket))
        bigsocket.listen(128)#监听
        self.bigsocket = bigsocket
    def go(self):
        while True:
            kefu_socket, ip_addr = self.bigsocket.accept()  # 创建客服套接字
            print('有人连接', ip_addr)
            threading1 = threading.Thread(target=self.work,args=(kefu_socket,))#创建线程
            threading1.setDaemon(True)
            threading1.start()
    @staticmethod
    def work(kefu_socket):                  #工作方法

        data = kefu_socket.recv(4096)
        if not data:
            print('客户端下线')
            kefu_socket.close()
            return
        print_data = data.decode('utf-8')
        print('收到请求',print_data)
        data_list = print_data.split(' ',maxsplit=2)
        send_addr = data_list[1]
        
        if send_addr == '/':
            send_addr = '/index.html'
        if send_addr.endswith('.html'):                   #动态资源请求=========================
            logging.info('有动态资源请求'+send_addr)
            env = {                                 #env  env  env env
                'request_path':send_addr
            }
            status,headers,response_body = framework.handle_request(env)#状态,响应头,响应体
            response_line = 'HTTP/1.1 %s\r\n'% status
            response_head = ''
            for head in headers:
                response_head += '%s: %s\r\n'% head

            send_data = (response_line + response_head+ '\r\n' + response_body).encode('utf-8')
            kefu_socket.send(send_data)#发送响应完成
            kefu_socket.close()

        else:                                                 #静态资源请求==============
            logging.info('有静态资源请求'+send_addr)
            try:
                with open('web' + send_addr , 'rb') as rb:
                    html_data = rb.read()#二进制html读取结果
            except Exception:
                send_line = 'HTTP/1.1 404 Not found\r\n'
                send_head = 'Server: YUMI/1.1\r\n'
                with open('web'+'/error.html','rb')as rb:
                    send_body = rb.read()
                send_data = (send_line + send_head + '\r\n').encode('utf-8') + send_body
            else:

                send_line = 'HTTP/1.1 200 OK\r\n'
                send_head = 'Server: YUMI/1.1\r\n'
                send_body = html_data
                send_data = (send_line + send_head + '\r\n').encode('utf-8') +send_body
            kefu_socket.send(send_data)#发送响应完成
            kefu_socket.close()                             #
def main():
    if len(sys.argv) != 2:
        print('不要乱搞')
        logging.warning('启动参数错误')
        return
    if not sys.argv[1].isdigit():#是不是数字
        logging.warning('启动参数错误')
        print('请输入数字端口')
        return

    dongsocket = int(sys.argv[1])
    super_socket = Fuwuqi(dongsocket)
    super_socket.go()
    
if __name__ == '__main__':
    main()

