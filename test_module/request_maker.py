import requests
import json
#talks to sql_flask.py! like a good boy
class Request_Maker:
    def __init__(self, port=9876):
        self.signature = "test_app.py"
        self.port = port
    ##############
    #1) NODE OPERATORS
    ##############
    
    def get_nodes(self):
        """
        sends get request
        output: json.dumps data
        """
        try:
            data = requests.get("http://localhost:{port}/get_nodes".format(port=self.port))
        except:
            print("failed to get data in get node")
            return 1
        print(data, "test module data")
        return data

    def insert_node(self, node_tup):
        """
        outputs 0 if success, 1 if error
        node tup is: (signature, uname, port, ip)
        """
        print("in insert node in test module", node_tup)
        try: 
            re = requests.post("http://localhost:{port}/insert_data".format(port=self.port), {
                "method":"POST",
                "headers": {"Content-Type":"application/json"},
                "body":json.dumps({
                    "node_tup": node_tup
                    })
                })
        except:
            print("failed to get data, insert node")
            return 1
        return 0

    def search_node(self, node_tup):
        """
        outputs 0 if success 1 for fail 
        """
        print("in delete node in test module", node_tup)
        try:
            re = requests.post("http://localhost:{port}/insert_data".format(port=self.port), {
                "method":"POST",
                "headers": {"Content-Type":"application/json"},
                "body":json.dumps({
                    "node_tup": node_tup
                    })
                })
        except:
            print("failed to get data, search node")
            return 1
        return 0

   
    def delete_node(self, node_tup):
        """
        outputs 0 if success 1 for fail 
        """
        print("in delete node in test module", node_tup)
        try:
            re = requests.post("http://localhost:{port}/insert_data".format(port=self.port), {
                "method":"POST",
                "headers": {"Content-Type":"application/json"},
                "body":json.dumps({
                    "node_tup": node_tup
                    })
                }
            )
        except:
            print("fail in delete node getting ")
            return 1
        return 0 
##
#TODO:
## Update Node
## Search Node
    ##############
    #2) DATA OPERATORS
    ##############
    
    def get_data(self):
        """
        sends get request
        output: regular data
        """
        data = requests.get("http://localhost:{port}/get_data".format(port=self.port))
        print(data, "test module data")
        return data

    def insert_data(self, data, data_signature=0):
        """
        outputs 0 if success, 1 if error
        TODO: choose a standardized hash algorithm and method for data_signature
        """
        print("in insert node in test module", signature)
        try:
            re = requests.post("http://localhost:{port}/insert_data".format(port=self.port), {
                "method":"POST",
                "headers": {"Content-Type":"application/json"},
                "body":json.dumps({
                    "data":data,
                    "signature":signature
                    })
                })
        except:
            return 1
        return 0

    def update_likes(self, data_signature, personal_signature, like="True"):
        """
        like = like, other is dislike ig?
        TODO: choose a standardized hash algorithm and method for data_signature
        """
        print("in insert node in test module", signature)
        try:
            re = requests.post("http://localhost:{port}/insert_data".format(port=self.port), {
                "method":"POST",
                "headers": {"Content-Type":"application/json"},
                "body":json.dumps({
                    "data_signature":data_signature,
                    "personal_signature":personal_signature,
                    "like":like
                    })
                })
        except:
            return 1
        return 0


    def delete_data(self, data_signature):
        """
        outputs 0 if success 1 for fail 
        """
        print("in delete data in test module", node_tup)
        try:
            re = requests.post("http://localhost:{port}/insert_data".format(port=self.port), {
                "method":"POST",
                "headers": {"Content-Type":"application/json"},
                "body":json.dumps({
                    "data_sig": data_signature
                    })
                })
        except:
            return 1
        return 0 
##############
#3) Blockchain OPERATORS
##############    
    def get_blockchain(self):
        """
        sends get request
        output: json.dumps data
        """
        try:
            data = requests.get("http://localhost:{port}/get_blockchain".format(port=self.port))
        except:
            print("except in request to flask here in test moduel ")
            return 1

        print(data, "test module blockchain data")
        return data
    
    def mine_blockchain(self):
        """
        sends get request
        output: json.dumps data
        """
        try:
            data = requests.get("http://localhost:{port}/mine".format(port=self.port))
            print("worked")
        except:
            return 1

        return b'done'

    def update_blockchain(self, blockchain, comments):
        """
        outputs 0 if success, 1 if error
        TODO: choose a standardized hash algorithm and method for data_signature
        """
        try:
            re = requests.post("http://localhost:{port}/update_blockchain".format(port=self.port), {
                "method":"POST",
                "headers": {"Content-Type":"application/json"},
                "body":json.dumps({
                    "blockchain":blockchain,
                    "comments":comments
                    })
                })
        except:
            return 1
        return 0

    def add_comment(self, comment, signature, topic="general", uname="dev module"):
        """
        like = like, other is dislike ig?
        TODO: choose a standardized hash algorithm and method for data_signatur
        """
        try:
            re = requests.post("http://localhost:{port}/add_comment".format(port=self.port), {
                "method":"POST",
                "headers": {"Content-Type":"application/json"},
                "body":json.dumps({
                    "comment":comment,
                    "signature":signature,
                    "topic":topic,
                    "uname":uname
                    })
                })
            print("success")
        except Exception as e:
            return 1
        return 0


##
#TODO:
## Search Data
##
# 4) Message Queue Operators
##

    
    def pop_message(self):
        """
        sends get request
        output: data
        """
        try:
            data = requests.get("http://localhost:{port}/pop_message".format(port=self.port))
        except:
            return 1
        print(data, "test module message_queue data")
        return data
 
    def enqueue_message(self, message):
        """
        like = like, other is dislike ig?
        TODO: choose a standardized hash algorithm and method for data_signatur
        """
        print("in enqueuemessage in test module", message)
        try:
            re = requests.post("http://localhost:{port}/insert_data".format(port=self.port), {
                "method":"POST",
                "headers": {"Content-Type":"application/json"},
                "body":json.dumps({
                    "val":message
                    })
                })
        except:
            return 1
        return 0

       
##TODO: peek at top of queue

