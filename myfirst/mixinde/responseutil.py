def wrap_response(response):
    response['code'] = 1000
    response['codedes'] = '没发现问题'
    return response

APPID=''
SECRET_KEY=''

# 代码都是根据思路来的

class Code:
    SUCCESS = 1000
    FAILED = 2222

    @classmethod
    def des(cls, code):
        if code == cls.SUCCESS:
            return 'is ok  ok'
        elif code == cls.FAILED:
            return 'not ok ...'
        else:
            return '我也不知道'


# Mixin 提供某些功能的类
class ResponseMixin():
    @staticmethod
    def wrap_response(response):
        if not response.get('code'):
            response['code'] = Code.SUCCESS
        if not response.get('codedes'):
            response['codedes'] = Code.des(response.get('code'))
        return response


class UtilMixin():
    @staticmethod
    def savepic(filename, content):
        with open(filename, 'wb') as f:
            f.write(content)

    @staticmethod
    def wrapdic(res_dict):
        """
        返回状态码以及结果,1000 default
        :param res_dict: 需要包裹的返回值字典类型
        :return: 装饰之后的dict
        """
        if not res_dict.get('code'):
            res_dict['code'] = Code.SUCCESS
        if not res_dict.get('codedes'):
            res_dict['codedes'] = Code.des(res_dict.get('code'))
        return res_dict
