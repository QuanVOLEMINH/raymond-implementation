import sys
from node import Node
import pika

topology = [
    {'name': 'A', 'neighbours': 'B,C', 'holder': 'D'},
    {'name': 'B', 'neighbours': 'A', 'holder': 'A'},
    {'name': 'C', 'neighbours': 'A', 'holder': 'A'},
    {'name': 'D', 'neighbours': 'A,E', 'holder': 'E'},
    {'name': 'E', 'neighbours': 'D', 'holder': 'self'},
    {'name': 'F', 'neighbours': 'D', 'holder': 'D'},
]

if __name__ == '__main__':
    if (len(sys.argv) < 4):
        print("usage: python treenode.py node_name neighbours holder")
    else:
        new_node = Node(sys.argv[1], sys.argv[2], sys.argv[3])

        running = True
        while running:
            message = input("Type message: ")
            if message == "establish":
                if new_node.name != 'A':
                    new_node.establish_connection()
                    new_node.receive_message()
                else:
                    # node A
                    new_node.establish_connection()
                    a_mess = input("Do you want to enter the critical section?")
                    if a_mess == 'y':
                        new_node.make_request()
                        new_node.receive_message()
            if message == "close":
                if new_node.connection:
                    new_node.close_connection()

        