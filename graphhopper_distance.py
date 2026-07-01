import requests
import json


API_KEY = "2b341399-b4ad-4695-8960-730b012b11d4"

def geocode(ciudad):
    """Obtiene latitud y longitud de una ciudad usando GraphHopper Geocoding."""
    url = f"https://graphhopper.com/api/1/geocode?q={ciudad}&key={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['hits']:
            hit = data['hits'][0]
            return hit['point']['lat'], hit['point']['lng']
    except Exception as e:
        print(f"Error en geocodificación: {e}")
    return None, None

def calcular_ruta(origen, destino, perfil="car"):
    """Calcula la ruta entre dos puntos usando GraphHopper Routing."""
    lat1, lng1 = geocode(origen)
    lat2, lng2 = geocode(destino)
    if None in (lat1, lng1, lat2, lng2):
        return None
    
    url = f"https://graphhopper.com/api/1/route?point={lat1},{lng1}&point={lat2},{lng2}&vehicle={perfil}&key={API_KEY}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error en la ruta: {e}")
        return None

def mostrar_resultado(resultado, origen, destino, perfil):
    """Procesa y muestra la información de la ruta."""
    if not resultado or 'paths' not in resultado:
        print("No se pudo calcular la ruta. Verifica los nombres de las ciudades.")
        return
    
    path = resultado['paths'][0]
    distancia_metros = path['distance']
    distancia_km = distancia_metros / 1000
    distancia_millas = distancia_km * 0.621371
    tiempo_segundos = path['time'] / 1000
    horas = int(tiempo_segundos // 3600)
    minutos = int((tiempo_segundos % 3600) // 60)
    
    # Narrativa del viaje (más detallada)
    narrativa = (
        f"Viaje desde {origen} hasta {destino} en {perfil}.\n"
        f"Distancia: {distancia_km:.2f} km ({distancia_millas:.2f} millas)\n"
        f"Duración estimada: {horas}h {minutos}min"
    )
    
    print("\n" + "="*50)
    print("🚗 RESULTADO DEL VIAJE")
    print("="*50)
    print(f"📌 Origen: {origen}")
    print(f"📌 Destino: {destino}")
    print(f"🚲 Transporte: {perfil}")
    print(f"📏 Distancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
    print(f"⏱️ Duración: {horas}h {minutos}min")
    print(f"📝 Narrativa: {narrativa}")
    print("="*50)

def main():
    print("🛑 Para salir en cualquier momento, presiona 's' (sin comillas) y Enter.")
    
    while True:
        origen = input("\nCiudad de Origen (en español): ").strip()
        if origen.lower() == 's':
            print("Saliendo del programa...")
            break
        
        destino = input("Ciudad de Destino (en español): ").strip()
        if destino.lower() == 's':
            print("Saliendo del programa...")
            break
        
        print("\nTipos de transporte disponibles:")
        print("  - car     (auto)")
        print("  - bike    (bicicleta)")
        print("  - foot    (peatón)")
        perfil = input("Seleccione medio de transporte (o presione Enter para 'car'): ").strip().lower()
        if perfil == 's':
            print("Saliendo del programa...")
            break
        if perfil not in ['car', 'bike', 'foot']:
            perfil = 'car'  # Valor por defecto
        
        resultado = calcular_ruta(origen, destino, perfil)
        mostrar_resultado(resultado, origen, destino, perfil)

if __name__ == "__main__":
    main()