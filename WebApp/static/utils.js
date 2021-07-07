function get_mmsi_color(mmsi){
    let colors = ['','red','blue',
                'orange','yellow',
                'purple','green',
                'black','white',
                'grey','lime']
    return colors[mmsi];
}

function createDirectionalMarker(p_lat_lon, angle, color = 'red') {


    let icon = '<svg xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" version="1.0" width="700" height="700"><rect id="backgroundrect" width="100%" height="100%" x="0" y="0" fill="none" stroke="none"/><defs id="defs9"/><g class="currentLayer"><title>Layer 1</title><g id="g4" class="selected" transform="rotate(-89.93659973144531 350.3506469726563,349.46508789062506) " stroke="#000000" stroke-opacity="1" stroke-width="4" fill="#ffffff" fill-opacity="1"><path d="M0.7127809999999997,-0.8547001342010496 C2.5712110000000017,-0.8547001342010496 700.7013,349.13757986579895 699.99948,349.71741986579895 C697.64471,351.66290986579895 0.5386209999999991,699.784939865799 0.28021100000000126,699.1444198657989 C0.11143099999999961,698.7260498657989 33.97113,619.847169865799 75.52398199999999,523.858019865799 L151.07464,349.33227986579897 L75.537317,175.09017986579894 C33.991804,79.25700986579895 0.000011000000000649384,0.4649398657989503 0.000011000000000649384,-0.0033201342010507062 C0.000011000000000649384,-0.4715801342010513 0.32076100000000096,-0.8547001342010496 0.7127809999999997,-0.8547001342010496 z" id="path6" style="" stroke="#000000" stroke-opacity="1" stroke-width="25" fill="' + color + '" fill-opacity="1"/></g></g></svg>';
    let svgURL = "data:image/svg+xml;base64," + btoa(icon);

    let myIcon = L.icon({
        iconUrl: svgURL,
        iconSize: [15, 15], // size of the icon
        iconAnchor: [7.5, 7.5],// point of the icon which will correspond to marker's location
    });
    let direction_icon = L.marker(p_lat_lon, {icon: myIcon, rotationAngle: angle});
    return direction_icon;
};

//https://blog.mapbox.com/fast-geodesic-approximations-with-cheap-ruler-106f229ad016
function geodesicApproximation(lat1,lat2,lon1,lon2){
    let dy = 122430 * (Math.abs(lat1-lat2)/180);
    let dx = 24901 * (Math.abs(lon1-lon2)/360) * Math.cos((lat1+lat2)/2);
    return Math.sqrt(Math.pow(dx,2)+Math.pow(dy,2));
}