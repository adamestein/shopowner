// Display errors in the Django style
function display_errors(error_obj) {
    for (var err in error_obj) {
        var container = document.getElementById(err + "_container");
        var error_ul = document.createElement("ul");

        error_ul.setAttribute("class", "errorlist");
        error_ul.innerHTML = "<li>" + error_obj[err] + "</li>";

        container.parentNode.insertBefore(error_ul, container);
    }
}

// Display error web page
function error_page(jqXHR, textStatus, errorThrown) {
    var text = jqXHR.responseText;

    if (text.search(/<head>/) == -1) {
        // Add CSS formatting since it's not there already

        // Pull out the web page title from the h1 tag
        h1 = new String(text.match("<h1>.*</h1>"));
        title = h1.slice(4, -5);

        if (title.length) {
            var pre = '<html lang="en"> ';
            pre += '<head> ';
            pre += '<meta http-equiv="content-type" content="text/html; charset=utf-8"> ';
            pre += '<meta name="robots" content="NONE,NOARCHIVE"> ';
            pre += '<title>' + title + '</title> ';
            pre += '<style type="text/css"> ';
            pre += 'html * { padding:0; margin:0; } ';
            pre += 'body * { padding:10px 20px; } ';
            pre += 'body * * { padding:0; } ';
            pre += 'body { font:small sans-serif; } ';
            pre += 'body>div { border-bottom:1px solid #ddd; } ';
            pre += 'h1 { font-weight:normal; } ';
            pre += 'h2 { margin-bottom:.8em; } ';
            pre += 'h2 span { font-size:80%%; color:#666; font-weight:normal; } ';
            pre += 'h3 { margin:1em 0 .5em 0; } ';
            pre += 'h4 { margin:0 0 .5em 0; font-weight: normal; } ';
            pre += 'table { border:1px solid #ccc; border-collapse: collapse; width:100%%; background:white; } ';
            pre += 'tbody td, tbody th { vertical-align:top; padding:2px 3px; } ';
            pre += 'thead th { padding:1px 6px 1px 3px; background:#fefefe; text-align:left; font-weight:normal; font-size:11px; border:1px solid #ddd; } ';
            pre += 'tbody th { width:12em; text-align:right; color:#666; padding-right:.5em; } ';
            pre += 'table.vars { margin:5px 0 2px 40px; } ';
            pre += 'table.vars td, table.req td { font-family:monospace; } ';
            pre += 'table td.code { width:100%%; } ';
            pre += 'table td.code div { overflow:hidden; } ';
            pre += 'table.source th { color:#666; } ';
            pre += 'table.source td { font-family:monospace; white-space:pre; border-bottom:1px solid #eee; } ';
            pre += 'ul.traceback { list-style-type:none; } ';
            pre += 'ul.traceback li.frame { margin-bottom:1em; } ';
            pre += 'div.context { margin: 10px 0; } ';
            pre += 'div.context ol { padding-left:30px; margin:0 10px; list-style-position: inside; } ';
            pre += 'div.context ol li { font-family:monospace; white-space:pre; color:#666; cursor:pointer; } ';
            pre += 'div.context ol.context-line li { color:black; background-color:#ccc; } ';
            pre += 'div.context ol.context-line li span { float: right; } ';
            pre += 'div.commands { margin-left: 40px; } ';
            pre += 'div.commands a { color:black; text-decoration:none; } ';
            pre += '#summary { background: #ffc; } ';
            pre += '#summary h2 { font-weight: normal; color: #666; } ';
            pre += '#explanation { background:#eee; } ';
            pre += '#template, #template-not-exist { background:#f6f6f6; } ';
            pre += '#template-not-exist ul { margin: 0 0 0 20px; } ';
            pre += '#unicode-hint { background:#eee; } ';
            pre += '#traceback { background:#eee; } ';
            pre += '#requestinfo { background:#f6f6f6; padding-left:120px; } ';
            pre += '#summary table { border:none; background:transparent; } ';
            pre += '#requestinfo h2, #requestinfo h3 { position:relative; margin-left:-100px; } ';
            pre += '#requestinfo h3 { margin-bottom:-1em; } ';
            pre += '.error { background: #ffc; } ';
            pre += '.specific { color:#cc3300; font-weight:bold; } ';
            pre += 'h2 span.commands { font-size:.7em;} ';
            pre += 'span.commands a:link {color:#5E5694;} ';
            pre += 'pre.exception_value { font-family: sans-serif; color: #666; font-size: 1.5em; margin: 10px 0 10px 0; } ';
            pre += '</style> ';
            pre += '<script type="text/javascript"> ';
            pre += 'function getElementsByClassName(oElm, strTagName, strClassName){ ';
            pre += 'var arrElements = (strTagName == "*" && document.all)? document.all : ';
            pre += 'oElm.getElementsByTagName(strTagName); ';
            pre += 'var arrReturnElements = new Array(); ';
            pre += 'strClassName = strClassName.replace(/\-/g, "\-"); ';
            pre += 'var oRegExp = new RegExp("(^|\s)" + strClassName + "(\s|$)"); ';
            pre += 'var oElement; ';
            pre += 'for(var i=0; i<arrElements.length; i++){ ';
            pre += 'oElement = arrElements[i]; ';
            pre += 'if(oRegExp.test(oElement.className)){ ';
            pre += 'arrReturnElements.push(oElement); ';
            pre += '} ';
            pre += '} ';
            pre += 'return (arrReturnElements) ';
            pre += '} ';
            pre += 'function hideAll(elems) { ';
            pre += 'for (var e = 0; e < elems.length; e++) { ';
            pre += 'elems[e].style.display = "none"; ';
            pre += '} ';
            pre += '} ';
            pre += 'window.onload = function() { ';
            pre += 'hideAll(getElementsByClassName(document, "table", "vars")); ';
            pre += 'hideAll(getElementsByClassName(document, "ol", "pre-context")); ';
            pre += 'hideAll(getElementsByClassName(document, "ol", "post-context")); ';
            pre += 'hideAll(getElementsByClassName(document, "div", "pastebin")); ';
            pre += '}; ';
            pre += 'function toggle() { ';
            pre += 'for (var i = 0; i < arguments.length; i++) { ';
            pre += 'var e = document.getElementById(arguments[i]); ';
            pre += 'if (e) { ';
            pre += 'e.style.display = e.style.display == "none" ? "block" : "none"; ';
            pre += '} ';
            pre += '} ';
            pre += 'return false; ';
            pre += '} ';
            pre += 'function varToggle(link, id) { ';
            pre += 'toggle("v" + id); ';
            pre += 'var s = link.getElementsByTagName("span")[0]; ';
            pre += 'var uarr = String.fromCharCode(0x25b6); ';
            pre += 'var darr = String.fromCharCode(0x25bc); ';
            pre += 's.innerHTML = s.innerHTML == uarr ? darr : uarr; ';
            pre += 'return false; ';
            pre += '} ';
            pre += 'function switchPastebinFriendly(link) { ';
            pre += 's1 = "Switch to copy-and-paste view"; ';
            pre += 's2 = "Switch back to interactive view"; ';
            pre += 'link.innerHTML = link.innerHTML == s1 ? s2 : s1; ';
            pre += 'toggle("browserTraceback", "pastebinTraceback"); ';
            pre += 'return false; ';
            pre += '} ';
            pre += '<' + '/script> ';
            pre += '</head> ';
            pre += '<body> ';

            var post = '</body></html>';

            text = pre + text + post;
        } else {
            text = "<pre>" + text + "</pre>";
        }
    }

    var doc = document.open("text/html", "replace");
    doc.write(text);
    doc.close();
}

