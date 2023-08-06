#!/usr/bin/env python2
# coding=utf-8
from core.manager import BaseManager
import json
import os
import time
from aliyunsdkcore.client import AcsClient
from aliyunsdkcdn.request.v20141111.PushObjectCacheRequest import PushObjectCacheRequest
from aliyunsdkcdn.request.v20141111.DescribeRefreshTasksRequest import DescribeRefreshTasksRequest


class AliyunManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super(AliyunManager, self).__init__(*args, **kwargs)

    def get_client(self, *args, **kwargs):
        ak = kwargs.get('ak')
        secret = kwargs.get('secret')
        region = kwargs.get('region')
        return AcsClient(ak, secret, region)

    def warn_up(self, url_file):
        with open(url_file) as f:
            data = f.read()
        req = PushObjectCacheRequest()
        req.set_ObjectPath(data)
        body = self.client.do_action_with_exception(req)
        print(body)
        self.task_id = json.loads(body).get('PushTaskId')
        return body

    def get_status(self, task_id=None):
        if task_id is None:
            task_id = self.task_id
        req = DescribeRefreshTasksRequest()
        req.set_TaskId(task_id)
        req.set_PageSize(50)
        page_number = 1
        task_list = []
        while True:
            req.set_PageNumber(page_number)
            body = self.client.do_action_with_exception(req)
            _data = json.loads(body)
            task_list.extend(_data['Tasks']['CDNTask'])
            if not _data['PageSize'] or not _data['TotalCount'] :
                break
            if _data['TotalCount']/_data['PageSize'] < page_number:
                break
            page_number += 1
        return task_list

    def watch_status(self, task_id=None, interval=10):
        task_list = self.get_status(task_id)
        while True:
            complate = True
            for task in task_list:
                print("{Process}\t{ObjectPath}".format(**task))
                if task.get('Status') != "Complete":
                    complate = False
            if complate:
                break
            time.sleep(interval)
            task_list = self.get_status(task_id)
        print("done")




if __name__ == "__main__":
    ak = os.getenv("AK", "")
    secret = os.getenv("SECRET", "")
    region = os.getenv("REGION", "")
    url_file = os.getenv("URL_FILE", "")
    manager = AliyunManager(ak=ak, secret=secret, region=region)
    manager.warn_up(url_file)
    manager.watch_status()



