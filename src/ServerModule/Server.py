from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from utils import mongotools

HTTP_REQUEST_TIMEOUT = 2  # seconds


class Server:

    def __init__(self, port: int, return_result: callable, transaction_pooling_period=2):
        self.timeouts = {}
        self.port = port
        self.return_result = return_result
        self.transaction_pooling_period = transaction_pooling_period

    def run(self):
        logging.basicConfig(level=logging.INFO)
        server_address = ('', self.port)
        httpd = HTTPServer(server_address, RequestHandler)
        logging.info('Starting httpd...\n')
        httpd.timeout = HTTP_REQUEST_TIMEOUT  # seconds

        while True:
            httpd.handle_request()


class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        logging.info(self.path)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info(post_data)

        post_data = str(post_data)[2:-1]
        parsed_post_data = post_data.split('&')
        info = {}
        for i in parsed_post_data:
            arg, val = i.split('=')
            info[arg] = val
        post_data = info
        
        if 'id' in post_data and 'from' in post_data and 'to' in post_data:
            if post_data['status'] == '1':
                post_data['status'] = True
            else:
                post_data['status'] = False
            update_transaction_details(post_data['id'], post_data['from'], post_data['to'], post_data['status'])

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        if self.path.endswith(".html") or self.path.endswith(".js"):
            filename = self.path
        elif len(self.path) <= 1:
            filename = "welcome.html"
        else:
            url = str(self.path)
            l = 0
            r = 0
            while(l+3 < len(url) and url[l:l+3] != 'id='):
                l += 1
            while(r+6 < len(url) and url[r:r+6] != '&link='):
                r += 1
            id_ = url[l+3:r]
            
            l = 0
            r = 0
            while(l+9 < len(url) and url[l:l+9] != 'ethereum:'):
                l += 1
            while(r < len(url) and url[r] != '@'):
                r += 1
            address = url[l+9:r]
            
            """logging.info(url)
            url_part = url.split('?')[1]
            url_part = url_part.split('&')
            id_ = url_part[0][3:]
            raw_address = url_part[1][15:]
            address = raw_address.split('@')[0]"""
            tx = mongotools.get_transaction(transaction_id=id_, user_address=address)
            filename = "index.html"
            
            if tx != None and tx['status'] == True:
                filename = "wrong_index.html"

        f = open('frontend/public/' + filename, 'rb')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(f.read())
        f.close()


def update_transaction_details(transaction_id, sender, receiver, status):
    '''
    :param transaction_id: unique id generated for this transaction
    :param sender: wallet address of sender
    :param receiver: wallet address of receiver
    :param amount: amount in wei
    '''
    db = mongotools.get_mongo_db().transactions
    logging.info("new request")
    logging.info({"_id": transaction_id, "sender": sender, "receiver": receiver, "status": status})
    #db.insert_one({"_id": transaction_id, "sender": sender, "receiver": receiver, "amount": amount, "status": True})
    mongotools.update_transaction_status(transaction_id=transaction_id, user_address=sender, new_status=status)


if __name__ == '__main__':
    s = Server(8000, logging.info)
    s.run()
