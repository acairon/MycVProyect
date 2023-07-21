let tables = [];
let relationships = [];

function addTable() {
    const tableName = document.getElementById("table-name").value;
    if (tableName) {
        tables.push({ name: tableName, attributes: [] });
        updateTablesList();
        updateTableSelects();
    }
}

function updateTablesList() {
    const tablesList = document.getElementById("table-list");
    tablesList.innerHTML = "";
    tables.forEach(table => {
        const li = document.createElement("li");
        li.textContent = table.name;
        tablesList.appendChild(li);
    });
}

function updateTableSelects() {
    const tableSelect = document.getElementById("table-select");
    const table1Select = document.getElementById("table1-select");
    const table2Select = document.getElementById("table2-select");

    tableSelect.innerHTML = "<option value='' disabled selected>Seleccione una tabla</option>";
    table1Select.innerHTML = "<option value='' disabled selected>Seleccione una tabla</option>";
    table2Select.innerHTML = "<option value='' disabled selected>Seleccione una tabla</option>";

    tables.forEach(table => {
        const option = document.createElement("option");
        option.textContent = table.name;
        option.value = table.name;

        tableSelect.appendChild(option);
        table1Select.appendChild(option.cloneNode(true));
        table2Select.appendChild(option.cloneNode(true));
    });
}

function addAttribute() {
    const tableName = document.getElementById("table-select").value;
    const attributeName = document.getElementById("attribute-name").value;
    const attributeType = document.getElementById("attribute-type").value;
    if (tableName && attributeName) {
        const table = tables.find(table => table.name === tableName);
        if (table) {
            table.attributes.push({ name: attributeName, type: attributeType });
            updateAttributes();
        }
    }
}

function updateAttributes() {
    const tableName = document.getElementById("table-select").value;
    const table = tables.find(table => table.name === tableName);
    if (table) {
        const attributesList = document.getElementById("attribute-list");
        attributesList.innerHTML = "";
        table.attributes.forEach(attr => {
            const li = document.createElement("li");
            li.textContent = `${attr.name} ${attr.type}`;
            attributesList.appendChild(li);
        });
    }
}

function updateAttributeSelect() {
    const tableName = document.getElementById("table2-select").value;
    const table = tables.find(table => table.name === tableName);
    if (table) {
        const attributeSelect = document.getElementById("attribute-select");
        attributeSelect.innerHTML = "<option value='' disabled selected>Seleccione un atributo</option>";

        table.attributes.forEach(attr => {
            const option = document.createElement("option");
            option.textContent = attr.name;
            option.value = attr.name;
            attributeSelect.appendChild(option);
        });
    }
}

function addRelationship() {
    const table1 = document.getElementById("table1-select").value;
    const degree1 = document.getElementById("degree1-select").value;
    const table2 = document.getElementById("table2-select").value;
    const degree2 = document.getElementById("degree2-select").value;
    const attribute = document.getElementById("attribute-select").value;
    if (table1 && degree1 && table2 && degree2 && attribute) {
        relationships.push({ table1, degree1, table2, degree2, attribute });
        updateRelationshipsList();
    }
}

function updateRelationshipsList() {
    const relationshipsList = document.getElementById("relationship-list");
    relationshipsList.innerHTML = "";
    relationships.forEach(relationship => {
        const li = document.createElement("li");
        li.textContent = `${relationship.table1} ${relationship.degree1}--${relationship.degree2} ${relationship.table2} : ${relationship.attribute}`;
        relationshipsList.appendChild(li);
    });
}

function generateMermaidCode() {
    let mermaidCode = "erDiagram\n";
    relationships.forEach(relationship => {
        mermaidCode += `${relationship.table1} ${relationship.degree1}--${relationship.degree2} ${relationship.table2} : "${relationship.attribute}"\n`;
    });
    tables.forEach(table => {
        mermaidCode += `${table.name} {\n`;
        table.attributes.forEach(attr => {
            mermaidCode += `  ${attr.name} ${attr.type}\n`;
        });
        mermaidCode += "}\n";
    });
    document.getElementById("mermaid-code").textContent = mermaidCode;
}