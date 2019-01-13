import multiprocessing

bind = '0.0.0.0:8000'
worker_class = 'gevent'
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = '/tmp/gunicorn_cgid_access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
