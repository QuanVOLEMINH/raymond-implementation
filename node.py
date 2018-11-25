import pika

class Node:
    def __init__(self, name, neighbours, holder):
        self.name = name
        self.neighbours = neighbours.split(',')
        self.holder = holder
        self.using = False
        self.request_q = []
        self.asked = False
        self.connection = None
        self.channel = None

        print("This is node " + self.name)
        print("My neighbours are " + '-'.join(self.neighbours))
        print("My holder is " + self.holder)
    
    def print_neighbours(self):
        print(self.neighbours)
    
    def establish_connection(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        for n in self.neighbours:
            self.channel.queue_declare(queue = self.name + n)
        print("Established Connection !!!")
    
    def close_connection(self):
        for n in self.neighbours:
            self.channel.queue_delete(queue = self.name + n)
        self.connection.close()
        
    def send_message(self, message, dest):
        self.channel.basic_publish(exchange='', routing_key = self.name + dest, properties=pika.BasicProperties(headers={'sender': self.name}), body=message)
        print("Message sent to: " + dest)

    def receive_message(self):
        def callback(ch, method, properties, body):
            if properties.headers:
                if body.decode('ascii') == 'request': #request mess
                    self.request_q.append(properties.headers['sender'])
                    if (self.holder != 'self'):
                        if (not self.using):
                            self.make_request()
                    else:
                        print("I'm holding the token")
                        self.assign_priviledge()
                elif body.decode('ascii') == 'priviledge':
                    print("returned priviledge message")
                    self.holder = "self"
                    self.assign_priviledge()
            
        for n in self.neighbours:
            self.channel.basic_consume(callback, queue = n + self.name, no_ack = False)

        self.channel.start_consuming()
    
    def make_request(self):
        if self.holder != 'self' and (not self.asked):
            l = len(self.request_q)
            if (l == 0) or (self.request_q[l-1] != 'self'):
                self.request_q.append('self')
            if len(self.request_q) != 0:
                self.send_message('request', self.holder)
                self.asked = True
          
    def assign_priviledge(self):
        if self.holder == 'self' and (not self.using) and (len(self.request_q) != 0):
            self.holder = self.request_q.pop(0)
            self.asked = False
            if self.holder == 'self':
                self.using = True
                print("In critical section")
            else:
                self.send_message('priviledge', self.holder)
