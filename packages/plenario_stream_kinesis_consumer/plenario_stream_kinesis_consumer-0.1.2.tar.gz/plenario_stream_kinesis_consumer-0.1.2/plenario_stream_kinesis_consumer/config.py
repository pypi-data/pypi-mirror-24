from os import getenv


DATABASE_URI = getenv('DATABASE_URI', 'postgresql://postgres:password@localhost:5432/postgres')
JOB_MANAGER = getenv('DATABASE_URI', 'http://etl.plenar.io')

REDIS_HOST = getenv('REDIS_HOST', 'localhost')
REDIS_PORT = getenv('REDIS_PORT', 6379)
REDIS_PASSWORD = getenv('REDIS_PASSWORD', None)

KINESIS_STREAM = getenv('KINESIS_STREAM', 'dev')
