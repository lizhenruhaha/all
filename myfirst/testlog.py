import logging
import os
import django
os.environ['DJANGO_SETTINGS_MODULE']='myfirst.settings'
django.setup()

def logdemo():
    logger=logging.getLogger('django')
    logger.debug('Something went wrong c')
    logger.warning('Something went wrong b')
    logger.info('lc Something went wrong a')

if __name__ == '__main__':
    logdemo()


