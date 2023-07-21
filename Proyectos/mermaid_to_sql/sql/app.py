import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ruta para generar consultas
@app.route('/generate_queries', methods=['POST'])
def generate_queries():
    try:
        mermaid_code = request.json['code']
        queries = generate_oracle_queries(mermaid_code)

        if queries:
            return jsonify({'queries': queries})
        else:
            return jsonify({'error': 'Error generando las consultas SQL'})
    except Exception as e:
        return jsonify({'error': f'Error generando las consultas SQL: {e}'})
# Ruta para generar enlaces de fotos subidas




# Método para poder extraer las relaciones del diagrama de mermaid
def extract_relation(mermaid_code):
    relation_pattern = r"(\w+)\s*[|\-o{}]+\s*(\w+)\s*:\s*\"(\w+)\""
    matches = re.findall(relation_pattern, mermaid_code)
    relations = []

    for match in matches:
        from_table = match[0]
        to_table = match[1]
        attribute = match[2]
        relations.append((from_table, to_table, attribute))

    return relations

def generate_oracle_queries(mermaid_code):
    try:
        table_pattern = r"(\w+)\s+{([\w\s\n\t\"\',]+)}"
        tables = re.findall(table_pattern, mermaid_code, re.MULTILINE)

        relations = extract_relation(mermaid_code)

        queries = []
        for table in tables:
            table_name = table[0]
            table_attributes = table[1].strip().split('\n')
            create_query = f"CREATE TABLE {table_name} (\n"
            create_query += "    ID NUMBER PRIMARY KEY,\n"

            for attribute in table_attributes:
                attribute = attribute.strip()
                if attribute:
                    attribute_parts = attribute.split(' ')
                    attribute_name = attribute_parts[0]
                    attribute_type = attribute_parts[1]

                    if len(attribute_parts) > 2:
                        comments = attribute_parts[2].strip("\"'")
                        if "NN" in comments:
                            create_query += f"    {attribute_name} {attribute_type} NOT NULL,\n"
                        else:
                            create_query += f"    {attribute_name} {attribute_type},\n"

                        if "AI" in comments:
                            sequence_query = f"CREATE SEQUENCE {table_name}_{attribute_name}_SEQ START WITH 1 INCREMENT BY 1;\n"
                            queries.append(sequence_query)
                    else:
                        create_query += f"    {attribute_name} {attribute_type},\n"

            create_query = create_query[:-2] + "\n);"
            queries.append(create_query)

        for relations in relations:
            from_table, to_table, attribute = relations
            constraint_type = "FOREIGN KEY"
            alter_query = f"ALTER TABLE {to_table} ADD CONSTRAINT {from_table}_{attribute}_FK {constraint_type} ({attribute}) REFERENCES {from_table}(ID);\n"
            queries.append(alter_query)

        return queries
    except Exception as e:
        print(f"Error generando las consultas SQL: {e}")
        return None

if __name__ == '__main__':
    app.run()
