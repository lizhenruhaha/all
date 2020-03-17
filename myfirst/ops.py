from logging import Filter

class XXXFilter(Filter):
    def filter(self, record):
        # 带有 lc 的不输出
        if 'lc' in record.msg:
            return False
        else:
            return True