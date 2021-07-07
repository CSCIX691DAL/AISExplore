io.connect('http://127.0.0.1:8080').on('ais', msg => plot_rotated_marker(msg.mmsi,msg.lat,msg.lon, msg.cog));

