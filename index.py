import sqlite3

# Función para obtener las tablas y sus columnas de una base de datos
def get_tables_and_columns(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Obtener todas las tablas en la base de datos
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    table_columns = {}
    
    # Para cada tabla, obtener las columnas
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        # Guardamos el nombre de la columna y su tipo de dato
        table_columns[table_name] = [(col[1], col[2]) for col in columns]
    
    conn.close()
    return table_columns

# Función para comparar las tablas y columnas entre dos bases de datos
def compare_databases(db1_path, db2_path, output_path):
    db1_tables = get_tables_and_columns(db1_path)
    db2_tables = get_tables_and_columns(db2_path)
    
    with open(output_path, 'w') as file:
        file.write("Comparación entre bases de datos\n")
        file.write(f"DB1: {db1_path}\n")
        file.write(f"DB2: {db2_path}\n\n")

        # Comparar tablas
        db1_table_set = set(db1_tables.keys())
        db2_table_set = set(db2_tables.keys())
        
        only_in_db1 = db1_table_set - db2_table_set
        only_in_db2 = db2_table_set - db1_table_set
        common_tables = db1_table_set & db2_table_set
        
        # Tablas que están solo en DB1
        if only_in_db1:
            file.write("Tablas solo en DB1:\n")
            for table in only_in_db1:
                file.write(f"  - {table}\n")
            file.write("\n")
        
        # Tablas que están solo en DB2
        if only_in_db2:
            file.write("Tablas solo en DB2:\n")
            for table in only_in_db2:
                file.write(f"  - {table}\n")
            file.write("\n")
        
        # Comparar las columnas de las tablas en común
        if common_tables:
            file.write("Tablas en común con diferencias en columnas:\n")
            for table in common_tables:
                db1_columns = set(db1_tables[table])
                db2_columns = set(db2_tables[table])
                
                only_in_db1_columns = db1_columns - db2_columns
                only_in_db2_columns = db2_columns - db1_columns
                
                if only_in_db1_columns or only_in_db2_columns:
                    file.write(f"Tabla: {table}\n")
                    
                    if only_in_db1_columns:
                        file.write("  Columnas solo en DB1:\n")
                        for column in only_in_db1_columns:
                            file.write(f"    - {column[0]} ({column[1]})\n")
                    
                    if only_in_db2_columns:
                        file.write("  Columnas solo en DB2:\n")
                        for column in only_in_db2_columns:
                            file.write(f"    - {column[0]} ({column[1]})\n")
                    file.write("\n")
                    
        file.write("Comparación finalizada.\n")

# Rutas a las bases de datos
db1_path = r'C:\Users\Arvey_Saavedra\Downloads\AMOVILBDF17(clean)-pru.db'
db2_path = r'C:\Users\Arvey_Saavedra\Downloads\AMOVILBDF17(clean)-prod.db'

# Ruta donde guardar el archivo de diferencias
output_path = r'C:\Users\Arvey_Saavedra\Downloads\diferencias.txt'

# Ejecutar la comparación
compare_databases(db1_path, db2_path, output_path)

print(f"Diferencias guardadas en: {output_path}")

