from flask import Flask, request, jsonify
import json

app = Flask(__name__)

tables = []
relationships = []

class Table:
    def __init__(self, name):
        self.name = name
        self.attributes = []

class Relationship:
    def __init__(self, table1, degree1, table2, degree2, text):
        self.table1 = table1
        self.degree1 = degree1
        self.table2 = table2
        self.degree2 = degree2
        self.text = text

@app.route('/tables', methods=['POST'])
def add_table():
    data = request.get_json()
    table_name = data['name']
    table = Table(table_name)
    tables.append(table)
    return jsonify({"message": f"Table {table_name} added successfully."}), 201

@app.route('/tables', methods=['GET'])
def get_tables():
    table_names = [table.name for table in tables]
    return jsonify(table_names), 200

@app.route('/attributes', methods=['POST'])
def add_attribute():
    data = request.get_json()
    table_name = data['table']
    attribute_name = data['name']
    attribute_type = data['type']

    table = next((table for table in tables if table.name == table_name), None)
    if table:
        table.attributes.append({"name": attribute_name, "type": attribute_type})
        return jsonify({"message": f"Attribute {attribute_name} added to table {table_name} successfully."}), 201
    else:
        return jsonify({"error": f"Table {table_name} not found."}), 404

@app.route('/relationships', methods=['POST'])
def add_relationship():
    data = request.get_json()
    table1 = data['table1']
    degree1 = data['degree1']
    table2 = data['table2']
    degree2 = data['degree2']
    text = data['text']

    relationship = Relationship(table1, degree1, table2, degree2, text)
    relationships.append(relationship)
    return jsonify({"message": "Relationship added successfully."}), 201

@app.route('/code', methods=['GET'])
def generate_mermaid_code():
    mermaid_code = "erDiagram\n"
    for table in tables:
        mermaid_code += f"{table.name} {{\n"
        for attr in table.attributes:
            mermaid_code += f"  {attr['name']} {attr['type']}\n"
        mermaid_code += "}\n"
    for relationship in relationships:
        mermaid_code += f"{relationship.table1} {relationship.degree1}--{relationship.degree2} {relationship.table2} : {relationship.text}\n"

    return jsonify({"code": mermaid_code}), 200

if __name__ == '__main__':
    app.run(debug=True)