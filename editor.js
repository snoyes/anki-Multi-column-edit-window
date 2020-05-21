var columnCount = 1;
singleColspan = columnCount;
singleLine = [];
function setColumnCount(n) {
    columnCount = n;
}
function setSingleLine(field) {
    singleLine.push(field);
}
function resetSingleLine(field) {
    singleLine = [];
}
function onMultipleLine(ord) {
    pycmd("MCEW:" + ord);
}
function setFields(fields) {
    var txt = "";
    var titles_line = "";
    var fields_line = "";
    var nb_fields_in_line = 0;
    for (var i = 0; i < fields.length; i++) {
        var n = fields[i][0];
        var f = fields[i][1];
        if (!f) {
            f = "<br>";
        }
        if (singleLine.indexOf(n) >= 0) {
            txt += `
        <tr>
            <td class=fname id="name${i}" colspan=${columnCount}>
              <a onclick="onMultipleLine('${i}')" title="Smaller field (${shortcut_full_line})">
                &raquo;-&laquo;
              </a>
              ${n}
            </td>
        </tr>
        <tr>
            <td width=100% colspan=${columnCount}>
                <div id=f${i}
                     onkeydown='onKey(window.event);'
                     oninput='onInput();'
                     onmouseup='onKey(window.event);'
                     onfocus='onFocus(this);'
                     onblur='onBlur();'
                     class='field clearfix'
                     ondragover='onDragOver(this);'
                     onpaste='onPaste(this);'
                     oncopy='onCutOrCopy(this);'
                     oncut='onCutOrCopy(this);'
                     contentEditable=true
                     class=field
                >${f}</div>
            </td>
        </tr>`;
        } else {
            nb_fields_in_line +=1;
            titles_line += `
            <td class=fname id="name${i}">
              <a onclick="onMultipleLine(${i})" title="Bigger field (${shortcut_full_line})">
                &laquo;-&raquo;
              </a>
              ${n}
            </td>`;
            fields_line += `
            <td width=100%>
                <div id=f${i}
                     onkeydown='onKey(window.event);'
                     oninput='onInput();'
                     onmouseup='onKey(window.event);'
                     onfocus='onFocus(this);'
                     onblur='onBlur();'
                     class='field clearfix'
                     ondragover='onDragOver(this);'
                     onpaste='onPaste(this);'
                     oncopy='onCutOrCopy(this);'
                     oncut='onCutOrCopy(this);'
                     contentEditable=true
                     class=field
                >${f}</div>
            </td>`;
            if (nb_fields_in_line == columnCount) {
                nb_fields_in_line = 0;
                txt += `
        <tr>
${titles_line}
        </tr>
        <tr>
${fields_line}
        </tr>`;
                titles_line = "";
                fields_line = "";
            }
        }
    }
    if (nb_fields_in_line > 0) {
        txt += `
        <tr>
${titles_line}
        </tr>
        <tr>
${fields_line}
        </tr>`;
    }
    $("#fields").html(`
    <table class=mceTable cellpadding=0 width=100% style='table-layout: fixed;'>
${txt}
    </table>`);
    maybeDisableButtons();
}