function ordinal( n ) {
    var s = [ "th", "st", "nd", "rd" ],

    v = n % 100;

    return n + ( s[ (v-20) % 10 ] || s[ v ] || s[ 0 ] );
}

function validateDecimal(value) {
    var RE = /^\d*\.?\d*$/;

    alert("Value = [" + value + "]");
    alert("RE Test = [" + RE.test(value) + "]");
    if(RE.test(value)) {
        return true;
    } else {
        return false;
    }
}

function validateDate(value) {
    if (value == "")
        return false;

    // Declare Regex 
    var rxDatePattern = /^(\d{1,2})(\/|-)(\d{1,2})(\/|-)(\d{4})$/;
    var dtArray = value.match(rxDatePattern); // is format OK?

    if (dtArray == null)
        return false;

    // Checks for mm/dd/yyyy format.
    dtMonth = dtArray[1];
    dtDay= dtArray[3];
    dtYear = dtArray[5];

    if (dtMonth < 1 || dtMonth > 12)
        return false;
    else if (dtDay < 1 || dtDay> 31)
        return false;
    else if ((dtMonth==4 || dtMonth==6 || dtMonth==9 || dtMonth==11) && dtDay ==31)
        return false;
    else if (dtMonth == 2) {
        var isleap = (dtYear % 4 == 0 && (dtYear % 100 != 0 || dtYear % 400 == 0));

        if (dtDay> 29 || (dtDay ==29 && !isleap))
            return false;
    }

    return true;
}

// Throw up a jquery-ui dialog to issue a warning
function warning(message, title)
{
    if (!title)
    {
        title = "Warning";
    }

    $("<div></div>").html(message).dialog({
        title: title,
        resizable: false,
        modal: true,
        buttons: {
            "Ok": function() { $(this).dialog("close"); }
        }
    });
}

