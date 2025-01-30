import pika
import time
from app.config import settings

def start_consumer():
    while True:
        try:
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

            def callback(ch, method, properties, body):
                print(f" [x] Received {body.decode()}")
                # Add your processing logic here

            channel.basic_consume(
                queue='posts',
                on_message_callback=callback,
                auto_ack=True
            )

            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

        except Exception as e:
            print(f"Connection failed: {e}")
            time.sleep(5)

if __name__ == "__main__":
    start_consumer()