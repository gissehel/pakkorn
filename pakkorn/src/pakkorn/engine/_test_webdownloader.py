from pakkorn.engine import WebDownloader

from pakkorn.test.testutils import get_test_full_path
from pakkorn.test.testutils import apply_assert_on_file
from pakkorn.test.testutils import TestCase

test_server = "test.giss.mine.nu"
test_root = "pakkorn"

import os
import urllib2
import time

def get_test_root_uri() :
    return "http://%s/%s" % (test_server,test_root)

class DownloadHandler(object) :
    def __init__(self,url,testcase) :
        self._ended = False
        self._url = url
        self._download_id = None
        self._local_file = None
        self._reason = None
        self._testcase = testcase

    def ended(self) :
        return self._ended

    def url(self) :
        return self._url

    def local_file(self) :
        return self._local_file

    def reason(self) :
        return self._reason

    def start_download(self, downloader, output_dir=None) :
        self._download_id = downloader.add_donwload(
            url = self._url,
            on_end = self.on_end_download,
            on_fail = self.on_fail_download,
            output_dir = output_dir
            )

    def on_end_download( self, download_id, url, local_file ) :
        # TODO : because there is no thread right now
        self._download_id = download_id

        self._testcase.assertEqual(self._ended,False)
        self._testcase.assertEqual(self._download_id,download_id)
        self._testcase.assertEqual(self._url,url)
        self._testcase.assertEqual(os.path.exists(local_file),True)

        self._local_file = local_file
        self._ended = True

    def on_fail_download( self, download_id, url, reason ) :
        # TODO : because there is no thread right now
        self._download_id = download_id

        self._testcase.assertEqual(self._ended,False)
        self._testcase.assertEqual(self._download_id,download_id)
        self._testcase.assertEqual(self._url,url)

        self._reason = reason
        self._ended = True

class TestWebDownloader(TestCase) :
    class_dir_prefix = [__module__]
    def test_creation(self) :
        web_downloader = WebDownloader()
        self.assertNotEqual(web_downloader,None)
        web_downloader = None

    def _test_download(self,file,dir_test) :
        web_downloader = WebDownloader()
        url = urllib2.posixpath.join(get_test_root_uri(),'test',file)
        handler = DownloadHandler(url=url,testcase=self)
        handler.start_download(web_downloader,output_dir=dir_test)
        # Let's wait 3 seconds
        for trying in xrange(5) :
            trying # unused
            if handler.ended() :
                break
            # 1 second
            time.sleep(1)

        self.assertEqual(handler.ended(),True)
        web_downloader = None
        return handler

    def test_download_image(self) :
        self.set_test_path( 'test_download_image', use_dir=True, clean=True )
        handler = self._test_download('imagetest.gif',self.get_full_test_path())
        self.assertFileIsReference(handler._download_id)

    def test_download_audio(self) :
        self.set_test_path( 'test_download_audio', use_dir=True, clean=True )
        handler = self._test_download('audiotest.au',self.get_full_test_path())
        self.assertFileIsReference(handler._download_id)

