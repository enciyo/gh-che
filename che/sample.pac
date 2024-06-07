function FindProxyForURL(url, host) {
    var proxyPort = {{port}};
    var targetUrl = "{{targetUrl}}";


    function isPortOpen(port) {
        var net = new ActiveXObject("WScript.Network");
        try {
            var connection = net.OpenSocket(port, host);
            connection.close();
            return true;
        } catch (e) {
            return false;
        }
    }


    if (url.indexOf(targetUrl) !== -1) {
        if (isPortOpen(proxyPort)) {
            return "PROXY 127.0.0.1:" + proxyPort;
        } else {
            return "DIRECT";
        }
    }
    return "DIRECT";
}
