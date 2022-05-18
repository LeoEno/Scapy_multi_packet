from scapy.all import *

def recevie_decode(bool=False):
    response = ssck.recv()
    if bool:
        print(response.load.decode(errors = 'ignore'))
        return response.load
    else:
        print(response.load.decode(errors = 'ignore'))
        return response.load
        
def split_header_body(res):
    rn = res.find(b'\r\n\r\n')
    header = res[:rn]
    body = res[rn+4:]# +4;'\r\n\r\n'
    return header, body
    
def find_content_length(header):
    c_len = re.search(b'Content-Length: ([0-9]+)\\r',header)
    return int(c_len.groups()[0])
    

requests = ("GET / HTTP/1.1\r\nHost: ylb.jp\r\n\r\n",
            "GET /a.html HTTP/1.1\r\nHost: ylb.jp\r\n\r\n",
            "GET /aa.html HTTP/1.1\r\nHost: ylb.jp\r\n\r\n",
            "GET /aaa.html HTTP/1.1\r\nHost: ylb.jp\r\n\r\n")
            
sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.connect(("ylb.jp", 80))
ssck = StreamSocket(sck)

for value in requests:
    ssck.send(value.encode())
    response = recevie_decode()
    header, body = split_header_body(response)
    c_len = find_content_length(header)

    b_recv = len(body)
    while True:
        if b_recv == c_len:
            break
        else:
            data = len(recevie_decode(True))
            b_recv = data + b_recv
    
ssck.close()
sck.close()
