/***
 Target: Cisco Spark specific integration
 Version: 0.1
 Date: 2017/01/18
 Author: Guillain (guillain@gmail.com)
***/

// Helper function that generates a random alpha/numeric string
var randomString = function(length) {
    var str = "";
    var range = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for(var i = 0; i < length; i++) {
        str += range.charAt(Math.floor(Math.random() * range.length));
    }
    return str;
}

/*  popup confirmation */
function getConfirm(){
    if(confirm('Are you sure you want to disable this button?') == true) {
        return true;
    }
    else {
        return false;
    }
}

/* get session ID */
var getSessionParam = function getSessionParam(sParam){
    var re = new RegExp('/'+sParam+'=[^;]+/');
    var jsId = document.cookie.match(re);
    if(jsId != null) {
        if (jsId instanceof Array)
            jsId = jsId[0].substring(11);
        else
            jsId = jsId.substring(11);
    }
    return jsId;
}

/* get Url parameters */
var getUrlParam = function getUrlParam(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

/* resize the input form according to the length of the text */
$('input[type="text"]')
    // event handler
    .keyup(resizeInput)
    // resize on page load
    .each(resizeInput);

function resizeInput() {
    $(this).attr('size', $(this).val().length);
}

/* display additionnal info when onmouse */
function onmouseoveragent(el) {
    var hint = el.querySelector("div.hideme");
    hint.style.display = 'block';

    hint.style.top = Math.max(el.offsetTop - hint.offsetHeight,0) + "px";
    hint.style.left = el.offsetLeft + "px";
};
function onmouseoutagent(el) {
    var hint = el.querySelector("div.hideme");
    hint.style.display = 'none';
}

/* json to list function */
function jsonToList(data) {    
    if (typeof(data) == 'object') {        
        var ul = $('<ul>');
        for (var i in data) {            
            ul.append($('<li>').text(i).append(jsonToList(data[i])));         
        }        
        return ul;
    } else {       
        var textNode = document.createTextNode(' => ' + data);
        return textNode;
    }
}

// implement JSON.stringify serialization
function jsonToString(obj){
    var t = typeof (obj);
    if (t != "object" || obj === null) {
        // simple data type
        if (t == "string") obj = '"'+obj+'"';
        return String(obj);
    }
    else {
        // recurse array or object
        var n, v, json = [], arr = (obj && obj.constructor == Array);
        for (n in obj) {
            v = obj[n]; t = typeof(v);
            if (t == "string") v = '"'+v+'"';
            else if (t == "object" && v !== null) v = JSON.stringify(v);
            json.push((arr ? "" : '"' + n + '":') + String(v));
        }
        return (arr ? "[" : "{") + String(json) + (arr ? "]" : "}");
    }
};

