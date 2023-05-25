"""
sentry_s3_nodestore.backend
~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2015 by Ernest W. Durbin III.
:copyright: (c) 2023 by Negashev Alexandr.
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

import io
import simplejson
from base64 import urlsafe_b64encode
from time import sleep
from uuid import uuid4
import zlib

from minio import Minio

from sentry.nodestore.base import NodeStorage

def retry(attempts, func, *args, **kwargs):
    for _ in range(attempts):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            sleep(0.1)
            raise
    raise

class S3NodeStorage(NodeStorage):

    def __init__(self, bucket_name=None, endpoint=None, region='eu-west-1', aws_access_key_id=None, aws_secret_access_key=None, max_retries=5, secure=True):
        self.max_retries = max_retries
        self.bucket_name = bucket_name
        
        self.client = Minio(
                endpoint,
                access_key=aws_access_key_id,
                secret_key=aws_secret_access_key,
                secure=secure
            )
    def delete(self, id):
        """
        >>> nodestore.delete('key1')
        """
        self.client.remove_object(self.bucket_name, id)
        
    def delete_multi(self, id_list):
        """
        Delete multiple nodes.
        Note: This is not guaranteed to be atomic and may result in a partial
        delete.
        >>> delete_multi(['key1', 'key2'])
        """
        error = self.client.remove_objects(self.bucket_name, [{'Key': id} for id in id_list])
        if error:
            for err in error:
                raise Exception(err)

    def _get_bytes(self, id):
        """
        >>> nodestore._get_bytes('key1')
        b'{"message": "hello world"}'
        """
        result = retry(self.max_retries, self.client.get_object, bucket_name=self.bucket_name, object_name=id)
        return zlib.decompress(result.read())

    def _set_bytes(self, id, data, ttl=None):
        """
        >>> nodestore.set('key1', b"{'foo': 'bar'}")
        """
        retry(self.max_retries, self.client.put_object, bucket_name=self.bucket_name, object_name=id, data=zlib.compress(data))

    def generate_id(self):
        return urlsafe_b64encode(uuid4().bytes)
