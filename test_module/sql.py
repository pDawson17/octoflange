import sqlite3
import pickle
import time
import hashlib
#use sha256
#conn = sqlite3.connect(':memory:') #in memory db
#conn = sqlite3.connect('file.db')
class sql_handler:
    #wrapper for sql
    def __init__(self):
        """
        ##TODO
        --add function to get next item in queue if we dont have timestamp and elems are left in queue
           self.app_process contains:
                message queue (from front end to back) 
                    -> columns: tstamp, request, dest_ip, dest_port, next_tstamp=None
                    #so we hold first and last timestamps in app for queue. then when
                    #popping values we select next timestamp, update. on insert pop
                    #tstamp of newly inserted value to oldest val, update oldest
                nodes:
                    -> columns: uname, ip, port, signature
                also: Nodes w/ data we own
           self.data contains:
                stringified versions of all data
                    -> columns, content hash, content, owner uname(/id/signature?)
                table2:
                    tags -> columns: tagname: pickled set of content hash's?
        """
        #self.app_process = sqlite3.connect('app_process.db', check_same_thread=False)
        self.mq_first = 0 #stores timestamp
        self.mq_last = 0 #stores timestamp
        #self.data =  sqlite3.connect('data.db')
#with conn: allows to skip commit and close
        #self.app_process_cursor = self.app_process.cursor() #creates cursor to run sql commands
        #self.data_cursor = self.data.cursor()
        self.create_nodes_table()
        self.create_message_queue_table()
        self.create_data_table()
        self.create_blockchain_table()


###############
#1) Node Operators
#**corresponds to line 16 in sql.py
#TODO:  Implement search by signature
###############
    def get_nodes(self):
        """
           return all nodes
        """
        app_process = sqlite3.connect('app_process::memory:', check_same_thread=False)
        app_process_cursor = app_process.cursor()
        app_process_cursor.execute("SELECT * FROM nodes")
        sol = app_process_cursor.fetchall()
        app_process.commit()
        app_process.close()
        return sol

    def insert_node(self, node_tup, node_uname = "", node_sig = ""):
        """
           node_tup is node tuple-> (ip, port, uname, signature)
        """
        signature = hashlib.sha256((node_tup[0]+node_tup[4]).encode('utf-8')).hexdigest()
        app_process = sqlite3.connect('app_process::memory:', check_same_thread=False)
        app_process_cursor = app_process.cursor()
        app_process_cursor.execute("INSERT INTO nodes VALUES (:ip, :port, uname, :signature)", {"ip":node_tup[0], "port":node_tup[1], "uname":node_tup[2], "signature":node_sig})
        app_process.commit()
        app_process.close()

    def delete_node(self, node_tup):
        """
           node_tup is node tuple-> (uname, ip, port, sig)
        """
        signature = hashlib.sha256((uname+node_sig).encode('utf-8')).hexdigest() #hash value
        app_process = sqlite3.connect('app_process::memory:', check_same_thread=False)
        app_process_cursor = app_process.cursor()
        app_process_cursor.execute("DELETE FROM nodes WHERE ip==(:ip) AND port==(:port)", { "ip":node_tup[1], "port":node_tup[2]})
        app_process.commit()
        app_process.close()

    def search_node(self, node_tup):
        """
           node_tup is node tuple-> (uname, ip, port, signature)
        """
        signature = hashlib.sha1(node_tup[0]+node_tup[4])
        app_process = sqlite3.connect('app_process::memory:', check_same_thread=False)
        app_process_cursor = app_process.cursor()
        out = app_process_cursor.execute("SELECT FROM nodes WHERE signature==(:signature)", { "signature":signature })
       
        app_process.commit()
        app_process.close()
        if not out:
            return (None,None)
        return out
        
