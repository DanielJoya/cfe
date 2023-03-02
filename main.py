from crawlers import get_prices
import sqlite3

PDBT_LINK = "https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRENegocio/Tarifas/PequenaDemandaBT.aspx"
GDBT_LINK = "https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRENegocio/Tarifas/GranDemandaBT.aspx"

# Identifiers and xpath definitions:
ids = {
    "year": "ContentPlaceHolder1_Fecha_ddAnio",
    "month": "ContentPlaceHolder1_Fecha2_ddMes",
    "state": "ContentPlaceHolder1_EdoMpoDiv_ddEstado",
    "town": "ContentPlaceHolder1_EdoMpoDiv_ddMunicipio",
    "division": "ContentPlaceHolder1_EdoMpoDiv_ddDivision",
    "table": '//*[@id="content"]/div/div[1]/div[2]/table[1]/tbody/tr[8]/td/table/tbody/tr[2]/td/table',
}


def main():
    create_database()
    get_prices(PDBT_LINK, "pdbt", ids)
    get_prices(GDBT_LINK, "gdbt", ids)


def create_database():

    conn = sqlite3.connect("prices.db")
    cur = conn.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS States (
            id INTEGER PRIMARY KEY, 
            state TEXT UNIQUE)"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS Towns (
            id INTEGER PRIMARY KEY, 
            state_id INTEGER, 
            town TEXT UNIQUE,
            FOREIGN KEY (state_id) REFERENCES States(id))"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS Divisions (
            id INTEGER PRIMARY KEY, 
            state_id INTEGER, 
            division TEXT UNIQUE,
            FOREIGN KEY (state_id) REFERENCES States(id))"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS Years (
            id INTEGER PRIMARY KEY, 
            year TEXT UNIQUE)"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS pdbt_fixed (
            state_id INTEGER,
            town_id INTEGER,
            division_id INTEGER,
            year_id INTEGER, 
            price REAL,
            FOREIGN KEY (state_id) REFERENCES States(id),
            FOREIGN KEY (town_id) REFERENCES Towns(id),
            FOREIGN KEY (division_id) REFERENCES Divisions(id),
            FOREIGN KEY (year_id) REFERENCES Years(id))"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS pdbt_variable (
            state_id INTEGER,
            town_id INTEGER,
            division_id INTEGER,
            year_id INTEGER, 
            price REAL,
            FOREIGN KEY (state_id) REFERENCES States(id),
            FOREIGN KEY (town_id) REFERENCES Towns(id),
            FOREIGN KEY (division_id) REFERENCES Divisions(id),
            FOREIGN KEY (year_id) REFERENCES Years(id))"""
    )

    return


main()

print("\n================================")
