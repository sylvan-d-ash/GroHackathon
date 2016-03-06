# List of modules to import when celery starts.
CELERY_IMPORTS = ('harvest')
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERYD_CONCURRENCY = 8
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_ACCEPT_CONTENT = ['json']

# Using rabbit-mq to store task state and results.
# BROKER_URL = 'amqp://localhost:5672//'
# CELERY_RESULT_BACKEND = 'amqp'

# OR using PostgreSQL to store task state and results.
BROKER_URL = 'sqla+postgresql://scott:tiger@localhost/mydatabase'
CELERY_RESULT_BACKEND = 'db+postgresql://scott:tiger@localhost/mydatabase'