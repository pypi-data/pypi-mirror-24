import requests
import json
import re
from base64 import b64decode
from json import loads
from traceback import format_exc
from typing import List

import geoalchemy2
import sqlalchemy
from amazon_kclpy.kcl import Checkpointer, RecordProcessorBase
from amazon_kclpy.messages import Record
from redis import Redis
from sqlalchemy import Column, Table, MetaData
from sqlalchemy.engine import Connection

from .config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, JOB_MANAGER
from .logger import logger


SQLALCHEMY_TYPES = {
    'datetime': sqlalchemy.DateTime,
    'integer': sqlalchemy.Integer,
    'float': sqlalchemy.Float,
    'text': sqlalchemy.Text,
    'point': geoalchemy2.Geometry
}


elasticache = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)


class RecordProcessor(RecordProcessorBase):
    """AWS Kinesis specific implementation of a consumer. This class provides
    methods which are invoked when a set of records is read off a stream and
    manages our position in it."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def initialize(self, shard: int):
        logger.info('Record processor shard id: {}'.format(shard))

    def handle_record(self, record: Record):
        try:
            record = b64decode(record.get('data'))
            logger.info(record)
            record = loads(record)
            record = validate(record)
            record = convert_geoms(record)
            record = load_into_database(record, self.connection)
            forward(record)
        except:
            exception = format_exc()
            for line in exception.split('\n'):
                logger.error(line)

    def process_records(self, records: List[Record], checkpointer: Checkpointer):
        for record in records:
            self.handle_record(record)

        # Kinesis Streams requires the record processor to keep track of the
        # records that have already been processed in a shard. The KCL takes
        # care of this tracking for you by passing a Checkpointer object to
        # process_records.
        #
        # If you don't pass a parameter, the KCL assumes that the call to
        # checkpoint means that all records have been processed, up to the
        # last record that was passed to the record processor.

        checkpointer.checkpoint()

    def shutdown(self, checkpointer, reason):
        logger.info('Shutting down: {}'.format(reason))

    # ========================== #
    # Job Manager Communications #
    # ========================== #

    def accepted(self, job_id: int):

        requests.post(JOB_MANAGER, data={
            'id': job_id,
            'status': 'accepted'
        }).raise_for_status()

    def success(self, job_id: int):

        requests.post(JOB_MANAGER, data={
            'id': job_id,
            'status': 'success'
        }).raise_for_status()

    def fail(self, job_id: int, reason: str):

        requests.post(JOB_MANAGER, data={
            'id': job_id,
            'status': 'failure',
            'reason': reason
        }).raise_for_status()


def validate(payload: dict) -> dict:
    """Ensure the incoming message data is structured the way we expect.

    :example:
    >>> validate({
    ...     'id': 123456789,
    ...     'table': 'ufo_sightings',
    ...     'columns': {},
    ...     'rows': [[]]
    ... })
    """

    for key in ['id', 'table', 'columns', 'rows']:
        try:
            assert key in payload
        except AssertionError:
            raise AssertionError('Payload is missing key: {}'.format(key))
    return payload


def convert_geoms(payload: dict) -> dict:
    """Convert informal representations of geospatial data to WKT, if any
    geospatial data is being provided."""

    # Collect the indices of any geospatial columns, if present.

    point_indices = []
    for i, dtype in enumerate(payload['columns'].values()):
        if dtype == 'point':
            point_indices.append(i)

    # This regex matches comma separated values enclosed within parentheses.

    regex = re.compile(r'\((.*),(.*)\)')

    # Use the regex to extract and transform values for each row at the columns
    # specified by the collected indices.

    for row in payload['rows']:
        for i in point_indices:
            match = re.match(regex, row[i])
            latitude, longitude = match.groups()
            row[i] = 'SRID=4326;POINT({} {})'.format(latitude, longitude)

    return payload


def load_into_database(payload: dict, connection: Connection) -> dict:
    """Given the metadata in the record, upsert the contents of the records
    data payload into the appropriate table.

    :example:
    >>> load_into_database({
    ...     'id': 123456789
    ...     'table': 'ufo_sightings',
    ...     'columns': {
    ...         'datetime': 'datetime',
    ...         'location': 'geometry',
    ...         'type': 'string'
    ...     }
    ...     'rows': [
    ...         ['sometime', 'somewhere', 'blorg']
    ...     ]
    ... })
    """

    # Convert the type specifications for each column into SQLAlchemy Column
    # objects, and then into a SQLAlchemy Table. This will let SQLAlchemy take
    # care of sanitizing the input data for us.

    columns = []
    for key, value in payload['columns'].items():
        columns.append(Column(key, SQLALCHEMY_TYPES[value]))
    table = Table(payload['table'], MetaData(), *columns)

    # Convert the input payload into the format that SQLAlchemy expects for a
    # bulk insert.

    rows = []
    column_names = payload['columns'].keys()
    for row in payload['rows']:
        rows.append(dict(zip(column_names, row)))

    connection.execute(table.insert(), rows)

    return payload


def forward(payload: dict) -> dict:
    """Forward a copy of the payload.

    :example:
    >>> forward({
    ...   'id': 123456789
    ... })
    """

    elasticache.set(payload['id'], json.dumps(payload))
    return payload
