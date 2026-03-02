import pika

def publish_message(message: str):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()

    channel.queue_declare(queue="tasks", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="tasks",
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()