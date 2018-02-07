import random

from wrap.exception import safe

from worker.worker import Worker

async def worker_do_sth(data, info):
# def worker_do_sth(data, info):
    assert len(data) == 2
    print(data, '>>>>>')
    return data

def xtest_it():
    print('>>>>')
    data = [
               'u11', 'u22', 'u33', 'u44',
               'u21', 'u22', 'u23', 'u24',
               'u31', 'u32', 'u33', 'u34',
               'u41', 'u42', 'u43', 'u44',
               'u51', 'u52', 'u53', 'u54',
           ] * 80
    info = {
        'worker': 'test.functional.test_worker_coroutine.worker_do_sth',
        'chunk_size': 2
    }
    worker = Worker(mode='coroutine')
    resp = worker.work(data, info)
    print(resp)
