from distutils.core import setup

setup(
    name='plenario_stream_kinesis_consumer',
    packages=['plenario_stream_kinesis_consumer'],
    version='0.1.1',
    description='A stream consumer of open data for plenar.io',
    author='Jesus Bracho',
    author_email='jbrach347@gmail.com',
    url='https://github.com/UrbanCCD-UChicago/plenario-stream-kinesis-consumer',
    download_url='https://github.com/UrbanCCD-UChicago/plenario-stream-kinesis-consumer/archive/0.1.tar.gz',
    keywords=['open data', 'kinesis client library', 'streaming', 'etl'],
    classifiers=[],
    install_requires=[
        'requests',
        'amazon-kclpy',
        'boto3',
        'pygogo',
        'redis',
        'sqlalchemy',
        'psycopg2',
        'geoalchemy2',
    ]
)
