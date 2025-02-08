import os

class ASDDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.create_database(db_name)

    def create_database(self, name):
        if not os.path.exists(name):
            os.makedirs(name)
        print(f"Database '{name}' creato con successo.")

    def create_table(self, table_name, columns):
        table_path = os.path.join(self.db_name, f"{table_name}.asd")
        if not os.path.exists(table_path):
            with open(table_path, 'w') as f:
                f.write('|'.join(columns) + '\n')
            print(f"Tabella '{table_name}' creata con colonne {columns}.")
        else:
            print(f"La tabella '{table_name}' esiste già.")

    def insertdata(self, data, table_name):
        table_path = os.path.join(self.db_name, f"{table_name}.asd")
        if os.path.exists(table_path):
            with open(table_path, 'a') as f:
                f.write('|'.join(map(str, data)) + '\n')
            print(f"Dati {data} inseriti nella tabella '{table_name}'.")
        else:
            print(f"Errore: La tabella '{table_name}' non esiste.")

    def read(self, table_name, row):
        table_path = os.path.join(self.db_name, f"{table_name}.asd")
        if os.path.exists(table_path):
            with open(table_path, 'r') as f:
                lines = f.readlines()
                if row < len(lines):
                    return lines[row].strip().split('|')
                else:
                    print(f"Errore: La riga {row} non esiste nella tabella '{table_name}'.")
        else:
            print(f"Errore: La tabella '{table_name}' non esiste.")

