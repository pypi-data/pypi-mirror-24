import asyncio
import aiohttp

class Request:

    def __init__(self, url, callback, meta=None):
        self.url = url
        self.callback = callback
        self.meta = meta


class Response:

    def __init__(self, body, url, meta=None, callback = None):
        self.body = body
        self.url = url
        self.meta = meta
        self.callback = callback


class Spider:
    start_urls = []

    def parse(self, response):
        pass


class Middleware:
    def __init__(self):
        self.web = aiohttp.ClientSession()
    def __del__(self):
        self.web.close()
    @asyncio.coroutine
    def get(self,req):
        response = yield from self.web.get(req.url)
        body = yield from response.read()
        response.close()
        return Response(body, req.url, req.meta, req.callback)

    def save(self, data):
        print(data)


class Scheduler:

    def __init__(self,spider, midw = Middleware):
        self.spider = spider
        self.midw = midw()
        self.request = []  # 请求队列
        self.response = [] # 回应队列
        self.thread_num = 16  # 线程数

    def __start(self):
        for url in self.spider.start_urls:
            self.request.append(Request(url, self.spider.parse))

    def putRequest(self):
        loop = asyncio.get_event_loop()
        def putRes(fur):
            self.response.append(fur.result())
        try:
            tasks = []
            while 1:
                if self.request:
                    num = 0
                    if len(self.request)<self.thread_num:
                        num = len(self.request)
                    else:
                        num = self.thread_num
                    for i in range(num):
                        task = asyncio.ensure_future(self.midw.get(self.request.pop()))
                        task.add_done_callback(putRes)
                        tasks.append(task)
                    if tasks:
                        loop.run_until_complete(asyncio.wait(tasks))
                        self.doResponse()
                    tasks.clear()
                else:
                    break
        except Exception as e:
            print("ERROR:",e)
        finally:
            loop.close()

    def doResponse(self):
        while self.response:
            res = self.response.pop()
            try:
                for req in res.callback(res):
                    if type(req) == Request:
                        self.request.append(req)
                    else:
                        self.midw.save(req)
            except Exception as e:
                print("ERROR:",e)
    def start(self):
        self.__start()
        self.putRequest()
        print("The end ...")
