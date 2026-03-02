import pika
import time

def callback(ch, method, properties, body):
    print(f"Worker received: {body.decode()}")
    time.sleep(1)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()

    channel.queue_declare(queue="tasks", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="tasks", on_message_callback=callback)

    print("Worker waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    main()