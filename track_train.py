import os
import click
import csv
import requests
import duckdb

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


DB_DATA_FILE= "db_data.db"
TABLE = "db_data"

URL = "https://www.iceportal.de/api1/rs/status"
# URL = "http://localhost:5001/jetty/api/v1/status" 

def fetch_and_log(csv_file: str, ice_number: str):
    try:
        response = requests.get(URL, timeout=5)
        data = response.json()
        
        isodate = datetime.now().isoformat()
        with open(csv_file, mode='a', newline='') as file:
            
            connectivity = data.get("connectivity")
            writer = csv.writer(file)
            writer.writerow([
                isodate,
                ice_number,
                1 if data.get("connection") == True else 0,
                data.get("serviceLevel"),
                data.get("gpsStatus"),
                data.get("latitude"),
                data.get("longitude"),
                data.get("series"),
                data.get("trainType"),
                data.get("tzn"),
                data.get("wagonClass"),
                data.get("speed"),
                data.get("internet"),
                connectivity.get("currentState"),
                connectivity.get("nextState"),
                connectivity.get("remainingTimeSeconds"),
                1 if data.get("bapInstalled") == True else 0,
                data.get("serverTime")
            ])
        print(f"[{isodate}] Daten gesichert.")
    except Exception as e:
         print(f"[{datetime.now().isoformat()}] Fehler: {e}")

def insert_into_database(csv_file: str):
    con = duckdb.connect(DB_DATA_FILE)

    exists = con.sql(f"""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{ TABLE }'
    """).fetchone()

    # Create table if needed
    if exists == None or exists[0] <= 0:
        con.sql(f"""
            CREATE TABLE { TABLE } (
                timestamp TIMESTAMP,
                icenumber VARCHAR,
                connection BOOLEAN,
                servicelevel VARCHAR,
                gpsStatus VARCHAR,
                latitude DOUBLE,
                longitude DOUBLE,
                series VARCHAR,
                trainType VARCHAR,
                tzn VARCHAR,
                wagonClass VARCHAR,
                speed DOUBLE,
                internet VARCHAR,
                currentState VARCHAR,
                nextState VARCHAR,
                remainingTimeSeconds BIGINT,
                bapInstalled BOOLEAN,
                serverTime BIGINT
            );
        """)
        print(f"Created new table: { TABLE }")

    # Insert data into table
    con.sql(f"""
        INSERT INTO { TABLE }
        SELECT * FROM read_csv('{ csv_file }')
    """)
    count_inserted_lines = con.sql(f"SELECT count(*) FROM read_csv('{ csv_file }')").fetchone()[0]
    print(f"\nInserted {count_inserted_lines} tuples into table { TABLE }.")

    # Print 
    # con.sql(f"SELECT * FROM { TABLE }").show()


@click.command()
@click.option('-i', '--interval', type=int, default=60, help="The interval in which the API gets called.")
@click.option('-f', '--file', type=str, default="log_status.csv", help="Filename for the CSV-File.")
@click.option('-d', '--display', is_flag=True, default=False, help="Print the current data.")
@click.argument('icenumber', type=str, required=False)
def main(interval: int, file: str, display:bool, icenumber: str):

    if display:
        con = duckdb.connect(DB_DATA_FILE)
        con.sql(f"SELECT * FROM { TABLE }").show()
        return 0

    if not icenumber:
        raise click.UsageError("Missing argument: ICENumber is required unless --display (-d) is set.")

    icenumber = "ICE " + icenumber

    try:
        with open(file, mode='x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "icenumber", "connection", "servicelevel", "gpsStatus", "latitude", "longitude", "series", "trainType", "tzn", "wagonClass", "speed", "internet", "currentState", "nextState", "remainingTimeSeconds", "bapInstalled","serverTime"])
            print("Header zur CSV Datei hinzugefügt.")
    except FileExistsError:
        pass

    scheduler = BlockingScheduler()
    scheduler.add_job(fetch_and_log, 'interval', seconds = interval, args=[file, icenumber])
    print("Scheduler gestartet. Drücke Strg + C zum Beenden.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        insert_into_database(file)

        # Remove CSV file
        choice = input(f"Do you want to delete the CSV-File f{ file}? (y/n)").strip().lower()
        if choice == 'y':
            try:
                os.remove(file)
                print(f"{file} deleted.")
            except FileNotFoundError:
                print(f"{file} does not exist.")
            except Exception as e:
                print(f"Error deleting {file}: {e}")
        else:
            print(f"{file} not deleted.")

        print("\nBeendet durch Benutzer (Strg + C).")

if __name__ == '__main__':
    main()