##############
#2) Data Operators
#***corresponds to line 44 in sql_flask.py
#Need to implement Search
##############
    def insert_data(self, i_data, data_sig = "", attachment = "", owner=""):
        """
            data, data_sig
            1)should data_sig be postername+comment hashed?
            or something more user searchable?
        """
        likes = pickle.dumps([])
        dislikes = pickle.dumps([])
        input_data = pickle.dumps(i_data)
        print("INSERTING", input_data)

        data = sqlite3.connect('data::memory:', check_same_thread=False)
        data_cursor = data.cursor()
        data_cursor.execute("INSERT INTO localdata VALUES (:data_sig, :data, :attachment, :likes, :dislikes, :owner)", {"data_sig":data_sig, "data":input_data, "attachment":attachment, "likes":likes, "dislikes":dislikes, "owner":owner})
        data.commit()
        data.close()
    
    def update_likes(self, data_sig, personal_sig, like=True):
        """
           adds your signature to likes
           false likes means add to dislikes
        """
        data_i = sqlite3.connect('data::memory:', check_same_thread=False)
        data_cursor = data_i.cursor()
        data_cursor.execute("SELECT * FROM localdata WHERE data_sig==(:data_sig)", {"data_sig":data_sig})
        obj = data_cursor.fetchone()
        likes_list =  obj[3]
        dislikes_list = obj[4]
        if like:
            lst = pickle.loads(likes_list)
            if personal_sig not in lst:
                lst.append(personal_sig)
                likes_list = pickle.dumps(lst)
        else: 
            lst = pickle.loads(dislikes_list)
            if personal_sig not in lst:
                lst.append(personal_sig)
                dislikes_list = pickle.dumps(lst)
        data_cursor.execute('UPDATE localdata SET likes = (:likes_list), dislikes = (:dislikes_list) WHERE data_sig==(:data_sig)', {"likes_list": likes_list, "dislikes_list":dislikes_list, "data_sig":data_sig})
        item = data_cursor.fetchall()
        data_i.commit()
        data_i.close()
        return item

    def delete_data(self, data_sig):
        """
           removes single item from data table based on data sig
        """
        data_i = sqlite3.connect('data::memory:', check_same_thread=False)
        data_cursor = data_i.cursor()
        data_cursor.execute('DELETE FROM localdata where data_sig==(:data_sig)', {"data_sig":data_sig})
        item = data_cursor.fetchall()
        data_i.commit()
        data_i.close()
        return item

    def generate_data_list(self, data_list):
        """
           takes list of data tuples & converts all to json for react app
           de-pickles info
        """
        sol = []
        for i in data_list:
            sol.append({
                "data_sig": i[0],
                "data": pickle.loads(i[1]),
                "attachment": i[2],
                "likes":pickle.loads(i[3]),
                "dislikes":pickle.loads(i[4]),
                "owner": i[5]
                    })
        return sol

    def get_data(self):
        """
           returns everything in data table
               0: data_sig text,
               1: data text,
               2: attachment text,
               3: likes pickled list
               4: dislikes pickeld list
               5: owner text
        """
        data_i = sqlite3.connect('data::memory:', check_same_thread=False)
        data_cursor = data_i.cursor()
        data_cursor.execute('SELECT * FROM localdata')
        item = data_cursor.fetchall()
        data_i.commit()
        data_i.close()
        return self.generate_data_list(item)

   # def search(self, signature)
##################
#3) Blockchain Operators
#***corresponds to line 92 in sql_flask.py
#################
    def get_chain(self):
        """
           returns chain as list of objects, return and unpickle
        """
        app_process = sqlite3.connect('app_process::memory:', check_same_thread=False)
        app_process_cursor = app_process.cursor()
        app_process_cursor.execute("SELECT * FROM blockchain LIMIT 1")
        sol = app_process_cursor.fetchall()
        app_process.commit()
        app_process.close()
        print(sol, "in get chain")
        return sol

    def replace_chain(self, chain):
        """
           inserts new chain
        """
        app_process = sqlite3.connect('app_process::memory:', check_same_thread=False)
        app_process_cursor = app_process.cursor()
        tstamp = time.time()
        app_process_cursor.execute("INSERT INTO blockchain VALUES (:tstamp, :chain)", {"tstamp":tstamp, "chain":chain})

        app_process.commit()
        app_process.close()

   
    def clear_hist(self):
        """
           clears table
        """
        app_process = sqlite3.connect('app_process::memory:', check_same_thread=False)
        app_process_cursor = app_process.cursor()
        tstamp = time.time()
        app_process_cursor.execute("DELETE * FROM blockchain")

        app_process.commit()
        app_process.close()


