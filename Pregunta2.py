import socket
import tkinter as tk
from datetime import datetime

# Configuración del servidor
HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 12345        # Puerto del servidor

# Función para procesar la cadena de entrada
def procesar_cadena(cadena):
    try:
        codigo_pais = int(cadena[:2])
        categoria_edad = int(cadena[2:4])
        genero = cadena[4]
        fecha_nacimiento = datetime.strptime(cadena[5:13], '%Y%m%d')
        nombre_completo = cadena[13:]

        # Validación de datos
        if codigo_pais == 1:
            pais = 'Honduras'
        elif codigo_pais == 2:
            pais = 'Costa Rica'
        elif codigo_pais == 3:
            pais = 'México'
        else:
            pais = 'País Desconocido'

        if 1 <= categoria_edad <= 18:
            categoria = 'Menor de Edad'
        elif 19 <= categoria_edad <= 50:
            categoria = 'Adulto'
        else:
            categoria = 'Tercera Edad'

        if genero == 'M':
            genero_texto = 'Masculino'
        elif genero == 'F':
            genero_texto = 'Femenino'
        else:
            genero_texto = 'Género Desconocido'

        # Cálculo de la edad
        hoy = datetime.now()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        # Creación de la respuesta
        respuesta = f"Hola {nombre_completo}, veo que eres del país de {pais} y tienes {edad} años, lo que indica que eres {categoria}."
        respuesta += f" Sin embargo, al observar tu fecha de nacimiento ({fecha_nacimiento.strftime('%d-%m-%Y')}), noto que la edad no concuerda con la fecha de nacimiento."

        return respuesta
    except Exception as e:
        return f"Error al procesar la cadena: {str(e)}"

# Creación del socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Servidor escuchando en {HOST}:{PORT}")

    # Aceptar conexiones entrantes
    conn, addr = server_socket.accept()
    with conn:
        print(f"Conexión establecida desde {addr}")

        # Recibir datos
        data = conn.recv(1024).decode('utf-8')
        print(f"Datos recibidos: {data}")

        # Procesar cadena
        respuesta = procesar_cadena(data)

        # Mostrar respuesta en una ventana tkinter
        root = tk.Tk()
        root.title("Respuesta del Servidor")
        tk.Label(root, text=respuesta, padx=20, pady=20).pack()
        root.mainloop()
