import threading
import logbook

_logger = logbook.Logger(__name__)


class KeepaliveThread(threading.Thread):

    def __init__(self, client, session, interval):
        super(KeepaliveThread, self).__init__()
        self._client = client
        self._session = session
        self._interval = interval / 2.0
        self._stopped_event = threading.Event()
        self.daemon = True

    def run(self):
        _logger.debug('Backslash keepalive thread started')
        try:
            while not self._stopped_event.is_set():
                self._stopped_event.wait(timeout=self._interval)
                self._session.send_keepalive()
        except Exception: #pylint: disable=broad-except
            _logger.error('Quitting keepalive thread due to exception', exc_info=True)
            raise
        finally:
            _logger.debug('Backslash keepalive thread terminated')

    def stop(self):
        self._stopped_event.set()
