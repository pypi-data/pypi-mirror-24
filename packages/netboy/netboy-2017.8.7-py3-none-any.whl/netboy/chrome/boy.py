import json
import socket
from concurrent import futures

import time
from urllib.parse import urlparse

import websocket
from netboy.chrome.interface import ChromeInterface

# import falsy
#
#
# class ChromeShortException(Exception):
#     pass
#
#
# class ChromeEmptyException(Exception):
#     pass
#
#
# class ChromeECMAScriptException(Exception):
#     pass
#
#
# import asyncio as aio
#
#
# class ChromeTargetException(Exception):
#     pass
from netboy.util.grouper import grouper_it
from netboy.util.makeup import Makeup


class ChromeBoy:
    def __init__(self, **kwargs):
        self._host = kwargs.get('host', 'localhost')
        self._port = kwargs.get('port', 9222)
        self._url = '%s:%d' % (self._host, self._port)
        self._socket_timeout = kwargs.get('sockettimeout', 20)
        self._browser_url = 'ws://' + self._url + '/devtools/browser'
        self._id = 0
        self._user_agent = kwargs.get('useragent')
        self._http_header = kwargs.get('httpheader')
        self._cookies = kwargs.get('cookies')
        self._load_timeout = kwargs.get('loadtimeout', 15)
        self._auto_connect = kwargs.get('auto_connect', True)
        self._tabs = {}

    def screenshot(self, c=None, shot_quality=40, shot_format='jpeg'):
        if c is None:
            c = self.c
        try:
            doc_id = c.DOM.getDocument()['result']['root']['nodeId']
            body_id = c.DOM.querySelector(selector="body", nodeId=doc_id)['result']['nodeId']
            box = c.DOM.getBoxModel(nodeId=body_id)['result']['model']
            width, height = box['width'], box['height']
            c.Emulation.setVisibleSize(width=width, height=height)
            c.Emulation.forceViewport(x=0, y=0, scale=1)
            if height > 2000:
                time.sleep((height // 1000) * 0.05)
            screen = c.Page.captureScreenshot(format=shot_format, quality=shot_quality, fromSurface=False)["result"][
                "data"]
        except Exception as e:
            print(e, type(e))
            print('error when shot')
        return screen

    def cookies(self, c=None):
        if c is None:
            c = self.c
        cookies = c.Network.getCookies()['result']['cookies']
        return cookies

    def new_page(self, **kwargs):
        xhr = kwargs.get('xhr')
        url = kwargs.get('url')
        if not url.startswith('http'):
            url = 'http://'+url
        start = time.time()
        c = self.chrome()
        c.Network.enable()
        c.Page.enable()
        c.Page.navigate(url=url)
        c.wait_event("Page.frameStoppedLoading", timeout=60)
        end = time.time()
        if xhr:
            ss = '''
            var xhr = new XMLHttpRequest();
            xhr.open('GET', document.location, false);
            xhr.send(null);
            var headers = xhr.getAllResponseHeaders().toLowerCase();
            JSON.stringify({
                "title": document.title,
                "location": {
                    "href": window.location.href,
                    "origin": window.location.origin,
                    "host": window.location.host,
                    "hostname": window.location.hostname,
                    "pathname": window.location.pathname,
                    "port": window.location.port,
                    "protocol": window.location.protocol,
                    "search": window.location.search,
                },
                "charset": document.charset,
                "input_encoding": document.inputEncoding,
                "text": document.body.innerText,
                "body": document.body.outerHTML,
                "head": document.head.outerHTML,
                "referer": document.referrer,
                "base_uri": document.baseURI,
                "doctype": document.doctype,
                "domain": document.domain,
                "last_modified": document.lastModified,
                "URL": document.URL,
                "metas": Array.prototype.map
                .call(document.getElementsByTagName("meta"), function(meta){
                  prop = meta.getAttribute("property")
                  if (prop) {
                    return {"property":prop, "content":meta.content}
                  }
                  return {"name":meta.name, "content":meta.content}
                }).filter(function(meta){return meta.content != ''}),
                "links": Array.prototype.map.call(document.links,function(link){return link.href})
                .filter(function(text){ return !text.startsWith('javascript');}),
                "links2": Array.prototype.map.call(document.querySelectorAll("link"),function(link){return link.href})
                .filter(function(text){ return !text.startsWith('javascript');}),
                "scripts": Array.prototype.map.call(document.scripts,function(script){return script.src})
                .filter(function(text){ return !text.startsWith('javascript');}),
                "images": Array.prototype.map.call(document.images,function(img){return img.src})
                .filter(function(text){ return !text.startsWith('javascript');}),
                "xhr": {
                    "headers": headers,
                    "status": xhr.status,
                    "responseXML": xhr.responseXML,
                    "responseType": xhr.responseType,
                    "response": xhr.response,
                },
                "url": "%s",
                "time": %f
            });
            ''' % (url, end - start)
        else:
            ss = '''
            JSON.stringify({
                "title": document.title,
                "location": {
                    "href": window.location.href,
                    "origin": window.location.origin,
                    "host": window.location.host,
                    "hostname": window.location.hostname,
                    "pathname": window.location.pathname,
                    "port": window.location.port,
                    "protocol": window.location.protocol,
                    "search": window.location.search,
                },
                "charset": document.charset,
                "input_encoding": document.inputEncoding,
                "text": document.body.innerText,
                "body": document.body.outerHTML,
                "head": document.head.outerHTML,
                "referer": document.referrer,
                "base_uri": document.baseURI,
                "doctype": document.doctype,
                "domain": document.domain,
                "last_modified": document.lastModified,
                "URL": document.URL,
                "metas": Array.prototype.map
                .call(document.getElementsByTagName("meta"), function(meta){
                  prop = meta.getAttribute("property")
                  if (prop) {
                    return {"property":prop, "content":meta.content}
                  }
                  return {"name":meta.name, "content":meta.content}
                }).filter(function(meta){return meta.content != ''}),
                "links": Array.prototype.map.call(document.links,function(link){return link.href})
                .filter(function(text){ return !text.startsWith('javascript');}),
                "links2": Array.prototype.map.call(document.querySelectorAll("link"),function(link){return link.href})
                .filter(function(text){ return !text.startsWith('javascript');}),
                "scripts": Array.prototype.map.call(document.scripts,function(script){return script.src})
                .filter(function(text){ return !text.startsWith('javascript');}),
                "images": Array.prototype.map.call(document.images,function(img){return img.src})
                .filter(function(text){ return !text.startsWith('javascript');}),
                "url": "%s",
                "time": %f
            });
            ''' % (url, end - start)
        r = c.Runtime.evaluate(expression=ss)
        c.wait_event("Network.responseReceived", timeout=60)
        r = r['result']['result']['value']
        r = json.loads(r)
        r['text'], r['charset'] = Makeup.beautify(r['text'], r['charset'])
        r['body'], _ = Makeup.beautify(r['body'], r['charset'])
        r['head'], _ = Makeup.beautify(r['head'], r['charset'])
        self.update_effect(r)
        if kwargs.get('screenshot'):
            r['screenshot'] = self.screenshot(c, shot_quality=kwargs.get('shot_quality', 40),
                                              shot_format=kwargs.get('shot_format', 'jpeg'))
        if kwargs.get('cookies'):
            r['cookies'] = self.cookies(c)
        r['spider'] = 'chrome'
        self._tabs[c] = r
        self.c = c
        return r, c

    def get(self, url, **kwargs):
        kwargs['url'] = url
        r, c = self.new_page(**kwargs)
        c.close_target()
        self.browser.close()
        return r

    def update_effect(self, r):
        try:
            effect = r['URL'] if r['URL'].startswith('http') else r['url']
            hostname = urlparse(effect).hostname if effect else None
            r['hostname'] = hostname
            r['ip'] = socket.gethostbyname(hostname) if hostname else None
        except Exception as e:
            print(e, type(e))
            print('error when effect')

    def chrome(self):
        self.browser = websocket.create_connection(self._browser_url, timeout=self._socket_timeout)
        return ChromeInterface(self.browser, self._host, self._port)

    def close(self):
        for c in self._tabs.keys():
            c.close_target()
        self.browser.close()


class ConcurrentBoy:
    def run(self, data):
        d = data.get('data')
        i = data.get('info')
        results = []
        for dd in grouper_it(d, i.get('chunk_size', 10)):
            result = self._run(dd, i)
            results.extend(result)
        return results

    def _run(self, data, info):
        results = []
        with futures.ThreadPoolExecutor(max_workers=info.get("max_workers")) as executor:
            future_to_url = {}
            for i, payload in enumerate(data):
                d = {'url': payload} if type(payload) is str else payload
                d.update(info)
                # payload['chrome_id'] = i
                future_to_url[executor.submit(self.run1, d)] = d
            for future in futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                else:
                    # data['chrome_id'] = url['chrome_id']
                    results.append(data)
        return results

    def run1(self, payload):
        p = payload
        url = p.get('url')
        if not url:
            return None
        a = ChromeBoy(useragent=p.get('useragent'),
                      sockettimeout=p.get('sockettimeout'))
        r, c = a.new_page(url=p.get('url'),
                          xhr=p.get('xhr'),
                          cookies=p.get('cookies'),
                          screenshot=p.get('screenshot'),
                          )
        a.close()
        return r

    def view(self, results, filters):
        scene = []
        for result in results:
            updated = {key: result.get(key) for key in filters}
            scene.append(updated)
        return scene


if __name__ == '__main__':
    # boy = ChromeBoy()
    # r, c = boy.new_page('http://www.baidu.com', cookies=True, screenshot=True)
    # print(r.keys())
    # print(r['title'])
    # print(r['time'])
    # print(r['cookies'])
    # boy.screenshot(c)
    # boy.close()





    # a = ConcurrentBoy()
    # r = a.run({
    #     'data': [
    #         # 'http://www.baidu.com',
    #         'http://www.bing.com',
    #         # 'http://www.facebook.com',
    #     ],
    #     'info': {'chunk_size': 2, 'max_worker': 2, 'useragent': 2,
    #              'cookies': True,
    #              'screenshot': True,
    #              'xhr': True,
    #
    #              }
    # })
    # print(json.dumps(a.view(r, ['ip', 'hostname', 'title', 'location', 'time', 'url', 'referer', 'URL', 'links']),
    #                  indent=2, ensure_ascii=False))
    #
    boy = ChromeBoy()
    r = boy.get('http://www.baidu.com')
    print(r)
    #
