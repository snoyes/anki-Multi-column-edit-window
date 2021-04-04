
/**Number of columns in the UI */
var numberOfColumns = 1;
var shortcut_full_line;
/** 
The indices of fields that takes a full line
*/
var fullLineFields = [];
const fieldsElements = new Map();

function setColumnCount(n) {
    numberOfColumns = n;
}
function setFullLineFields(field) {
    fullLineFields.push(field);
}
function resetFullLineFields(field) {
    fullLineFields = [];
}
function onMultipleLine(ord) {
    const msg = "MCEW:" + ord;
    pycmd(msg);
}


function longField(fieldName) {
    return fullLineFields.indexOf(fieldName) >= 0;
}

function adjustFieldAmount(fields) {
    amount = fields.length;
    const fieldsContainer = document.getElementById("fields");
    if (fieldsContainer == null) {
        return;
    }

    while (fieldsContainer.childElementCount > 0) {
        fieldsContainer.removeChild(fieldsContainer.lastElementChild);
    }

    const table = document.createElement("table");
    table.className += " mceTable"
    fieldsContainer.appendChild(table);
    let current_line = document.createElement("tr");
    for (var ord = 0; ord < amount; ord++) {
        var fieldName = fields[ord][0];
        let field_ord, title;
        if (fieldsElements.has(ord)) {
            field_ord = fieldsElements.get(ord);
        } else {
            field_ord = document.createElement("div", {
                is: "anki-editor-field",
            });
            field_ord.ord = ord;
            const link = document.createElement("a");
            const ord_copy = ord;
            link.onclick = () => onMultipleLine(ord_copy);
            link.title = `title`;
            link.appendChild(document.createTextNode("--"));
            link.id = `MCEW_${ord}`;
            labelContainer = field_ord.labelContainer;
            labelContainer.appendChild(document.createTextNode(" "))
            labelContainer.appendChild(link)
            fieldsElements.set(ord, field_ord);
        }
        const td = document.createElement("td");
        td.appendChild(field_ord)
        const is_long = longField(fieldName);
        if (is_long) {
            const line = document.createElement("tr");
            td.colSpan = numberOfColumns;
            line.appendChild(td);
            table.appendChild(line);
            title = "Smaller";
            link_text = "»-«";
        } else {
            td.colSpan = 1;
            current_line.appendChild(td);
            title = "Bigger";
            link_text = "«-»";
            if (current_line.childElementCount >= numberOfColumns) {
                table.appendChild(current_line);
                current_line = document.createElement("tr")
            }
        }        
    }
    if (current_line.childElementCount > 0) {
        table.appendChild(current_line);
        current_line = document.createElement("tr")
    }
}


function forEditorField(
    values,
    func
) {
    for (let ord = 0; ord < values.length; ord++) {
        const fieldElement = fieldsElements.get(ord);
        const value = values[ord];
        func(fieldElement, value, ord);
    }
}

function getEditorField(n) {
    if (n >= numberOfColumns) {
        return null;
    } else {
        return fieldsElements.get(n);
    }
}

// Literal copies
// editor/toolbar.ts

const highlightButtons = ["bold", "italic", "underline", "superscript", "subscript"];

function clearButtonHighlight() {
    for (const name of highlightButtons) {
        const elem = document.querySelector(`#${name}`);
        elem.classList.remove("highlighted");
    }
}

function disableButtons() {
    const buttons = document.querySelectorAll(
        "button.linkb:not(.perm)"
    );
    buttons.forEach((elem) => {
        elem.disabled = true;
    });
    clearButtonHighlight();
}

function setFields(fields) {
    // webengine will include the variable after enter+backspace
    // if we don't convert it to a literal colour
    const color = window
        .getComputedStyle(document.documentElement)
        .getPropertyValue("--text-fg");

    adjustFieldAmount(fields);
    forEditorField(
        fields,
        (field, [fieldName, fieldContent], ord) => {
            const is_long = longField(fieldName);
            const title_start = (is_long) ? "Smaller" : "Bigger";
            const id = `MCEW_${ord}`;
            const link = document.getElementById(id);
            // link.title = `${title_start} field (${shortcut_full_line})`;
            link.textContent = (is_long) ? "»-«" : "«-»" ;
            field.initialize(fieldName, color, fieldContent);
        }
    );
    

    if (!getCurrentField()) {
        // when initial focus of the window is not on editor (e.g. browser)
        disableButtons();
    }
}

function setBackgrounds(cols) {
    forEditorField(cols, (field, value, ord) =>
        field.editingArea.classList.toggle("dupe", value === "dupe")
    );
    dupes = document
        .getElementById("dupes");
    if (dupes == null) {
        return;
    }
    dupes.classList.toggle("is-inactive", !cols.includes("dupe"));
}

function setFonts(fonts) {
    forEditorField(fonts, (field, [fontFamily, fontSize, isRtl], ord) => {
        field.setBaseStyling(fontFamily, `${fontSize}px`, isRtl ? "rtl" : "ltr");
    });
}


function focusField(n) {
    const field = getEditorField(n);

    if (field) {
        field.editingArea.focusEditable();
        caretToEnd(field.editingArea);
        updateButtonState();
    }
}

function caretToEnd(currentField) {
    const range = document.createRange();
    range.selectNodeContents(currentField.editable);
    range.collapse(false);
    const selection = currentField.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
}

function updateButtonState() {
    for (const name of highlightButtons) {
        const elem = document.querySelector(`#${name}`);
        elem.classList.toggle("highlighted", document.queryCommandState(name));
    }

    // fixme: forecolor
    //    'col': document.queryCommandValue("forecolor")
}
