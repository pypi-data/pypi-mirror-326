## ASD DATABASE

A simple database for your projects.

# Install

```bash
pip install asd-database
```

# Usage
Here's a quick example to get you started:

```python
from asd_database import ASDDatabase

# Create a new database
db = ASDDatabase('my_database')

# Create a table with columns 'id', 'name', and 'email'
db.create_table('users', ['id', 'name', 'email'])

# Insert data into the table
db.insertdata([1, 'Mario Rossi', 'mario@example.com'], 'users')
db.insertdata([2, 'Luca Bianchi', 'luca@example.com'], 'users')

# Read the second row (header is row 0)
print(db.read('users', 2))
```

## File Structure
Each table is stored in a `.asd` file inside the database directory. The first row contains the column headers, and each subsequent row represents a data entry.

Example `users.asd` file:

```
id|name|email
1|Mario Rossi|mario@example.com
2|Luca Bianchi|luca@example.com
```

## API Reference

### `ASDDatabase(db_name)`
Creates or opens a database directory.

### `create_table(table_name, columns)`
Creates a new table with the specified columns.

**Parameters:**
- `table_name` (str): The name of the table.
- `columns` (list): A list of column names.

### `insertdata(data, table_name)`
Inserts a row of data into the specified table.

**Parameters:**
- `data` (list): A list of values corresponding to the table columns.
- `table_name` (str): The name of the table.

### `read(table_name, row)`
Reads a specific row from the specified table.

**Parameters:**
- `table_name` (str): The name of the table.
- `row` (int): The row number to read (header is row 0).

**Returns:**
- A list of values from the specified row.

## License

This project is licensed under the MIT License.
