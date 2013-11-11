#/usr/bin/env python
# coding=utf-8
import tornado.ioloop
import tornado.web
import os, datetime, time, hashlib

APP_ROOT = os.path.dirname(__file__)

# 密钥
secret_key = "secret_key"

class MainHandler(tornado.web.RequestHandler):
    """
    Web page demo
    """
    def get(self):
        timestamp = int(time.time()).__str__()
        params = {"sign":hashlib.md5(secret_key + timestamp).hexdigest().upper(), "time":timestamp}
        self.render(os.path.join(APP_ROOT, 'index.html'), params=params)
  
class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        # Permission check
        sign = self.get_argument("sign")
        timestamp = self.get_argument("time")
        if hashlib.md5(secret_key + timestamp).hexdigest().upper() != sign:
            self.write("sign error")
        elif self.request.files:  
            uploadFile = self.request.files['upload_image'][0]
            fileName =  time.strftime("%H%M%S") + '%d' % datetime.datetime.now().microsecond + '.' + uploadFile["filename"].split('.')[-1].lower()
            uploadPath = time.strftime("%Y/%m/%d")
            uploadRealPath = os.path.join(APP_ROOT, "upload", uploadPath)
            try:
                os.makedirs(uploadRealPath)
            except Exception:
                pass
            uploadRealFilePath = os.path.join(uploadRealPath, fileName)
            uploadedFile = open(uploadRealFilePath, "w")
            uploadedFile.write(uploadFile["body"])
            uploadedFile.close()
            self.write('{"status":200, "file":"%s"}' % os.path.join(uploadPath, fileName))
            

settings = {
    "debug": True,
}

application = tornado.web.Application([
    (r'/',MainHandler),
    (r'/upload', UploadHandler)
], **settings)

if __name__ == '__main__':
    application.listen(8001)
    tornado.ioloop.IOLoop.instance().start()
