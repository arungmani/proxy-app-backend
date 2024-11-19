import pika
import json
from app.services.socket import sio
import asyncio
import time
from app.services.socket import broadcast_message
from app.services.redisService import setCache


def connectRabbitMq():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("192.168.1.39"))
        channel = connection.channel()
        return channel, connection
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Connection to RabbitMQ failed: {e}. Retrying...")
        return None, None  # Return None if connection fails


def add_data_to_notification_queue(data_instance):
    channel, connection = connectRabbitMq()
    if not channel or not connection:
        print("Failed to connect to RabbitMQ. Cannot send message.")
        return

    try:
        channel.queue_declare(queue="notification_queue")
        message = json.dumps(data_instance.__dict__)
        channel.basic_publish(
            exchange="", routing_key="notification_queue", body=message
        )
        print(" [x] Sent message:", message)
    except pika.exceptions.AMQPError as e:
        print(f"Failed to publish message: {e}")
    finally:
        connection.close()


def callback(ch, method, properties, body):
    data = json.loads(body.decode("utf-8"))
    print(f" [x] Received {data}")
    print("THE TASK INFOR IS", data["task_info"])
    """ Show notification to online customers """
    asyncio.run(broadcast_message(data["task_info"], data["sid"]))
    """ For showing notification for off line customers """
    message = json.dumps(data["task_info"])
    user_ids = data["user_ids"]
    for user_id in user_ids:
        key = f"notifications_{user_id}"
        asyncio.run(setCache(key, message))


def consume_queue():
    while True:  # Keep trying to consume even after failure
        channel, connection = connectRabbitMq()
        if not channel or not connection:
            time.sleep(5)
            continue  # Retry after a delay if connection fails

        try:
            channel.queue_declare(queue="notification_queue")
            channel.basic_consume(
                queue="notification_queue", auto_ack=True, on_message_callback=callback
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
