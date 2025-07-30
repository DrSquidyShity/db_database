import click
import requests
import duckdb

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


DB_DATA_FILE= "db_data.db"

TRAIN_TABLE = "train"
TRAIN_DATA_TABLE = "train_data"

URL = "https://www.iceportal.de/api1/rs/status"
DEFAULT_FLASK_PORT = 5001

def fetch_and_insert(ice_number: str):
    try:
        response = requests.get(URL, timeout=5)
        data = response.json()
        connectivity = data.get("connectivity")

        database_con = duckdb.connect(DB_DATA_FILE)

        timestamp = datetime.now().isoformat()
        connection = 1 if data.get("connection") == True else 0
        service_level = data.get("serviceLevel")
        gps_status = data.get("gpsStatus")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        speed = data.get("speed")
        internet = data.get("internet")
        connection_current_state = connectivity.get("currentState")
        connection_next_state = connectivity.get("nextState")
        connection_remaining_time_seconds = connectivity.get("remainingTimeSeconds")
        server_time = data.get("serverTime")

        date = datetime.now().date().isoformat()
        train_number = ice_number

        train_type = data.get("trainType")
        series = data.get("series")
        tzn = data.get("tzn")
        bip_installed = 1 if data.get("bapInstalled") == True else 0

        # Insert into Train Relation if not alread contained
        already_created = database_con.sql(f"""
            SELECT COUNT(*)
            FROM {TRAIN_TABLE}
            WHERE train_number = '{ ice_number }' and
                  date = '{ date }'
        """).fetchone()

        if already_created == None or already_created[0] < 1:
            query_train = f"""
                INSERT INTO { TRAIN_TABLE } (date, train_number, train_type, series, tzn, bap_installed)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            values_train = [date, train_number, train_type, series, tzn, bip_installed]
            database_con.execute(query_train, values_train)

        # Insert into { TRAIN_DATA_TABLE }
        query_train_data = f"""
            INSERT INTO {TRAIN_DATA_TABLE} (timestamp, connection, service_level, gps_status, latitude, 
                                            longitude, speed, internet, connection_current_state,
                                            connection_next_state, connection_remaining_time_seconds, server_time,
                                            date, train_number)
            VALUES (?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?)
        """
        train_data_values = [timestamp, connection, service_level, gps_status, latitude, 
                             longitude, speed, internet, connection_current_state, connection_next_state,
                             connection_remaining_time_seconds, server_time, date, train_number]
        database_con.execute(query_train_data, train_data_values)

        print(f"[{timestamp}] Daten gesichert.")
    except Exception as e:
        print(f"[{datetime.now().isoformat()}] Fehler: {e}")

def create_tables():
    con = duckdb.connect(DB_DATA_FILE)

    print("Creating tables if necessary...")

    con.sql(f"""
        CREATE TABLE IF NOT EXISTS { TRAIN_TABLE } (
            date DATE NOT NULL,
            train_number VARCHAR NOT NULL,
            train_type VARCHAR,
            series VARCHAR,
            tzn VARCHAR,
            bap_installed BOOlEAN,
            PRIMARY KEY (date, train_number)
        )
    """)

    # Create Train Data Table if needed
    con.sql(f"""
        CREATE TABLE IF NOT EXISTS { TRAIN_DATA_TABLE } (
            timestamp TIMESTAMP PRIMARY KEY,
            connection BOOLEAN,
            service_level VARCHAR,
            gps_status VARCHAR,
            latitude VARCHAR,
            longitude VARCHAR,
            speed DOUBLE,
            internet VARCHAR,
            connection_current_state VARCHAR,
            connection_next_state VARCHAR,
            connection_remaining_time_seconds INTEGER,
            server_time BIGINT,
            date DATE,
            train_number VARCHAR,
            FOREIGN KEY (date, train_number) REFERENCES {TRAIN_TABLE}(date, train_number)
        )
    """)


@click.command()
@click.option('-i', '--interval', type=int, default=30, help="The interval in which the API gets called.")
@click.option('-t', '--test', is_flag=True, default=False, help="Change URL to localhost + change name of databasefile (Avoid accidental editing of real file)")
@click.option('-d', '--display', is_flag=True, default=False, help="Print the current data.")
@click.argument('icenumber', type=str, required=False)
def main(interval: int, test: bool, display: bool, icenumber: str):

    if test:
        global DB_DATA_FILE
        global URL
        URL = f"http://localhost:{ DEFAULT_FLASK_PORT }/api1/rs/status"
        DB_DATA_FILE = "test_" + DB_DATA_FILE

    if display:
        con = duckdb.connect(DB_DATA_FILE)
        for table in [TRAIN_DATA_TABLE, TRAIN_TABLE]:
            con.sql(f"SELECT * FROM { table }").show()
        return 0
    
    if not icenumber:
        raise click.UsageError("Missing argument: ICE-Number is required unless --display (-d) is set.")

    icenumber = "ICE " + icenumber
    
    create_tables()
    scheduler = BlockingScheduler()
    scheduler.add_job(fetch_and_insert, 'interval', seconds = interval, args=[icenumber])
    print("Scheduler gestartet. Drücke Strg + C zum Beenden.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nBeendet durch Benutzer (Strg + C).")

if __name__ == '__main__':
    main()
