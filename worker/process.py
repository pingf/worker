import logging
import traceback
from concurrent import futures
from logcc.util.table import trace_table as tt

from copy import deepcopy
from loader.function import load

from worker.exception import WorkerException
from worker.util import grouper_it


def work(data, info):
    log = logging.getLogger(info.get('log', 'worker'))
    results = []
    chunk_size = info.get('chunk_size', 20)
    max_workers = info.get('max_workers', 4)
    try:
        func_str = info.get('worker')
        func = load(func_str)
    except Exception as exc:
        log.error('dynamic worker func invalid! %s' % exc)
        return results

    Executor = futures.ProcessPoolExecutor
    backup_info = deepcopy(info)
    with Executor(max_workers=max_workers) as executor:
        future_to_data = {}

        for index, data_chunked in enumerate(grouper_it(data, chunk_size)):
            log.debug('process worker chunk %d processing.' % (index))
            info = deepcopy(backup_info)
            info['index'] = index
            future_to_data[executor.submit(func, data_chunked, info)] = data_chunked

        for future in futures.as_completed(future_to_data):
            data = future_to_data[future]
            try:
                result = future.result()
            except Exception as exc:
                tt(exc)
                log.critical('exception catched! %s %s' % (exc, type(exc)))
                result = WorkerException('%s -- %r' % (type(exc), exc))
            results.append(result)
    return results
