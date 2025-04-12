from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'svcr-db'
}

@app.route('/tables', methods=['POST'])
def get_table_data():
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({'error': 'Expected JSON object with table names and column lists'}), 400

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        result = {}

        for table, columns in data.items():
            col_str = ", ".join(f"`{col}`" for col in columns)
            query = f"SELECT {col_str} FROM `{table}`;"
            cursor.execute(query)
            result[table] = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(result)

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
