import pika
from app.config import settings

def send_post_notification(message: str):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            credentials=pika.PlainCredentials(
                username=settings.rabbitmq_user,
                password=settings.rabbitmq_password
            )
        )
    )
    
    channel = connection.channel()
    channel.queue_declare(queue='posts')
    channel.basic_publish(
        exchange='',
        routing_key='posts',
        body=message
    )
    connection.close()