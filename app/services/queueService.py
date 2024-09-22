import pika
import json


def add_data(obj):

    connection = pika.BlockingConnection(pika.ConnectionParameters("192.168.43.2"))

    channel = connection.channel()

    channel.queue_declare(queue="message_queue")
    data = obj()
    message = json.dumps(data.__dict__)
    channel.basic_publish(exchange="", routing_key="message_queue", body=message)
    print(" [x] Sent 'Hello World!'")

    connection.close()

    return


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


def consume_queue():

    connection = pika.BlockingConnection(pika.ConnectionParameters("192.168.43.2"))

    channel = connection.channel()

    channel.queue_declare(queue="message_queue")
    channel.basic_consume(
        queue="message_queue", auto_ack=True, on_message_callback=callback
    )
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

    connection.close()
    return
