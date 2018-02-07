import random
from copy import deepcopy
from time import sleep

from wrap.exception import safe

from worker.celery import app, work, celery_thread_worker, celery_coroutine_worker
from worker.worker import Worker

# @app.task(bind=True)
# def simple(self, data, info):
#     sub_info = deepcopy(info)
#
#     worker = Worker(mode='thread')
#     resp = worker.work(data, sub_info)

# simple = app.task(bind=True)(celery_coroutine_worker)
simple = app.task(bind=True)(celery_thread_worker)


@safe(Exception, return_value={"state":"error"})
def worker_do_sth(data, info):
# async def worker_do_sth(data, info):
    print(data, '111111')
    sleep(1)
    # raise Exception('......')
    return data
    # return 'haha'
    # print(str(data) + '.2222')
    # print(info, '2222')


# @app.task(bind=True)
def callback(results):
    print('final')
    print(results, '>>>>>>>>>>>>>>>>>>>>>>>>>>>')


def test_celery():
    data = [
               'u11', 'u22', 'u33', 'u44',
               'u21', 'u22', 'u23', 'u24',
               'u31', 'u32', 'u33', 'u34',
               'u41', 'u42', 'u43', 'u44',
               'u51', 'u52', 'u53', 'u54',
           ]*8
    info={
        'celery_worker': 'test.functional.test_celery.simple',
        'worker': 'test.functional.test_celery.worker_do_sth',
        'celery_max_workers': 4,
        'celery_chunk_size': 80,
        'chunk_size': 20,
        'final_callback': 'test.functional.test_celery.callback',
        'queue': '123'
    }
    # resp = work(data=data,

    worker = Worker(mode='celery')
    resp = worker.work(data, info)
    return resp
