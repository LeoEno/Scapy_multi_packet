from scapy.all import *

def recevie_write(bool=False):
    response = ssck.recv()
    if bool:
        fp.write(response.load.decode(errors = 'ignore'))
        return response.load
    else:
        #fp.write(response.load.decode(errors = 'ignore'))
        return response.load
        
def split_header_body(res):
    rn = res.find(b'\r\n\r\n')
    header = res[:rn]
    body = res[rn+4:]# +4;'\r\n\r\n'
    return header, body
    
def find_content_length(header):
    c_len = re.search(b'([0-9]+)\\r',header)
    return int(c_len.groups()[0])
    

requests = ("GET / HTTP/1.1\r\nHost: ylb.jp\r\n\r\n",
            "GET /a.html HTTP/1.1\r\nHost: ylb.jp\r\n\r\n",
            "GET /aa.html HTTP/1.1\r\nHost: ylb.jp\r\n\r\n",
            "GET /aaa.html HTTP/1.1\r\nHost: ylb.jp\r\n\r\n")

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.connect(("ylb.jp", 80))
ssck = StreamSocket(sck)

for index, value in enumerate(requests):
    ssck.send(value.encode())
    fp = open("./"+str(index)+".txt", mode='w')
    
    response = recevie_write()
    header, body = split_header_body(response)
    c_len = find_content_length(header)
    fp.write(body.decode(errors = 'ignore'))

    b_recv = len(body)
    while True:
        if b_recv == c_len:
            break
        else:
            data = len(recevie_write(True))
            b_recv = data + b_recv

    fp.close()
    
ssck.close()
sck.close()
