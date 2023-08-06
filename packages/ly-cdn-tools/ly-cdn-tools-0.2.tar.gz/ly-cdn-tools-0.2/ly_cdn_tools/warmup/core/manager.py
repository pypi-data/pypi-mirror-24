
class BaseManager(object):
    def __init__(self, *args, **kwargs):
        self.task_id = None
        self.client = self.get_client(*args, **kwargs)

    def get_client(self, *args, **kwargs):
        raise NotImplementedError

    def warm_up(self, url_file):
        raise NotImplementedError

    def get_status(self):
        raise NotImplementedError