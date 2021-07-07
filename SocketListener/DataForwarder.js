var http = require('http'), net = require('net'), io = require('socket.io');
var socket = io.listen(http.createServer().listen(8080));
net.createServer(s => s.on('data',d => socket.emit('ais',JSON.parse(d.toString())))).listen(1337);

/*
setInterval(function(){
    let ship = Math.floor(Math.random()*1000+1);
    let lat = Math.floor(Math.random()*180-90);
    let lon = Math.floor(Math.random()*360-180);
    socket.emit('ais',{
        'mmsi':ship,
        'lat': lat,
        'lon': lon
    })
},200);
*/
