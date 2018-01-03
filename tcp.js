var tcp = require('net');
var PORT = 8951;

const drives = []

tcp.createServer(function(sock) {
   
    sock.on('data', function(data) {
       
    });

    sock.on('close', function(data) {
        
    });
    
    drives[0] = sock
    
}).listen(PORT);

module.exports = { tcp tcp, drives drives };