from pika import BlockingConnection, ConnectionParameters, PlainCredentials

connection = BlockingConnection(
    ConnectionParameters(
        host='rabbitmq',
        port=15672,
        virtual_host='/',
        credentials=PlainCredentials(
            username='guest',
            password='guest'
        )
    )
)

channel = connection.channel()

start_consuming = channel.start_consuming
