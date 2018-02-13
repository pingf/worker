import random
from copy import deepcopy
from time import sleep

from celery import chain, group, chord
from wrap.exception import safe

from worker.celery import work, celery_thread_worker, celery_coroutine_worker
from worker.celery_app import app
from worker.worker import Worker

# @app.task(bind=True)
# def simple(self, data, info):
#     sub_info = deepcopy(info)
#
#     worker = Worker(mode='thread')
#     resp = worker.work(data, sub_info)

# simple = app.task(bind=True)(celery_coroutine_worker)
simple = app.task(bind=True)(celery_thread_worker)


@safe(Exception, return_value={"state": "error"})
def worker_do_sth(data, info):
    # async def worker_do_sth(data, info):
    #     print(data, '111111')
    # sleep(1)
    # raise Exception('......')
    print('work' + str(data))
    sleep(2)
    print('after sleep')
    return data
    # return 'haha'
    # print(str(data) + '.2222')
    # print(info, '2222')


def sync_callback(self, results):
    print('final_si')
    print(results, '>>>>>>>>>>>>>>>>>>>>>>>>>>>')


@app.task(bind=True)
def final_callback(self, results):
    print('final')
    print(results, '>>>>>>>>>>>>>>>>>>>>>>>>>>>')

@app.task(bind=True)
def final_callback_si(self):
    print('final')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>')

@app.task(bind=True)
def callback(self, result):
    print('each' + str(result))
    return result
    # print(data)
    # print(info)


@app.task(bind=True)
def add(self, a, b):
    print(str(a) + '+' + str(b) + '=' + str(a + b))
    sleep(3)
    return a + b


@app.task
def dummy(*args, **kwargs):
    return "OK"


def test_celery():
    # g1 = group(add.si(2, 3))
    # g2 = group([add.si(4, 4)])
    # s1 = chord(g1, dummy.si())
    # s2 = chord(g2, dummy.si())
    # # func = chain([g1, g2]) | final_callback.s()
    # func = s1 | s2 | final_callback.s()
    # res = func()
    # print(res)




    data = [
        'u11', 'u22', 'u33', 'u44', 'u21', 'u22', 'u23', 'u24',
        'u31', 'u32',
        'u33', 'u34',
        'u41', 'u42', 'u43', 'u44', 'u51', 'u52', 'u53', 'u54',
    ]*1
    info = {
        'celery_worker': 'test.functional.test_celery.simple',
        'worker': 'test.functional.test_celery.worker_do_sth',
        'celery_max_workers': 1,
        'celery_chunk_size': 40,
        'chunk_size': 40,
        # 'final_callback': 'test.functional.test_celery.final_callback_si',
        'dummy': 'test.functional.test_celery.dummy',
        'sync_callback': 'test.functional.test_celery.final_callback',
        'each_callback': 'test.functional.test_celery.callback',
        # 'queue': 'worker'
    }
    # resp = work(data=data,

    worker = Worker(mode='celery')
    resp = worker.work(data, info)
    return resp
