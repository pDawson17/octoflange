import pickle
import json
import time
import hashlib
import requests
"""
Packet types:
    1) Data Request 
    2) Data Response
    3) Blockchain update
    4) direct message Receiving/Sending
    5) friend request
    6) search
"""
class Packet_Creator:
    def __init__(self, ip, port):

        self.ip = ip
        self.port = port
        self.hobby = 42
        self.favorite_color = "beige"

    def handle_message(self, message):
        print(message, "message in michael")
        time.sleep(20)
        message_json = message
        if message_json["type"] == "Data Request":
            return self.data_request(message)
        elif message_json["type"] == "Data Response":
            return self.data_response(message)
        elif message_json["type"] == "Blockchain Update":
            return self.blockchain_update(message)
        elif message_json["type"] == "Direct Message":
            return self.direct_message(message)
        elif message_json["type"] == "Friend Request":
            return self.friend_request(message)
        else: #search
            return self.search(message)

    def data_request(self, message):
        try:
            data = requests.get("http://localhost:9876/get_data")
            print(data)
            response_packet = json.dumps({
                "type":"Data Response",
                "payload": data
                     })
        except:
            response_packet = json.dumps({"type":"Data Response", "payload": "fail"})
        return response_packet

    def data_response(self, message):
        #insert the data here
        print(message)
        message_data = message["payload"] #do something to get message_data
        try:
            requests.post("http://localhost:9876/insert_data", {
                "method":"POST",
                "headers": {"Content-Type":"application/json"},
                "body": json.dumps({
                    "data": message_data,
                    "signature":hashlib.sha1(message_data).hexdigest()
                    })
                    })
        except:
            return None
        return None


    def blockchain_update(self, message):
        print(message)
        blockchain_data = message["payload"]
        try:
            requests.post("http://localhost:9876/update_blockchain", {
                "method":"POST",
                "headers": {"Content-Type":"application/json"},
                "body": json.dumps({
                    "blockchain": blockchain_data["data"],
                    "comments":blockchain_data["comments"],
                    "signature":hashlib.sha1(message_data).hexdigest()
                    })
                })
        except:
            return None
        return None
       
    def create_blockchain_update_packet(self):
        try:
            bc = requests.get("http://localhost:9876/get_blockchain")
        except:
            bc = []
        packet = json.dumps({
            "type":"Blockchain Update",
            "payload":bc

            })
        return packet

    def direct_message(self, message):
        message_data = message["payload"]
        try:
            requests.post("http://localhost:9876/enqueue_message", {
                "method":"POST",
                "headers": {"Content-Type":"application/json"},
                "body": json.dumps({
                    "val": message_data,
                    "signature":hashlib.sha1(message_data).hexdigest()
                    })
                })
        except:
            return
        
    def friend_request(self, message):
        accept = True
        if accept:
            try:    
                requests.post("http://localhost:9876/add_node", {
                    "method":"POST",
                    "headers": {"Content-Type":"application/json"},
                    "body": json.dumps({
                        "node_tup":(message["payload"]["uname"], message["payload"]["ip"], message["payload"]["port"])})})
                return (message["payload"]["uname"], message["payload"]["ip"], message["payload"]["port"])
            except:
                return ("accpted", "failed")
        return (None, None)

    def create_friend_request(self, message):
        #else create friend request to ip
        packet = json.dumps({
            "type":"Friend Request",
            "payload":{"ip":message["payload"]["dest_ip"], "port":message["payload"]["dest_port"]}
                })
        return packet

        #def search(self, message)
