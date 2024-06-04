import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Configurar a conexão com o SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=LAPTOP-VNP0UL09\SQLEXPRESS;'
                      'DATABASE=ArduinoData;'
                      'Trusted_Connection=yes;')

# Função para buscar dados do SQL Server
def fetch_data():
    query = "SELECT temperature, humidity, soilHumidity, luminosity, timestamp FROM SensorData ORDER BY timestamp DESC"
    df = pd.read_sql(query, conn)
    return df

# Função para atualizar os gráficos no dashboard
def update_dashboard():
    try:
        data = fetch_data()
        if not data.empty:
            # Limpar os eixos para atualizar os gráficos
            ax1.cla()
            ax2.cla()
            ax3.cla()
            ax4.cla()

            # Plotar os dados
            ax1.plot(data['timestamp'], data['temperature'], label='Temperature')
            ax2.plot(data['timestamp'], data['humidity'], label='Humidity')
            ax3.plot(data['timestamp'], data['soilHumidity'], label='Soil Humidity')
            ax4.plot(data['timestamp'], data['luminosity'], label='Luminosity')

            # Adicionar títulos e legendas
            ax1.set_title('Temperatura')
            ax2.set_title('umidade')
            ax3.set_title('Umidade do solo')
            ax4.set_title('Luminosidade')

            ax1.legend()
            ax2.legend()
            ax3.legend()
            ax4.legend()

            # Redesenhar os gráficos
            canvas.draw()
    except Exception as e:
        print(f"An error occurred: {e}")

    # Agendar a próxima atualização
    root.after(60000, update_dashboard)  # Atualiza a cada 60.000 milissegundos (1 minuto)

# Configurar a interface Tkinter
root = tk.Tk()
root.title("Real-time Data Dashboard")

# Configurar os gráficos com Matplotlib
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Iniciar a primeira atualização
update_dashboard()

# Iniciar a interface Tkinter
root.mainloop()