###############
#4) Message Queue Operators
#**corresponds to line 123 in sql_flask.py
##############
    def insert_message(self, message_text, address_tup=("",0)):
        """
           message is already pickled and ready to go
           address tup has who we're planning on sending it to. ""/0 means send to random i guess
           also updates queue vals
        """
        app_process = sqlite3.connect('app_process::memory:', check_same_thread=False)
        app_process_cursor = app_process.cursor()
        tstamp = time.time()
        if self.mq_first == 0:
            self.mq_first = tstamp
            self.mq_last = tstamp
        app_process_cursor.execute("INSERT INTO message_queue VALUES (:tstamp, :message, :ip, :port, :next)", {"tstamp":tstamp, "message":message_text, "ip":address_tup[0], "port":address_tup[1], "next":0})
        if self.mq_first != tstamp:
            app_process_cursor.execute("UPDATE message_queue SET next_tstamp = (:next) WHERE tstamp == (:last)", {"next":tstamp,"last":self.mq_last})
        self.mq_last = tstamp
        app_process.commit()
        app_process.close()

    def pop_message(self):
        """
           returns top of queue
        """
        app_process = sqlite3.connect('app_process::memory:', check_same_thread=False)
        app_process_cursor = app_process.cursor()
        app_process_cursor.execute("SELECT * FROM message_queue WHERE tstamp==(:first)", {"first":self.mq_first}) 
        item = app_process_cursor.fetchone()
        if item == None:
            return
        app_process_cursor.execute("DELETE FROM message_queue WHERE tstamp==(:first)", {"first":self.mq_first})
        self.mq_first = item[4] #now sets first to next item pointed to
        app_process.commit()
        app_process.close()
        return item


#######
#Create Tables
######
    def create_message_queue_table(self):
        """
            creates message queue table
        """
        app_process = sqlite3.connect('app_process::memory:', check_same_thread=False)
        app_process_cursor = app_process.cursor()
        app_process_cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='message_queue'")
        if app_process_cursor.fetchone()[0]==1:
            return
        app_process_cursor.execute("""
            CREATE TABLE message_queue (
                tstamp real,
                request text,
                dest_ip text,
                dest_port integer,
                next_tstamp real
            )
                """)
        app_process.commit()
        app_process.close()

    def create_nodes_table(self):
        """
            creates nodes table
        """
        app_process = sqlite3.connect('app_process::memory:', check_same_thread=False)

       #app_process = sqlite3.connect('app_process.db', check_same_thread=False)
        app_process_cursor = app_process.cursor()
        app_process_cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='nodes'")
        if app_process_cursor.fetchone()[0]==1:
            return
        app_process_cursor.execute("""
            CREATE TABLE nodes ( 
                ip text,
                port integer,
                uname text
                siganture blob,
            )
                """)
        app_process.commit()
        app_process.close()

    def create_data_table(self):
        """
            creates data table
        """
        print("CREATE DATA")
        #data_i = sqlite3.connect('data.db', check_same_thread=False)
        data_i = sqlite3.connect('data::memory:', check_same_thread=False)
        data_cursor = data_i.cursor()
        data_cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='localdata'")
        if data_cursor.fetchone()[0]==1:
            return
        data_cursor.execute("""
            CREATE TABLE localdata (
                data_sig text,
                data text,
                attachment text,
                likes text,
                dislikes text,
                owner text
            )
                """)
        data_i.commit()
        data_i.close()

    def create_blockchain_table(self):
        """
            creates blockchain table
        """
        print("CREATE Blockchain")
        #data_i = sqlite3.connect('data.db', check_same_thread=False)
        data_i = sqlite3.connect('app_process::memory:', check_same_thread=False)
        data_cursor = data_i.cursor()
        data_cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='blockchain'")
        if data_cursor.fetchone()[0]==1:
            return
        data_cursor.execute("""
            CREATE TABLE blockchain (
                userSig text,
                userId text,
                lastUpdate text,
                chain text
            )
                """)
        data_i.commit()
        data_i.close()


#c.execute("""
#        CREATE TABLE friends (
#            uname text,
#            address text,
#            last_interaction integer
#        )
#        """) #whatever command as docstring

#c.execute("INSERT INTO friends VALUES ('u1', 'i work', 1)")
#e1 = example("u1", "hey", 10)
#c.execute("INSERT INTO friends VALUES (?,?,?), (emp1.first, emp1.second, emp1.third)") #includes escaping to avoid sqlinjection
#c.execute("SELECT * FROM friends WHERE uname=='u1'")
#print(c.fetchall())
#c.fetchmany(5) selects 5 val
#conn.commit()
#conn.close()
