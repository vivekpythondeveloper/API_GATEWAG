from sqlalchemy import create_engine
from models.client import create_client_table
from db import sql_uri
import psycopg2


class ClientHandler:
    def __init__(self) -> None:
        self.Client = create_client_table()
    def get_domain_from_email(self, admin_email):
        if "@" in admin_email:
            return admin_email.split("@")[-1]
        else:
            raise ValueError("Invalid admin email format. Please provide a valid email address.")
        
    def get_org_details_by_domain(self, domain):
        filters = {"domain": domain}
        return self.Client.dynamic_query(filters=filters)
    
    # Function to create a schema
    def create_schema(self,schema_name):
        conn = psycopg2.connect(sql_uri)
        cur = conn.cursor()
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
        conn.commit()
        cur.close()
        conn.close()

    def add_client(self, data):
        client_name = data['client_name']
        domain = data['domain']
        schema = domain.split(".")[0]
        schema_assign = f"schema_{schema}"
        admin_email = data['admin_email']
        trial_start_date = data.get('trial_start_date')
        trial_end_date = data.get('trial_end_date')
        subscription_start_date = data.get('subscription_start_date')
        subscription_end_date = data.get('subscription_end_date')

        # Attempt to insert the new client
        new_client = self.Client.insert(client_name, domain, schema_assign, admin_email,
                                trial_start_date, trial_end_date,
                                subscription_start_date, subscription_end_date)
        if new_client:
            self.create_schema(schema_assign)
        return new_client

