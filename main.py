import tkinter as tk
from tkinter import ttk

class Table:
    def __init__(self, name):
        self.name = name
        self.attributes = []

class EntityRelationshipDiagramGenerator:
    def __init__(self):
        self.tables = []
        self.relationships = []

    def add_table(self, table_name):
        self.tables.append(Table(table_name))

    def add_attribute(self, table_name, attribute_name, attribute_type):
        for table in self.tables:
            if table.name == table_name:
                table.attributes.append((attribute_name, attribute_type))
                break

    def add_relationship(self, table1_name, degree1, table2_name, degree2, relationship_label):
        self.relationships.append((table1_name, degree1, table2_name, degree2, relationship_label))

    def generate_mermaid_code(self):
        mermaid_code = "erDiagram\n\n"

        for table in self.tables:
            mermaid_code += f"  {table.name} {{\n"
            for attribute in table.attributes:
                attribute_name, attribute_type = attribute
                mermaid_code += f"    {attribute_name} {attribute_type}\n"
            mermaid_code += "  }\n\n"

        for relationship in self.relationships:
            table1, degree1, table2, degree2, label = relationship
            mermaid_code += f"  {table1} {degree1}--{degree2} {table2} : {label}\n\n"

        return mermaid_code

class CreateTableDialog:
    def __init__(self, parent, generator, parent_app, table=None):
        self.parent = parent
        self.generator = generator
        self.parent_app = parent_app
        self.dialog = tk.Toplevel(parent)
        if table:
            self.dialog.title("Editar Tabla")
        else:
            self.dialog.title("Crear Nueva Tabla")

        self.table_name_label = tk.Label(self.dialog, text="Nombre de la tabla:")
        self.table_name_label.grid(row=0, column=0)
        self.table_name_entry = tk.Entry(self.dialog)
        self.table_name_entry.grid(row=0, column=1)

        self.add_attribute_button = tk.Button(self.dialog, text="Añadir Atributo", command=self.add_attribute)
        self.add_attribute_button.grid(row=0, column=2)

        self.save_button = tk.Button(self.dialog, text="Guardar", command=self.save_table)
        self.save_button.grid(row=0, column=3)

        self.attribute_frame = tk.Frame(self.dialog, padx=10, pady=10)
        self.attribute_frame.grid(row=1, columnspan=5)

        self.attribute_name_label = tk.Label(self.attribute_frame, text="Nombre del atributo")
        self.attribute_type_label = tk.Label(self.attribute_frame, text="Tipo de atributo")

        self.attribute_name_label.grid(row=0, column=0)
        self.attribute_type_label.grid(row=0, column=1)

        self.attribute_rows = []

        if table:
            self.table_name_entry.insert(0, table.name)
            for attribute in table.attributes:
                attribute_row = self.create_attribute_row()
                attribute_name_entry, attribute_type_combobox = attribute_row
                attribute_name_entry.insert(0, attribute[0])
                attribute_type_combobox.set(attribute[1])

    def add_attribute(self):
        attribute_row = self.create_attribute_row()
        self.attribute_rows.append(attribute_row)

    def create_attribute_row(self):
        attribute_row = []

        attribute_name_entry = tk.Entry(self.attribute_frame)
        attribute_name_entry.grid(row=len(self.attribute_rows) + 1, column=0)

        attribute_type_combobox = ttk.Combobox(self.attribute_frame, values=["number", "varchar"], state="readonly")
        attribute_type_combobox.grid(row=len(self.attribute_rows) + 1, column=1)

        attribute_row.extend([attribute_name_entry, attribute_type_combobox])

        return attribute_row

    def save_table(self):
        table_name = self.table_name_entry.get()
        if table_name:
            self.generator.add_table(table_name)
            for attribute_row in self.attribute_rows:
                attribute_name = attribute_row[0].get()
                attribute_type = attribute_row[1].get()
                if attribute_name:
                    self.generator.add_attribute(table_name, attribute_name, attribute_type)
            self.parent_app.update_tables_list()
            self.parent_app.update_table_elements()
            self.dialog.destroy()

