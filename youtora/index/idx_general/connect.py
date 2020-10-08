# make global connection to elastic search
from elasticsearch_dsl.connections import connections

connections.create_connection()
