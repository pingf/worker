import asyncio
import random
import select
import pycurl



async def multicurl_simple(data, index):
    print(index)
    return 'haha'
    try:
        import signal
        from signal import SIGPIPE, SIG_IGN
        signal.signal(signal.SIGPIPE, signal.SIG_IGN)
    except ImportError:
        pass
    m = pycurl.CurlMulti()
    m.setopt(pycurl.M_PIPELINING, True)

    curls = []


    urls = ['https://www.douban.com', 'http://www7a.nanhushi.com', 'http://www.csdn.net', #'https://www.google.com',
            'http://www.bing.com', 'http://www.baidu.com','https://www.douban.com', 'http://www7a.nanhushi.com', 'http://www.csdn.net', #'https://www.google.com',
            'http://www.bing.com', 'http://www.baidu.com'
            ]

    DEFAULT_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm; Baiduspider/2.0; +http://www.baidu.com/search/spider.html) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80() Safari/537.36'
    for i in range(5):
        c = pycurl.Curl()
        # c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.URL, urls[random.randint(0, 4)])
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.NOSIGNAL, 1)
        c.setopt(pycurl.USERAGENT, DEFAULT_USER_AGENT)

        c.setopt(pycurl.CONNECTTIMEOUT, 10)
        c.setopt(pycurl.TIMEOUT, 10)
        m.add_handle(c)
        curls.append(c)


    #
    #
    while 1:
        ret, num_handles = m.perform()
        # ret, num_handles = m.perform()
        if ret != pycurl.E_CALL_MULTI_PERFORM: break

    fd_set = set()
    while num_handles:
        # print('handles:', num_handles)
        # print(rrr, '?'*400)
        # print(m)
        #
        # mfdset = m.fdset()
        # print(mfdset, '>>>>>>>>>')
        # fdset_reading = [e for e in mfdset[0]]
        # fdset_writing = [e for e in mfdset[1]]
        # fdset_exception = [e for e in mfdset[1]]
        # fdsets = fdset_reading + fdset_writing + fdset_exception
        #
        # epoll = select.epoll()
        #     epoll = select.epoll()
        #     for fd in fdsets:
        #         # print(fd,'fd')
        #         fd_set.add(fd)
        #         if fd not in fd_set:
        #             epoll.register(fd, select.EPOLLIN | select.EPOLLOUT | select.EPOLLHUP | select.EPOLLPRI)
        #     events = epoll.poll(0.5)
        #     if len(events) > 0:
        #         print('event:', events, '?'*400)
        #         continue
        num_q, ok_list, err_list = m.info_read()
        for c in ok_list:
            # c.fp.close()
            # c.fp = None
            m.remove_handle(c)
            effective_url = c.getinfo(pycurl.EFFECTIVE_URL)
            http_code = c.getinfo(pycurl.HTTP_CODE)
            print('success', effective_url, http_code)
            # print("Success:", c.filename, c.url, c.getinfo(pycurl.EFFECTIVE_URL))
        for c, errno, errmsg in err_list:
            # c.fp.close()
            # c.fp = None
            m.remove_handle(c)
            effective_url = c.getinfo(pycurl.EFFECTIVE_URL)
            http_code = c.getinfo(pycurl.HTTP_CODE)
            print('failed', effective_url, http_code)
            # print("Failed: ", c.filename, c.url, errno, errmsg)

        ret = m.select(0.5)
        if ret == -1:
            # await asyncio.sleep(0.5)
            continue

        while True:
            ret, num_handles = m.perform()
            if ret != pycurl.E_CALL_MULTI_PERFORM:
                break
    return curls

    # for i, c in enumerate(curls):
    #     effective_url = c.getinfo(pycurl.EFFECTIVE_URL)
    #     http_code = c.getinfo(pycurl.HTTP_CODE)
    #     print(i, effective_url, http_code)

if __name__ == '__main__':
    multicurl_simple()
