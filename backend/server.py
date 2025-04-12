from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS  # Import CORS from flask_cors


app = Flask(__name__)
CORS(app)  # This will allow all domains to access your server

# MySQL connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'svcr-db'
}

@app.route('/tables', methods=['GET'])
def get_table_data():
    try:
        query = request.args.get('query')

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        result = {}

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
        except Exception as e:
            print(e)

        cursor.close()
        connection.close()

        return jsonify(result)

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
