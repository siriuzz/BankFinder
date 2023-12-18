import psycopg2

# Configuración de la conexión
db_params = {
    'dbname': 'bankfinder',
    'user': 'jamal',
    'password': '12345',
    'host': 'localhost',  # Cambia esto según tu configuración
    'port': 5432,         # Puerto predeterminado de PostgreSQL
}

connection = None

# Intenta establecer la conexión
try:
    connection = psycopg2.connect(**db_params)
    print("Conexión exitosa!")

    # Aquí puedes realizar operaciones en la base de datos

except psycopg2.Error as e:
    print(f"Error al conectar a la base de datos: {e}")

finally:
    # Cierra la conexión, independientemente de si ha tenido éxito o no
    if connection:
        connection.close()
        print("Conexión cerrada.")
