import logging, os


DIR = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)
#logging.basicConfig(filename='test.log', level=logging.DEBUG)
logging.info('hi;')
logging.warning('ooops')