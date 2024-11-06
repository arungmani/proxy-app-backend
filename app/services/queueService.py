import pika
import json
from app.services.socket import sio
import asyncio
import time
from app.services.socket import broadcast_message

def connectRabbitMq():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("192.168.1.54"))
        channel = connection.channel()
        return channel, connection
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Connection to RabbitMQ failed: {e}. Retrying...")
        return None, None  # Return None if connection fails

def add_data_to_Broadcastqueue(data_instance):
    channel, connection = connectRabbitMq()
    if not channel or not connection:
        print("Failed to connect to RabbitMQ. Cannot send message.")
        return

    try:
        channel.queue_declare(queue="broadcast_queue")
        message = json.dumps(data_instance.__dict__)
        channel.basic_publish(exchange="", routing_key="broadcast_queue", body=message)
        print(" [x] Sent message:", message)
    except pika.exceptions.AMQPError as e:
        print(f"Failed to publish message: {e}")
    finally:
        connection.close()


def callback(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))
    print(f" [x] Received {data}")
    asyncio.run(broadcast_message(data))

def consume_queue():
    while True:  # Keep trying to consume even after failure
        channel, connection = connectRabbitMq()
        if not channel or not connection:
            time.sleep(5)
            continue  # Retry after a delay if connection fails

        try:
            channel.queue_declare(queue="broadcast_queue")
            channel.basic_consume(
                queue="broadcast_queue", auto_ack=True, on_message_callback=callback
            )
            print(" [*] Waiting for messages. To exit press CTRL+C")
            channel.start_consuming()
        except pika.exceptions.StreamLostError as e:
            print(f"Stream lost, reconnecting: {e}")
            time.sleep(5)  # Wait before retrying
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection error: {e}")
            time.sleep(5)  # Wait before retrying
        finally:
            if connection:
                connection.close()
