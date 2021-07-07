ships = {};
const DIST_THRESHOLD = 30000; //miles
const TIME_THRESHOLD = 2 * 60000;//milliseconds
totalpins = 0

function updateMapWithBounds(){
    if(map.getZoom() > 8){
        var bounds = map.getBounds();
        var northWest = [bounds.getNorthWest().lat, bounds.getNorthWest().lng],
        northEast = [bounds.getNorthEast().lat, bounds.getNorthEast().lng],
        southWest = [bounds.getSouthWest().lat, bounds.getSouthWest().lng],
        southEast =[bounds.getSouthEast().lat, bounds.getSouthEast().lng];
        var Httpreq = new XMLHttpRequest(); // a new request
        Httpreq.open("GET","http://localhost:8000/region/" + JSON.stringify({"nw": northWest, "ne": northEast, "se": southEast, "sw": southWest}),true);
        Httpreq.send(null);
    }
}

function dragUpdate(){
    // Update the map on drag only if zoomed in enough
    if(map.getZoom() > 8){
        updateMapWithBounds();
    }
}

$(function () {

    map = L.map('map', {preferCanvas:true}).setView([0, 0], 2);

    L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, ' +
            'NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012',
        noWrap: true
    }).addTo(map);

    let search = L.control.search({position: 'topleft'}).addTo(map);
    search.init();
    map.on("dragend", dragUpdate)
});

function plot_rotated_marker(mmsi, lat, lon, cog) {
    let ship = ships[mmsi];
    let color = get_mmsi_color(mmsi);
    let dt =  new Date().getTime();
    if (ship == null) {
        let m = createDirectionalMarker([lat, lon], cog, color);
        ships[mmsi] = {'marker':m,'dt':dt};
        m.addTo(map);
        totalpins += 1
    } else {
        let old_latlng = ship.marker.getLatLng();
        let dist = geodesicApproximation(lat,old_latlng.lat,lon,old_latlng.lng);
        if (dist > DIST_THRESHOLD){
            ships[mmsi].marker = ship.marker.setLatLng([lat, lon]);
        }
        ships[mmsi].dt = dt;
    }
}


function removeOldShips(){
    console.log("Removing Old Ships");
   let thresh = new Date().getTime() - TIME_THRESHOLD;
    for (var key in ships) {
       if (ships[key].dt < thresh){
           console.log("Removing");
           map.removeLayer(ships[key].marker);
           delete ships[key];
           totalpins -= 1
       }
   }
}

setInterval(updateMapWithBounds,10000);
setInterval(removeOldShips,60000);
