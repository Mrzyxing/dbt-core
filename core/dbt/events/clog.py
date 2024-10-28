import os
import json
from dataclasses import dataclass, asdict
from dataclasses_json import dataclass_json

from vadata_utils_public import KafkaHelper

k = KafkaHelper('sys.dp.dbt.permodel.log')

@dataclass_json
@dataclass(kw_only=True)
class ClogEvent:
    zeus_job_id: str = '0'
    zeus_action_id: str = '0'
    zeus_hive_user: str = '0'
    status: str
    execution_time_s: float
    message: str
    node_id: str
    database: str
    schema: str
    table: str
    target_fqn: str
    started_at: str
    compiled_code: str

    def __init__(self, status, execution_time, message, node_id, database, schema, table, target_fqn, started_at, compiled_code):
        self.zeus_job_id = os.environ.get('zeus_job_id', '0')
        self.zeus_action_id = os.environ.get('zeus_action_id', '0')
        self.zeus_hive_user = os.environ.get('USER', '0')
        self.status = status
        self.execution_time_s = execution_time
        self.message = message
        self.node_id = node_id
        self.database = database
        self.schema = schema
        self.table = table
        self.target_fqn = target_fqn
        self.started_at = started_at
        self.compiled_code = compiled_code

    def __str__(self):
        return f"""
         status: {self.status} 
         execution_time: {self.execution_time_s} 
         message: {self.message} 
         node id: {self.node_id} 
         databse: {self.database} 
         schema: {self.schema} 
         table: {self.table} 
         full table: {self.target_fqn} 
         started at: {self.started_at}
         compiled code: {self.compiled_code} 
        """

    def send(self):
        msg = json.dumps(asdict(self), ensure_ascii=False)
        #print(f"send as kafka message: {msg}")
        k.send(msg)
