import functools

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import threading
import time
import shutil
import pathlib
import requests

# warning: importing pathlib replace any "import os" order

# https://nachtimwald.com/2019/12/10/python-http-server/
# SSL: https://realpython.com/python-http-server/


class QuietSimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def log_error(self, *args):
        pass


class TemporaryWebServer(object):
    def __init__(self, fpath='/tmp/wserver', port=8000, host=None):
        self._path: pathlib.Path = pathlib.Path(fpath)
        self._host=host
        self._port=int(port)
        self._interface=''
        self._thread=None
        self._httpd=None
        self._files={}
        self._timeout=0

    def url(self, path=None):
        host=self._host or self._interface
        if host:
            url='http://%s:%d' % (host, self._port)
            if path:
                if path[0]!='/':
                    url += '/'
                url += path
            return url

    def server(self):
        handler=functools.partial(QuietSimpleHTTPRequestHandler, directory=self.pathstr())
        with ThreadingHTTPServer((self._interface, self._port), handler) as httpd:
            try:
                self._httpd=httpd
                httpd.serve_forever()
            except:
                pass
            httpd.server_close()

        self._httpd=None

    def pathstr(self):
        try:
            return str(self._path)
        except:
            pass

    def createPath(self):
        try:
            self._path.mkdir(parents=True, exist_ok=True)
            return True
        except:
            pass
        return False

    def getPathForFile(self, fname):
        try:
            return self._path.joinpath(fname)
        except:
            pass

    def isFile(self, fname):
        try:
            p=self.getPathForFile(fname)
            if p.exists() and p.is_file():
                return True
        except:
            pass
        return False

    def importFile(self, fpath, fname=None, timeout=0):
        try:
            sp=pathlib.Path(fpath)
            if sp.is_file():
                self.start()
                if not fname:
                    fname=sp.name
                tp=self.getPathForFile(fname)
                shutil.copyfile(str(sp), str(tp))
                self._files[fname]={'fname': fname, 'timeout': timeout}
                self._timeout=time.time()+60
                url=self.url(fname)
                if url:
                    return url
        except:
            pass
        return False

    def removeFile(self, fname):
        try:
            if fname:
                p=self.getPathForFile(fname)
                p.unlink()
                try:
                    del self._files[fname]
                except:
                    pass
                return True
        except:
            pass
        return False

    def isFileTimeout(self, fname):
        try:
            timeout=self._files[fname]['timeout']
            if timeout>0 and self.isFile(fname):
                p=self.getPathForFile(fname)
                info=p.stat()
                age=time.time()-info.st_mtime
                if age>=timeout:
                    return True
        except:
            pass
        return False

    def getFiles(self):
        try:
            files=[]
            for f in self._path.iterdir():
                fname=f.name
                if not self.isFile(fname):
                    continue
                if self.isFileTimeout(fname):
                    self.removeFile(fname)
                    continue
                files.append(fname)
            return files
        except:
            pass

    def start(self):
        if not self._thread:
            self.createPath()
            self._thread=threading.Thread(target=self.server)
            self._thread.daemon=True
            self._thread.start()

    def stop(self):
        if self._thread:
            try:
                self._httpd.shutdown()
            except:
                pass

            try:
                # force a fake request to the server (may be waiting for a request)
                requests.get('http://localhost:%d/fake' % self._port, timeout=1.0)
            except:
                pass

            self._thread.join()
            self._thread=None

    def isRunning(self):
        if self._thread:
            return True
        return False

    def manager(self):
        files=self.getFiles()
        if files:
            self._timeout=time.time()+60

        if time.time()>self._timeout:
            self.stop()

    def __del__(self):
        self.stop()


if __name__ == '__main__':
    ws=TemporaryWebServer('/tmp/wserver')
    ws.importFile('/tmp/myfile', 'fhe', 600)
    ws.start()
