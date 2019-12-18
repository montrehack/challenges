"use strict";
var system = require("system");
var args = system.args;

if (args.length >= 2) {
    var url = args[1];

    var cookie_domain = args[2];
    var cookie_name = args[3];
    var cookie_value = args[4];
    var page = require('webpage').create();
    if (cookie_domain && cookie_name && cookie_value) {
        page.customHeaders = {
            "Referer": "https://" + cookie_domain + "/admin"
        };
        phantom.addCookie({
            'name' : cookie_name,
            'domain' : cookie_domain,
            'value' : cookie_value,
            'path' : '/',
            'httponly' : false,
            'secure'   : false
        });
    }

    if (url.indexOf("http://") !== 0 && url.indexOf("https://") !== 0) {
        url = "http://" + url;
    }
    page.open(url, function(status) { });
    setTimeout(function () {
        phantom.exit();
    }, 7000);
} else {
    phantom.exit();
}
