import socket
import threading
import json

BIND_IP = '0.0.0.0'
BIND_PORT = 8888

config_price_list='price.json'


def __get_product_name(data):
	request_message = json.loads(data)
	request_data = request_message['Request Message']
	return request_data['Product Name']

def __get_price(product_name):
    with open(config_price_list) as f:
       data = json.load(f)
       key = data[product_name]
       return key['price']

def __construct_reply_message(price):
	data = { "Reply Message" : { "Type" : "New Protocol", "Price" : price, "Status" : "ok" }}
	return json.dumps(data)

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print "[*] Received request for product: " + request
    product_name=__get_product_name(request)
    price = __get_price(product_name) 
    reply = __construct_reply_message(price)
    print reply
    client_socket.send(reply)
    print "[*] Current price of the product: " + reply
    client_socket.close()

def tcp_server():
    server = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    server.bind(( BIND_IP, BIND_PORT))
    server.listen(5)
    print"[*] Listening on %s:%d" % (BIND_IP, BIND_PORT)

    while 1:
        client, addr = server.accept()
        print "[*] Accepted connection from: %s:%d" %(addr[0], addr[1])
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == '__main__':
    tcp_server()
