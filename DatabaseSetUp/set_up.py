import configparser
import sshtunnel
import psycopg2

def connect_to_database(write=None):
    config = configparser.ConfigParser()
    config.read('dbconfig.txt')
    dbconfig = config['DATABASE']
    # print(f"started connecting to the database: {time.strftime('%X')}")

    sshtunnel.SSH_TIMEOUT = 5.0
    sshtunnel.TUNNEL_TIMEOUT = 5.0
    with sshtunnel.SSHTunnelForwarder(
            (dbconfig["IP"], int(dbconfig["Port"])),
            ssh_username=dbconfig["User"], ssh_password=dbconfig["Password"],
            remote_bind_address=('localhost', 5432),
            local_bind_address=('localhost', 9954)
    ) as server:
        server.start()
        #      print("server connected")
        params = {
            'database': 'melogamadb',
            'user': dbconfig["User"],
            'password': dbconfig["Password"],
            'host': 'localhost',
            'port': 9954
        }
        conn = psycopg2.connect(**params)
        cur = conn.cursor()