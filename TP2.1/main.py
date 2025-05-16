import requests
import mysql.connector
import json

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "trabajo2",
}

def fetch_country_data(code):
    url = f"https://restcountries.com/v3.1/alpha/{code}"
    response = requests.get(url)
    print("response: " + response)
    
    if response.status_code != 200:
        return None 

    data = response.json()

    if not data:
        return None  

    country = data[0]

    return {
        "codigoPais": country.get("ccn3", ""),
        "nombrePais": country.get("name", {}).get("common", ""),
        "capitalPais": country.get("capital", [""])[0] if "capital" in country else "",
        "region": country.get("region", ""),
        "subregion": country.get("subregion", ""),
        "poblacion": country.get("population", 0),
        "latitud": country.get("latlng", [0.0, 0.0])[0],
        "longitud": country.get("latlng", [0.0, 0.0])[1],
    }

def main():
    print("Ejecutando main()...")  # <-- Prueba si se ejecuta
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print('prueba2')
        cursor = conn.cursor()
        print('prueba3')
        for code in range(100, 1000):
            country_data = fetch_country_data(code)
            if not country_data:
                continue 

            codigoPais = country_data["codigoPais"]
            cursor.execute("SELECT COUNT(*) FROM paises2 WHERE codigoPais = %s", (codigoPais,))
            existePais = cursor.fetchone()[0] > 0

            if existePais:
                cursor.execute("""
                    UPDATE paises2 
                    SET nombrePais = %s, capitalPais = %s, region = %s, subregion = %s, 
                        poblacion = %s, latitud = %s, longitud = %s 
                    WHERE codigoPais = %s
                """, (
                    country_data["nombrePais"], country_data["capitalPais"], country_data["region"],
                    country_data["subregion"], country_data["poblacion"], 
                    country_data["latitud"], country_data["longitud"], codigoPais
                ))
            else:
                cursor.execute("""
                    INSERT INTO paises2 (codigoPais, nombrePais, capitalPais, region, subregion, poblacion, latitud, longitud) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    codigoPais, country_data["nombrePais"], country_data["capitalPais"], country_data["region"],
                    country_data["subregion"], country_data["poblacion"], 
                    country_data["latitud"], country_data["longitud"]
                ))

            conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    print("Ejecutando script...")
    main()