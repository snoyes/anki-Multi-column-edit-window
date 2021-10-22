
/**Number of columns in the UI */
var numberOfColumns = 1;
var shortcut_full_line;
/** 
The indices of fields that takes a full line
*/
var fullLineFields = [];
var stickyFields = [];
const fieldsElements = new Map();
let pin_src;

function setColumnCount(n) {
    numberOfColumns = n;
}
function setFullLineFields(field) {
    fullLineFields.push(field);
}
function resetFullLineFields(field) {
    fullLineFields = [];
}
function setStickyFields(field) {
    stickyFields.push(field);
}
function setSticky() {
    // allow to cancel the default setSticky
}
    stickyFields = [];
function resetStickyFields(field) {
}
function onMultipleLine(ord) {
    pycmd(`MCEW_line:${ord}`);
}
function onSticky(ord, name) {
    const index = stickyFields.findIndex((arg) => arg == name);
    const was_sticky = index >= 0;
    if (was_sticky) {
        stickyFields.splice(index, 1);
    } else {
        stickyFields.push(name);
    }
    document.getElementById(`sticky_{ord}`).classList.toggle("is-inactive", was_sticky);
    pycmd(`MCEW_sticky:${ord}`);
}


function longField(fieldName) {
    return fullLineFields.indexOf(fieldName) >= 0;
}
function stickyField(fieldName) {
    return stickyFields.indexOf(fieldName) >= 0;
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
        const fieldName = fields[ord][0];
        let field_ord, title;
        const is_sticky = stickyField(fieldName);
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

            const sticky = document.createElement("img");
            sticky.id = `sticky_{ord}` ;
            sticky.src = pin_src;
            labelContainer.appendChild(sticky);
            sticky.onclick = () => onSticky(ord_copy, fieldName);
            sticky.classList.toggle("is-inactive", !is_sticky);
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
            link.title = `${title_start} field (${shortcut_full_line})`;
            link.textContent = (is_long) ? "»-«" : "«-»" ;
            field.initialize(fieldName, color, fieldContent);
        }
    );
}

// Literal copies
// editor/toolbar.ts

function setBackgrounds(cols) {
    forEditorField(cols, (field, value, ord) =>
        field.editingArea.classList.toggle("dupe", value === "dupe")
    );
    dupes = document
        .getElementById("dupes");
    if (dupes == null) {
        return;
    }
    dupes.classList.toggle("d-none", !cols.includes("dupe"));
}

function setFonts(fonts) {
    forEditorField(fonts, (field, [fontFamily, fontSize, isRtl], ord) => {
        field.setBaseStyling(fontFamily, `${fontSize}px`, isRtl ? "rtl" : "ltr");
    });
}


function focusField(n) {
    const field = getEditorField(n);

    if (field) {
        field.editingArea.focus();
        field.editingArea.caretToEnd();
    }
}

function updateButtonState() {
    for (const name of highlightButtons) {
        const elem = document.querySelector(`#${name}`);
        elem.classList.toggle("highlighted", document.queryCommandState(name));
    }

    // fixme: forecolor
    //    'col': document.queryCommandValue("forecolor")
}