class SetRelationshipDialog:
    def __init__(self, parent, generator, parent_app):
        self.parent = parent
        self.generator = generator
        self.parent_app = parent_app
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Establecer Relación")

        self.table1_label = tk.Label(self.dialog, text="Tabla 1:")
        self.table1_label.grid(row=0, column=0)
        self.table1_combobox = ttk.Combobox(self.dialog, values=[table.name for table in self.generator.tables])
        self.table1_combobox.grid(row=0, column=1)

        self.table2_label = tk.Label(self.dialog, text="Tabla 2:")
        self.table2_label.grid(row=0, column=2)
        self.table2_combobox = ttk.Combobox(self.dialog, values=[table.name for table in self.generator.tables])
        self.table2_combobox.grid(row=0, column=3)

        self.degree1_label = tk.Label(self.dialog, text="Grado de Relación Tabla 1:")
        self.degree1_label.grid(row=1, column=0)
        self.degree1_combobox = ttk.Combobox(self.dialog, values=["|o", "||", "}o", "|}"])
        self.degree1_combobox.grid(row=1, column=1)

        self.degree2_label = tk.Label(self.dialog, text="Grado de Relación Tabla 2:")
        self.degree2_label.grid(row=1, column=2)
        self.degree2_combobox = ttk.Combobox(self.dialog, values=["o|", "||", "o{", "{|"])
        self.degree2_combobox.grid(row=1, column=3)

        self.relationship_label_label = tk.Label(self.dialog, text="Texto Relación:")
        self.relationship_label_label.grid(row=2, column=0)
        self.relationship_label_entry = tk.Entry(self.dialog)
        self.relationship_label_entry.grid(row=2, column=1, columnspan=3)

        self.save_button = tk.Button(self.dialog, text="Guardar", command=self.save_relationship)
        self.save_button.grid(row=3, column=0, columnspan=4)

    def save_relationship(self):
        table1 = self.table1_combobox.get()
        table2 = self.table2_combobox.get()
        degree1 = self.degree1_combobox.get()
        degree2 = self.degree2_combobox.get()
        relationship_label = self.relationship_label_entry.get()

        if table1 and table2 and degree1 and degree2 and relationship_label:
            self.generator.add_relationship(table1, degree1, table2, degree2, relationship_label)
            self.parent_app.update_table_elements()
            self.dialog.destroy()

class EntityRelationshipDiagramApp:
    def __init__(self, root):
        self.generator = EntityRelationshipDiagramGenerator()
        self.root = root
        self.root.title("Generador de Diagramas ER con Mermaid")

        self.table_frame = tk.Frame(self.root, padx=20, pady=20)
        self.table_frame.grid(row=0, column=0)

        self.create_table_button = tk.Button(self.table_frame, text="Crear Nueva Tabla", command=self.create_table_dialog)
        self.create_table_button.grid(row=0, column=0)

        self.create_relationship_button = tk.Button(self.table_frame, text="Establecer Relación", command=self.set_relationship_dialog)
        self.create_relationship_button.grid(row=1, column=0)

        self.table_elements_frame = tk.Frame(self.root, padx=20, pady=20)
        self.table_elements_frame.grid(row=0, column=1)

        self.table_elements = []

        self.generate_diagram_button = tk.Button(self.root, text="Generar Código Mermaid", command=self.generate_diagram)
        self.generate_diagram_button.grid(row=1, column=0, pady=10)

    def create_table_dialog(self, table=None):
        dialog = CreateTableDialog(self.root, self.generator, self, table=table)
        self.root.wait_window(dialog.dialog)

    def set_relationship_dialog(self):
        dialog = SetRelationshipDialog(self.root, self.generator, self)
        self.root.wait_window(dialog.dialog)

    def update_tables_list(self):
        pass

    def update_table_elements(self):
        for widget in self.table_elements_frame.winfo_children():
            widget.destroy()

        for table in self.generator.tables:
            table_element_frame = tk.Frame(self.table_elements_frame, padx=10, pady=10)
            table_element_frame.grid(row=len(self.table_elements), column=0)

            table_name_label = tk.Label(table_element_frame, text=table.name)
            table_name_label.grid(row=0, column=0)

            edit_button = tk.Button(table_element_frame, text="Editar", command=lambda table=table: self.edit_table(table))
            edit_button.grid(row=0, column=1)

            self.table_elements.append(table_element_frame)

    def edit_table(self, table):
        self.create_table_dialog(table)

    def generate_diagram(self):
        mermaid_code = self.generator.generate_mermaid_code()
        with open("diagram.mmd", "w") as file:
            file.write(mermaid_code)

        print("Código Mermaid generado y guardado en 'diagram.mmd'")

def main():
    root = tk.Tk()
    app = EntityRelationshipDiagramApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()