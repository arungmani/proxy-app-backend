import pika
import json
from app.services.socket import sio


# Establish a connection to RabbitMQ
# connection = pika.BlockingConnection(pika.ConnectionParameters("192.168.1.37"))

# channel = connection.channel()

# # Declare the queue
# channel.queue_declare(queue="message_queue")


def add_data(data_instance):
    # Convert the instance's data to JSON
    message = json.dumps(data_instance.__dict__)
    # Publish the message to the queue
    channel.basic_publish(exchange="", routing_key="message_queue", body=message)
    print(" [x] Sent message:", message)
    
    return


def callback(ch, method, properties, body):
    # Decode the body and parse JSON
    data = json.loads(body.decode('utf-8'))
    print(f" [x] Received {data}")
    sio.emit(
        "task_notification",
        {"message": f"New task {data['task_name']} added by {data['user']}"},
        broadcast=True,
        skip_sid=data['sid'],  # Ensure 'sid' is part of your message
    )
    
    

async def consume_queue():
    channel.basic_consume(
        queue="message_queue", auto_ack=True, on_message_callback=callback
    )
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

    connection.close()
    return
