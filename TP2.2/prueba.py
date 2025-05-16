
import requests
from pymongo import MongoClient

# Configuración de MongoDB
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "paises_db"
COLLECTION_NAME = "paises"

def fetch_country_data(code):
    """Obtiene los datos del país desde la API."""
    url = f"https://restcountries.com/v3.1/alpha/{code}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error en código {code}: {response.status_code}")
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
    """Función principal que obtiene datos y actualiza la base de datos en MongoDB."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        for code in range(100, 200):
            country_data = fetch_country_data(code)
            if not country_data:
                continue

            codigoPais = country_data["codigoPais"]
            existing_country = collection.find_one({"codigoPais": codigoPais})

            if existing_country:
                collection.update_one(
                    {"codigoPais": codigoPais},
                    {"$set": country_data}
                )
            else:
                collection.insert_one(country_data)
        
        print("Proceso completado.")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()