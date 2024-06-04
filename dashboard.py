import serial
import pyodbc
import time


# Configuração da conexão serial (ajuste a porta conforme necessário)
ser = serial.Serial('COM6', 115200)  # Porta COM3 com baud rate 9600

# Configuração da conexão com o SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=LAPTOP-VNP0UL09\SQLEXPRESS;'
                      'DATABASE=ArduinoData;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

def insert_data(temperature, humidity, soil_humidity, luminosity):
    query = """
    INSERT INTO SensorData (temperature, humidity, soilHumidity, luminosity)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (temperature, humidity, soil_humidity, luminosity))
    conn.commit()

def process_line(line):
    parts = line.split(",")
    data = {}
    for part in parts:
        key, value = part.split(":")
        data[key.strip()] = float(value.strip())
    return data

def main():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            data = process_line(line)
            insert_data(
                data['Temperature'],
                data['Humidity'],
                int(data['SoilHumidity']),
                int(data['Luminosity'])
            )
            print("Data inserted:", data)
        time.sleep(5)  # Aguardar 60 segundos antes de ler novamente

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ser.close()
        cursor.close()
        conn.close()
        print("Conexões encerradas.")