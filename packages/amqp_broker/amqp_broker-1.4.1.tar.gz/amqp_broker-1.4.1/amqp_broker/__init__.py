#!/usr/bin/python2.7
#-*- coding: utf-8 -*-
""" Main class of amqp_broker
Client and Server """

# VERSION 1.3.0

from uuid import uuid4
import pika

class Client(object):
    """ Class client broker """
    def __init__(self, server_host='127.0.0.1', key='hello', user='guest', password='guest'):
        credentials = pika.credentials.PlainCredentials(user, password)
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=server_host,
                credentials=credentials))
        except pika.exceptions.ProbableAuthenticationError:
            raise AMQPException('Authentication issue. Check your rights on AMQP server.')
        self.key = key
        self.response = None
        self.corr_id = str(uuid4())
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response,
                                   no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        """ Response interpreter """
        if self.corr_id == props.correlation_id:
            self.response = body

    def send(self, parameter):
        """ Send parameter to the server. 'parameter' is the function parameter.
        It has to be a string."""
        self.channel.basic_publish(exchange='',
                                   routing_key=self.key,
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id),
                                   body=str(parameter))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

class Server(object):
    """ Class AMQP Broker Server """
    def __init__(self, func, server_host='127.0.0.1', key='hello', user='guest', password='guest'):
        credentials = pika.credentials.PlainCredentials(user, password)
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=server_host,
                credentials=credentials))
        except pika.exceptions.ConnectionClosed:
            raise AMQPException('Cannot communicate to AMQP server. Install the package or start the service.')
        self.key = key
        self.func = func
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.key)

    def on_request(self, ch, method, props, body):
        """ Default method on_request from pika, but with some differences. """

        print " [x] Requested f(%s)" % body
        response = self.func(body)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def init(self):
        """ Initialization of the server """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue=self.key)

        print " [x] Awaiting connections"
        self.channel.start_consuming()

class AMQPException(Exception):
    """ Custom Exception """
    pass
