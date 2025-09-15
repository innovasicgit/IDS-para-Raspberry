from sqlalchemy import create_engine
import socket
import random
import time
import json
import threading
import pandas as pd
import numpy as np

PORT = 8889
IP = "10.42.65.126"

def handler(client_soc):
    client_soc.send(b"b")
    print("Peticion enviada")
    time.sleep(20)
    global df

    try:
        data = client_soc.recv(65536).decode()
        #print(data, "\n")
        if len(data) > 4:
            j = json.loads(data)
            print("datos recibidos")
            # Agregar fecha y hora actual al JSON
            j["time"] = pd.to_datetime('now')

            # Actualizar DataFrame global
            df = pd.concat([df, pd.DataFrame([j])], ignore_index=True)
            df2 = pd.DataFrame([j])
            df2 = df2.rename(columns={
                'Device': 'device',
                'IP': 'ip',
                'LUX': 'lux',
                'NH3': 'nh3',
                'HS': 'hs',
                'H': 'h',
                'T': 't',
                'time': 'time'
            })
            
            # Convertir la columna 'time' a tipo datetime
            df2['time'] = pd.to_datetime(df2['time'])
            condicion = df2['time'].apply(lambda x: x.minute % 5 == 0 and 0 <= x.second <= 10)

            # Filtrar el DataFrame usando la condición
            df2_filtrado = df2[condicion]

            # Guardar DataFrame en un archivo Excel
            df.to_excel("data_test_15.xlsx", sheet_name='sheet1', index=False)

            # Generar datos de prueba
            random_lux = random.uniform(110.0, 200.0)
            random_nh3 = random.uniform(5.0, 15.0)
            random_hs = random.uniform(40.0, 310.0)
            random_h = random.uniform(60.0, 80.0)
            random_t = random.uniform(20.0, 40.0)

            # Extraer los primeros valores de df2 para evitar pasar Series
            device_value = df2['device'].values[0]
            ip_value = df2['ip'].values[0]
            time_value = df2['time'].values[0]

            # Crear DataFrame de prueba
            df_test = pd.DataFrame({
                'device': [device_value],
                'ip': [ip_value],
                'lux': [random_lux],
                'nh3': [random_nh3],
                'hs': [random_hs],
                'h': [random_h],
                't': [random_t],
                'time': [time_value]
            })
            df_test['time'] = df_test['time'].apply(lambda t: t.replace(microsecond=0))

            
            condicion_test = df_test['time'].apply(lambda x: x.minute % 5 == 0 and 0 <= x.second <= 10)

            # Filtrar el DataFrame usando la condición
            df_test_filtrado = df_test[condicion_test]
            
            

            print("=== VALORES ===")
            print(df_test.head())


            
            column_order = ['ip', 'device', 'lux', 'nh3', 'hs', 'h', 't', 'time']
            df_test_filtrado = df_test_filtrado[column_order]



            # Enviar datos a la base de datos
            send_to_db(df_test_filtrado)

    except Exception as e:
        print(e)
    
    client_soc.close()

def send_to_db(df):
    # Conexión a la base de datos PostgreSQL
    engine = create_engine('postgresql+psycopg2://alex:123@localhost:5432/granja')
    
    # Insertar datos en la tabla 'sensors3'
    df.to_sql('sensors3', engine, if_exists='append', index=False)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global df
    df = pd.DataFrame()
    
    with s:
        s.bind((IP, PORT))
        s.listen(True)
        while True:
            client_soc, client_address = s.accept()
            client_soc.settimeout(25)
            threading.Thread(target=handler, args=(client_soc,), daemon=True).start()

if __name__ == "__main__": 
    print("Servidor ON")
    main()
