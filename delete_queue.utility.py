import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

for queue_name in sys.argv:
    channel.queue_delete(queue=queue_name)

connection.close()