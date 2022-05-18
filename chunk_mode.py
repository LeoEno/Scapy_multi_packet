#dataに入れた後にbodyに入っていないばあいのfind_chunk_sizeが動かない場合がある
#他人のコードを読む、コードのレビューを受ける


from scapy.all import *

class content:
    def __init__(self):
        self.response = ssck.recv().load

    def split_header_body(self):
        rn = self.response.find(b'\r\n\r\n')
        self.header = self.response[:rn]
        self.body = self.response[rn+4:]  

class chunk_mode():
    def __init__(self,body):
        self.buffer = body
        self.data = b''
        self.find_chunk_size()

    def find_chunk_size(self):
        tmp = self.buffer.find(b'\r\n')
        self.chunk_size = self.buffer[:tmp]

    def get(self):
        chunk_head = len(self.chunk_size) + len(b'\r\n')#chunk header + <CR><LF>
        while True:
            if len(self.buffer) < int(self.chunk_size,16):
                self.buffer += ssck.recv().load
            else:
                self.data += self.buffer[chunk_head : chunk_head + int(self.chunk_size,16)]#[:chunk header + <CR><LF> + chunk]
                self.buffer = self.buffer[chunk_head + int(self.chunk_size,16) + len(b'\r\n') - 1:]#[chunk header + <CR><LF> + chunk + <CR><LF> - 1:]
                if self.buffer == '':
                    self.buffer += ssck.recv().load
                self.find_chunk_size()
                if int(self.chunk_size,16) == 0:
                    break
                
class content_length():
    def __init__(self,header,body):
        self.header = header
        self.body = body
        self.find_content_length()

    def find_content_length(self):
        tmp = re.search(b'Content-Length: ([0-9]+)\\r',self.header)
        self.c_len = int(tmp.groups()[0])
    
    def get(self):
        while True:
            if len(self.body) < self.c_len: 
                self.body += ssck.recv().load
            else:
                break

def conect():
    global sck
    global ssck
    sck= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.connect(("localhost", 8080))
    ssck = StreamSocket(sck)
    ssck.send("GET /a.php HTTP/1.1\r\nHost: localhost\r\n\r\n".encode())

def close():
    ssck.close()
    sck.close()
    
def write(data):
    fp = open("./a.txt", mode='bw')
    fp.write(data)
    fp.close()

conect()
a = content()
a.split_header_body()

if b"Transfer-Encoding: chunked" in a.header:
    b = chunk_mode(a.body)
    b.get()
    write(b.data)
else:
    c = content_length(a.header,a.body)
    c.get()
    write(c.body)

close()