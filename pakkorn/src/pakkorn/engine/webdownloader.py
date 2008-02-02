import os
import sha
from web import Web
import cPickle as serializer
import threading

from pakkorn.config import register_key

class ThreadDownloader(threading.Thread) :
    def __init__(self,download_id,url,filename,manager) :
        super(ThreadDownloader,self).__init__()

        http_proxy = None
        if manager._config['proxy'] is not None :
            http_proxy = manager._config['proxy'].split(':')

        self._web = Web(http_proxy=http_proxy)
        self._download_id = None
        self._url = None
        self._filename = None
        self._manager = manager
        self._active = False
        self._continuation_condition = threading.Condition()
        self._continuation = True

        self.reinit(download_id,url,filename)

    def _change_continuation(self,download_id=None,url=None,filename=None,continuation=True) :
        self._continuation_condition.acquire()
        self._download_id = download_id
        self._url = url
        self._filename = filename
        self._continuation = continuation
        self._active = True
        self._continuation_condition.notify()
        self._continuation_condition.release()

    def reinit(self,download_id,url,filename) :
        self._change_continuation(download_id=download_id,url=url,filename=filename,continuation=True)

    def end(self) :
        self._change_continuation(continuation=False)

    def active(self) :
        self._continuation_condition.acquire()
        result = self._active
        self._continuation_condition.release()

        return result

    def run(self) :
        while True :
            self._continuation_condition.acquire()

            while self._continuation and self._download_id is None :
                self._continuation_condition.wait()

            continuation = self._continuation
            download_id = self._download_id
            url = self._url
            filename = self._filename

            self._continuation_condition.release()

            if not(continuation) :
                break
            if download_id is not None :

                self._continuation_condition.acquire()
                self._active = True
                self._continuation_condition.release()

                self._manager.on_start_download(download_id,thread=self)

                result = self._web.get(url,file=filename)

                success = result is not None

                self._continuation_condition.acquire()
                self._download_id = None
                self._filename = None
                self._url = None
                self._active = False
                self._continuation_condition.release()

                self._manager.on_stop_download(download_id,success=success,thread=self)


        self._manager.on_stop_thread(thread=self)

