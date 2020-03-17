import time
import logging


logger_statistics=logging.getLogger('statistic')
class StatisticsMiddle():
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):
        print('before call')
        start_time=time.time()
        time_for=time.localtime()
        print(request)
        path=request.path
        response=self.get_response(request)
        end_time=time.time()
        print('after call')
        log_dict={
            'start_time':time.strftime('%Y,%m,%d %X',time_for),
            'used_time':end_time - start_time,
            'path':path
        }
        # time1=end_time - start_time
        # total='time : '+time1+'path : '+path
        # logger_statistics.info(total)

        #repr可以直接转成json
        logger_statistics.info(repr(log_dict))
        return response