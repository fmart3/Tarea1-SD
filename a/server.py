import grpc
import cache_pb2
import cache_pb2_grpc

import redis
from concurrent import futures

class CacheServicer(cache_pb2_grpc.CacheServicer):
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def Get(self, request, context):
        value = self.redis_client.get(request.key)
        return cache_pb2.GetResponse(value=value.decode() if value else "")

    def Set(self, request, context):
        self.redis_client.set(request.key, request.value)
        return cache_pb2.SetResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cache_pb2_grpc.add_CacheServicer_to_server(CacheServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