class WebDownloader(object) :

    instance = None

    def __init__(self,config=None,cache=None) :
        '''Constuctor'''

        if cache is None :
            cache = os.path.join('.','__cache__')

        self._max_downloads = 5
        self._max_downloads_per_site = 1
        self._config = config

        for parameter in ('max_downloads','max_downloads_per_site') :
            if self._config is not None and parameter in self._config :
                setattr(self,'_'+parameter,self._config[parameter])

        self._output_dir = cache
        self._index_dir = os.path.join(self._output_dir,'__index__')
        self._downloads_condition = threading.Condition()
        self._downloads_condition.acquire()
        self._downloads = {}
        self._downloads_condition.release()

        self._threads_condition = threading.Condition()
        self._threads_condition.acquire()
        self._working_threads = {}
        self._waiting_threads = []
        self._threads_condition.release()

        self._load_cache_index()

    def _create_download_id(self,url) :
        return sha.new(url).hexdigest()

    def add_donwload(self,url,priority=0,on_end=None,output_file=None,output_dir=None,on_fail=None) :
        '''Add a new download to the manager. The download can start at the discretion of the manager.
           The manager decide to download the file to the 'output_file' if given. If not, he decide to
           download the file using the filename provided by the server or by the url into the 'output_dir'
           if given. If both of them are missing, he decide to download it to any location that the
           manager thinks great, and remember that location. Once the download is finished, the callback
           'on_end' is called (if given). If the download fail, the callback on_fail is called.


           on_end(download_id,url,local_file)

           on_fail(download_id,url,reason)

           add_download returns a download_id used for other operations.
           '''

        if output_dir is None :
            output_dir = self._output_dir
        if not(os.path.exists(output_dir)) :
            os.makedirs(output_dir)

        download_id = self._create_download_id(url)
        filename = os.path.join(output_dir,download_id)

        # TODO : if download_id in self._downloads :
        # TODO : if os.path.exists(filename) :

        self._downloads_condition.acquire()
        self._downloads[download_id] = {'cache':{},'dynamic':{}}

        self._downloads[download_id]['cache']['url'] = url
        self._downloads[download_id]['cache']['filename'] = filename
        self._downloads[download_id]['cache']['download_id'] = download_id
        self._downloads[download_id]['cache']['status'] = 'waiting to start'
        self._downloads[download_id]['dynamic']['on_end'] = on_end
        self._downloads[download_id]['dynamic']['on_fail'] = on_fail
        self._downloads[download_id]['dynamic']['end_condition'] = threading.Condition()
        self._downloads_condition.release()

        self._save_cache_index_entry(download_id)

        self._threads_condition.acquire()
        download_thread = None

        if len(self._waiting_threads) == 0 :
            download_thread = ThreadDownloader(download_id,url,filename,manager=self)
            download_thread.start()
        else :
            download_thread = self._waiting_threads.pop(0)
            download_thread.reinit(download_id,url,filename)
        self._working_threads[download_thread] = download_id

        self._threads_condition.release()

        # download_thread.run()

        # web = Web()
        #
        # result = web.get(url,file=filename)
        #
        # if result is None :
        #     on_fail(download_id,url,'Failed downloading %s' % (url,))
        # else :
        #     on_end(download_id,url,filename)

        return download_id

    def iter_downloads(self) :
        '''Returns a dictonnary for each download in the manager (currently queued file, currently downloading file,
           or already downloaded file still in the manager).'''

        self._downloads_condition.acquire()
        iterkeys = self._downloads.keys()
        self._downloads_condition.release()

        return iter(iterkeys)

    def abort_download(self,download_id) :
        '''Abort a download using a download_id provided by other methods. the on_fail provided
           to add_download is called using "abort" as reason.'''

    def set_max_downloads(self, max_downloads) :
        '''Change the maximum concurrent downloads'''
        self._max_downloads = max_downloads

    def set_max_downloads_per_site(self, max_downloads_per_site) :
        '''Change the maximum concurrent downloads per site'''
        self._max_downloads_per_site = max_downloads_per_site

    def on_start_download(self,download_id,thread) :
        self._downloads_condition.acquire()
        self._downloads[download_id]['cache']['status'] = 'started'
        self._downloads_condition.release()
        self._save_cache_index_entry(download_id)

    def on_stop_download(self,download_id,success,thread) :
        self._downloads_condition.acquire()
        if success :
            self._downloads[download_id]['cache']['status'] = 'downloaded'
        else :
            self._downloads[download_id]['cache']['status'] = 'aborted'
        self._downloads_condition.release()
        self._save_cache_index_entry(download_id)

        self._threads_condition.acquire()
        del self._working_threads[thread]
        self._waiting_threads.append(thread)
        self._threads_condition.release()

        self._downloads_condition.acquire()
        (url,filename,) = map(self._downloads[download_id]['cache'].get,('url','filename'))
        (on_end,on_fail,end_condition) = map(self._downloads[download_id]['dynamic'].get,('on_end','on_fail','end_condition'))
        self._downloads[download_id]['dynamic'] = {}
        self._downloads_condition.release()

        #self._threads_condition.acquire()
        #thread.end()
        #self._threads_condition.release()

        if success :
            if on_end is not None :
                on_end(download_id,url,filename)
        else :
            if on_fail is not None :
                on_fail(download_id,url,'Failed downloading %s' % (url,))

        end_condition.acquire()
        end_condition.notify()
        end_condition.release()

    def on_stop_thread(self,thread) :
        self._threads_condition.acquire()
        if thread in self._working_threads :
            del self._working_threads[thread]
        if thread in self._waiting_threads :
            self._waiting_threads.remove(thread)
        self._threads_condition.release()

    def get_thread_status_string(self) :
        status_string = ""
        self._threads_condition.acquire()
        self._downloads_condition.acquire()
        status_string += "Active threads :\n  "
        status_string += "\n  ".join(map(lambda thread:"%s : %s" % (thread.getName(),self._downloads[self._working_threads[thread]]['cache']['url']),self._working_threads))
        status_string += "\nEnd Active threads\n"
        status_string += "Inactive threads :\n  "
        status_string += "\n  ".join(map(lambda thread:"%s" % (thread.getName(),),self._waiting_threads))
        status_string += "\nEnd Inactive threads\n"
        self._downloads_condition.release()
        self._threads_condition.release()

        return status_string

    def test_remove_waiting_thread(self) :
        name = None
        self._threads_condition.acquire()

        if len(self._waiting_threads)>0 :
            thread = self._waiting_threads.pop(0)
            name = thread.getName()
            thread.end()

        self._threads_condition.release()
        return name


    def _save_cache_index(self) :
        for download_id in self.iter_downloads() :
            self._save_cache_index_entry(download_id)

    def _load_cache_index(self) :
        self._downloads_condition.acquire()
        self._downloads = {}
        if not(os.path.exists(self._index_dir)) :
            os.makedirs(self._index_dir)
        for filename in os.listdir(self._index_dir) :
            index_filename = os.path.join(self._index_dir,filename)
            handle = open(index_filename,'rb')
            entry = serializer.load(handle)
            self._downloads[entry['download_id']] = {}
            self._downloads[entry['download_id']]['cache'] = entry
            self._downloads[entry['download_id']]['dynamic'] = {}
            handle.close()
        self._downloads_condition.release()

    def _save_cache_index_entry(self,download_id) :
        self._downloads_condition.acquire()
        if not(os.path.exists(self._index_dir)) :
            os.makedirs(self._index_dir)
        index_filename = os.path.join(self._index_dir,download_id)
        handle = open(index_filename,'wb')
        serializer.dump(self._downloads[download_id]['cache'],handle)
        handle.close()
        self._downloads_condition.release()

    def wait(self,download_id) :
        if download_id in self._downloads :
            end_condition = self._downloads[download_id]['dynamic'].get('end_condition',None)
            if end_condition :
                end_condition.acquire()
                while self._downloads[download_id]['cache']['status'] not in ('downloaded','aborted') :
                    end_condition.wait()
                end_condition.release()

    def clean(self) :
        self._threads_condition.acquire()
        for thread in list(self._waiting_threads) :
            thread.end()
        self._threads_condition.release()

    def get_filename(self,download_id) :
        filename = None
        self._downloads_condition.acquire()
        if self._downloads[download_id]['cache']['status'] == 'downloaded' :
             filename = self._downloads[download_id]['cache']['filename']
        self._downloads_condition.release()
        return filename

    def expire(self,url) :
        download_id = self._create_download_id(url)

        download = None

        self._downloads_condition.acquire()

        if download_id in self._downloads :
            status = self._downloads[download_id]['cache']['status']
            if status in ('downloaded','aborted') :
                download = self._downloads[download_id]
                del self._downloads[download_id]

        self._downloads_condition.release()

        index_filename = os.path.join(self._index_dir,download_id)
        if os.path.exists(index_filename) :
            os.remove(index_filename)
        standard_filename = os.path.join(self._output_dir,download_id)
        if os.path.exists(standard_filename) :
            os.remove(standard_filename)
        if download is not None :
            filename = download['cache']['filename']
            if os.path.exists(filename) :
                os.remove(filename)


register_key('max_downloads',int,doc='The maximum concurrent download number (unused)', default=5, advanced=False )
register_key('max_downloads_per_site',int,doc='The maximum concurrent download number per site (unused)', default=1, advanced=False )
register_key('proxy',str,doc='The proxy host:port if needed', default=None, advanced=False )



# web_downloader = WebDownloader()
