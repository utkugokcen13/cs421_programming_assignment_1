

import socket
import base64
import time


def client_program():
    hostName = socket.gethostname()
    port = 8000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((hostName, port))  # connect to the server

    request = 'GET / HTTP/1.1\r\n'
    host = 'Host: ' + hostName + ':8000/ \r\n'

    client_socket.sendall(request.encode() + host.encode())


    req = client_socket.recv(1024).decode()
    print(req)

    # Writing the retrieved data to index2.html file
    f = open('index2.html', 'w')

    f.write(req)
    f.close()

    # The next entity is scraped from the index.html
    html_string = ".html"

    result = req.find(html_string)
    start_string = result

    for i in req[result:0:-1]:
        if i == "=":
            index = start_string
            break
        else:
            start_string = start_string - 1

    entity = '/' + req[start_string+2:result+5]


    new_request = 'GET ' + entity + ' HTTP/1.1\r\n'

    # Obtaining base64 encoding
    credentials = 'bilkentstu:cs421s2021'
    credentials_bytes = credentials.encode('ascii')
    credentials_encoded = base64.b64encode(credentials_bytes)
    base64_credentials = credentials_encoded.decode('ascii')

    authorization = 'Authorization: Basic '

    last = authorization + base64_credentials + "\r\n\r\n"




    client_socket.sendall(new_request.encode() + host.encode() + last.encode())

    req1 = client_socket.recv(1024).decode()
    print(req1)

    # Writing the retrieved data to protected2.html file
    f = open('protected2.html', 'w')

    f.write(req1)
    f.close()

    # Extracting the next entity
    href_string = "href="

    result1 = req1.find(href_string)

    next_entity = "/" + req1[result1+6:result1+13]


    last_request_for_txt = 'HEAD ' + next_entity + ' HTTP/1.1\r\n'
    last_request_for_html = 'HEAD /index.html HTTP/1.1\r\n'


    client_socket.sendall(last_request_for_txt.encode() + host.encode())

    req2 = client_socket.recv(1024).decode()
    print(req2)

    client_socket.sendall(last_request_for_html.encode() + host.encode())

    req3 = client_socket.recv(1024).decode()
    print(req3)



    get_request = "GET " + next_entity + " HTTP/1.1\r\n"

    # store starting time
    begin = time.time()

    # program body starts

    req13 = ""
    a = 15000
    range1 = 0
    for i in range (0,6488394,a):
        range1 = i + a
        if range1 > 6488394:
            range1 = 6488394
        range_request = "Range: bytes=" + str(i) + "-" + str(range1) + "\r\n\r\n"


        client_socket.sendall(get_request.encode() + host.encode() + range_request.encode())

        req13 = req13 + client_socket.recv(20000).decode()
    print(req13)


    # store end time
    end = time.time()
    print(f"Total runtime of the program is {end - begin} secs")

    f = open('big100.txt', 'w')

    f.write(req13)
    f.close()

    exit_request = "EXIT HTTP/1.1\r\n"
    client_socket.sendall(exit_request.encode() + host.encode())






if __name__ == '__main__':
    client_program()

