import os
import socket

ENV_IP = os.environ.get('ENV_IP', '127.0.0.1')
ip = ENV_IP
if '.' not in ip:
    ip = [(s.connect(('223.5.5.5', 53)), s.getsockname()[0], s.close()) for s in
          [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

broker_url = os.environ.get('CELERY_BROKER_URL', 'amqp://dameng:hello@' + ip + '/worker')
# result_backend = 'redis://:password@host:port/db'
# result_backend =broker_url #os.environ.get('CELERY_RESULT_URL', 'file:///tmp/celery_results')
result_backend = os.environ.get('CELERY_RESULT_URL', 'redis://:hello@' + ip + ':6379/1')

task_serializer = 'pickle'#'msgpack'
result_serializer = 'json'
accept_content = ['json', 'msgpack', 'pickle']
timezone = 'UTC'
enable_utc = True
# CELERY_CHORD_PROPAGATES
chord_propagates = False
# worker_prefetch_multiplier = 1
worker_concurrency = 4

task_send_sent_event = True

# worker_hijack_root_logger=False
