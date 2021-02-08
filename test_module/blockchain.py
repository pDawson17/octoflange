#CODE
#UDEMY TUTORIAL
### TODO:
# write traversal function to compute money
# using user hash, create function to chec user balance
# write in support for mass transactions
# write in storage for temporariry comment sections, comment sorting etc
#integrate comments

import datetime
import hashlib
import json
import requests
from uuid import uuid4
from urllib.parse import urlparse
import pickle
import time
import random

class Blockchain:

    def __init__(self, chain=None):
        if chain:
            p = pickle.loads(chain)
            if p != None: 
                self.chain = p
            else:
                self.chain =[]
        else:
            self.chain = [] 
        self.transactions = [] #list of obj: {"sender":sender_id, rate: recepients, rate:recip....}
        self.comments = {} #-> hash(signature+comment):{uname, signature, comment, timestamp, category, likes={}}, dislikes
        if len(self.chain) == 0:
           self.genesis = self.create_block(proof = 1, prev_hash = 0, signature='0') #create genesis block
        else:
            self.genesis = self.chain[0]
        self.chain_collection = []

    def collect_chain(self, chain, comments):
        self.chain_collection.append(chain)
        for i in comments.keys():
#comment sig topic uname
            self.add_comment(comments[i]["comment"], comments[i]["signature"], comments[i]["topic"], comments[i]["uname"])
        if len(self.chain_collection) > 5:
            self.consensus()
            self.chain_collection = []
            return self.chain
        #TODO: Merge likes
        return None

    def export_chain(self):
        #to read: pickle.loads(x)
        return pickle.dumps(self.chain), self.comments
    
    def import_chain(self, chain):
        #imports pickled chain
        self.chain = pickle.loads(chain)

    def create_block(self, proof, prev_hash, signature): #make transactions an arg
        block = {
        'index' : len(self.chain)+1,
        'timestamp' : time.time(),
        'proof' : proof, #proof is ur id as checked on comments above
        'prev_hash' : prev_hash,
        'transactions' : self.transactions,
        'comments' : self.comments #add all comments for now 
        }
        self.transactions = [] #empty transactions after block mined
        self.comments = {} #empty comments after mined
        self.chain.append(block)
        return block

    def replace_chain(self): #replaceChain works chain by chain
        #FIRST: request chains, have them here
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        network_responses = [] #SERVER FUNC RESPONJSE
        for node in network:
            #response = requests.get(f"http://{node}/get_chain")
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length: #and self.is_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

    def get_prev_hash(self):
        return self.hash(self.chain[-1])

    def get_prev_block(self):
        #returns last block of chain
        return self.chain[-1]

    def add_transaction(self, transaction):
 
        self.transactions.append(transaction)
        prev_block = self.get_prev_block()
        return prev_block['index']+1

    def add_comment(self, comment, signature, topic, uname):
        #later change to be list of objects, signature: object and do replacement decision
        comment_signature = hashlib.sha256((signature+comment).encode('utf-8')).hexdigest()
        if comment_signature not in self.comments:
            self.comments[comment_signature] = {"comment":comment, "likes":{}, "dislikes":{}, "uname":uname, "timestamp":time.time(), "topic":topic, "signature":signature}
        #else compare them & their likes& update
        else:
            r = self.update_likes(comment, signature,{}, "", "") #empty dict for likes
        print("added comment, ", comment, " comments r now : ", self.comments)
    
    def update_likes(self, comment, signature, likes_list, personal_sig, amt):
    
        comment_signature = hashlib.sha256((signature+comment).encode('utf-8')).hexdigest()
        if comment_signature not in self.comments:
            return 1
        #likes list should be dict of ur_sig: amt
        for i in likes_list:
            if i not in self.comments[comment_signature]["likes"]:
                self.comments[i] = likes_list[i]
        return 0

    def replace_comments(self, comments_list):
        self.comments = comments_list

    def hash(self, block):
        encoded_block =pickle.dumps(block)
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        prev_block = chain[0]
        index = 1
        while index < len(chain):
            block = chain[index]
            if block['prev_hash'] != self.hash(prev_block):
                return False #chain is invalid

            prev_proof = prev_block['comments'][0]['allowed_index']
            proof = block['proof']
            #hash_operation = hashlib.sha256(str(proof**2-prev_proof**2).encode()).hexdigest()
            #if user != '0000':
            #    return False
            if prev_block != proof:
                return False
            prev_block = block
            index+=1
        return True
    
    def compute_transactions(self):
        #publishes transactions based on role
        #so for this i think i'll so %profit splits 
        #algorithm:
        #1) Block Miner gets revenue off the top
        #2) Comment gets alloted portion of revenue based on % of likes it has. then commenter takes flat % + and rest goes to likers
        #3) Likers get a portion of their liked comments' share - based on how much they bet
        return self.get_top_comments(), "we arent doing that rn "

    def compute_transactions_draft_1(self): 
        transactions = {} #signature: {}
        total_revenue = 0 #{] looks cool
        top_commenter = {} #commenter sig, total likes for his block
        top_comments = self.get_top_comments()
        comment_fee = 2
        miner_fee = .1
        num_comments = 5
        commenter_fee = .05
        for i in self.comments:
            if i not in top_comments:
                #this is revenue
                #self.comments[i]["signature"] 
                for j in self.comments[i]["likes"]:
                    if j not in self.transactions:
                        transactions[j] = -1*self.comments[i]["likes"][j] #should return amt liked
                    else:
                        transactions[j] -= self.comments[i]["likes"][j] #should return amt liked
                transactions[self.comments[i]["signature"]] -= comment_fee
            else:
                count = 0
                for j in self.comments[i]["likes"]:
                    #transactions[j] += self.comments[i]["likes"][j] #should return amt liked
                    count += self.comments[i]["likes"][j]
                print("SELF> COMMENTS SLEEP \n", self.comments)
                top_commenter[self.comments[i]["signature"]] = count
                #TODO: fix to compute for user who comments several times
        #now iterate thru top comments& assign payouts
        for k in top_comments.items():
            divisible_amt = (top_commenter[k["signature"]]/total_revenue)-(miner_fee/num_comments)
            transactions[k["signature"]] += divisible_amt*commenter_fee
            divisible_amt = divisible_amt -  divisible_amt*commenter_fee

            for l in k["likes"]:
                #can assume that we've already encountered user in first loop
                transactions[l] += k["likes"][l]/top_commenter["signature"]

        return top_comments, transactions
    

    def consensus(self):
        chain_list = self.chain_collection
        print("RUNNING CONSENSUS")
        #chain list should be list of blockchains collected from nodes
        #chain_list.append(self.export_chain())
        #chain list is: (ip, port): pickle(actual_chain_list)
        d = {} #dict to count most common chains
        for i in chain_list:
            key = self.hash(i)
            if key in d:
                d[key]['count']+=1
            else:
                d[key]={'count':1, 'list':i}
        max_len = 0
        current_chain = self.chain
        curr_key = self.hash(current_chain) #current key in count dict
        for j in d.keys():
            if len(d[j]['list']) > max_len:
                current_chain = d[j]['list']
                max_len = len(current_chain)
            elif len(d[j]['list']) == max_len:
                if d[curr_key]['count'] < d[j]['count']:
                    current_chain = j['list']
                    curr_key = self.hash(current_chain)
                elif d[self.hash(current_chain)]['count'] == d[j]['count']:
                    print("TIE IN PROTOCOL!")
                    #++self
        self.chain = current_chain
        
    #def add_comments(self, comments_list):
        ##merge comments& likes
    def get_top_comments(self, max_ret=10):
        #would be more effecient with linked list in terms of insertion but 
        #this still wins cuz we need to export as array
        #worst case n**2 when we have items sorted in the inverse direction
        #AND user requests a large amount, but 
        #this is intended for no more than 150 comments which i think should be pretty doable 
        #IF performance is bad do a binary search
        if len(self.comments) < 10:
            return self.comments
        sol =[random.choice(list(comments.items()))] #cannot exceed 10
        for i in self.comments.keys():
           
            if len(self.comments[i]["likes"]) > len(sol[-1]["likes"]):
                if len(sol) < max_ret:
                    sol.pop(-1)
                j = len(sol)-1
                while ((j > 0) and (len(self.comments[i]["likes"]) > len(sol[j]["likes"]))):
                    j-=1
                    sol.insert(self.commnets[i])
        #now return comments to a dict
        sol_d = {}
        print(sol)
        for j in sol:
            print(j)
            sol_d[self.hash(j['uname']+j['comment'])] = j
        return sol_d
    
    def mining_proof(self):
        return True

    def mine(self, uname=""):
        #make it to where you can't mine new block till old block
        #has been around for an hou
        #if time.time() - self.chain[-1]["timestamp"] < 60:
         #   print("to early to mine")
         #   return
        if len(self.comments) < 1:
            print("not enough comments to mine, self.comments: ", self.comments)
            return
        allowed_index = 0 
        if ((time.time() - self.chain[-1]["timestamp"]) > 10000):
            allowed_index = 1
        if (self.mining_proof()) or (len(self.chain) < 5):
            #self.comments = self.get_top_comments()
            self.comments, self.transactions = self.compute_transactions()
            self.create_block(uname, self.hash(self.chain[-1]), "Signature1")
