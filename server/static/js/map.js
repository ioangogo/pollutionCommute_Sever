/*
Author: Ioan Loosley 2020
*/

var lat = 0;
var lng = 0;

var queryParams = urlParams = new URLSearchParams(window.location.search);

if(queryParams.has("lat") && queryParams.has("lng")){
    lat = queryParams.get("lat");
    lng = queryParams.get("lng");
}


function pmtoColour(pm) {
    /*
    Function adapted from: https://stackoverflow.com/a/30144587 and is licenced under a CC-BY Licence 
    Thank You Felipe Ribeiro
    */
    var color1 = [255, 0, 0];
    var color2 = [0, 255, 0];
    var p = (pm / 25.0);
    console.log(pm);
    console.log(p);
    var w = p * 2 - 1;
    var w1 = (w / 1 + 1) / 2;
    var w2 = 1 - w1;
    var rgb = [Math.round(color1[0] * w1 + color2[0] * w2),
    Math.round(color1[1] * w1 + color2[1] * w2),
    Math.round(color1[2] * w1 + color2[2] * w2)];
    return rgb;
}

// Used in various places to get data and for confiuring the graph
var Sevendays = moment().subtract(1, 'd').format('YYYY-MM-DD')
var SevendaysWH = moment().subtract(1   , 'd')
var today = moment()

/*
Leaflet Map Setup
*/
var startpost = new Array
var Markers = new Array;

var map = L.map('map', { worldCopyJump: true });
function doGeo() {
    var options = {
        timeout: 5000,
        maximumAge: 0
    };
    // This only seems to work on mobile
    navigator.geolocation.getCurrentPosition(function (pos) {
        map.panTo(new L.LatLng(pos.coords.latitude, pos.coords.longitude));
    },
        function (err) { console.warn(`ERROR(${err.code}): ${err.message}`); },
        options);

}
map.whenReady(doGeo);
map.setView([lat, lng], 7); // Initialise the map

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
map.on('zoomend', updateSensors);
map.on('moveend', updateSensors);

/*
Chart JS Chart Setup
*/
var ctx = document.getElementById('DataChart');
const graphOptions = { scales: { yAxes: [{scaleLabel: {labelString: "PM2.5 µg/m³", display: true}} ],  xAxes: [{ type: 'time', time: { unit: "hour" }, ticks: { min: Sevendays, max: today } }] } };
var lineChart = new Chart(ctx, {
    type: 'scatter',
    data: { datasets: [{ label: "Sensors In View", data: [] }] },
    options: graphOptions
});

/**
 * This function is called whenever the map stops moving and requests recordings from
 * the server to show on the map, it also adds data to the chart
 * @param {*} ev event data... this isnt used
 */
var timerObj = setInterval(updateSensors, 30*1000);

function updateSensors(ev) {
    clearInterval(timerObj);
    Markers.forEach(mark => { map.removeLayer(mark); });
    lineChart.destroy();
    Markers = new Array;
    var bounds = map.getBounds();
    var request = { "after": Sevendays.toString(), "bottom": { "lat": bounds._northEast.lat, "lng": bounds._northEast.lng }, "top": { "lat": bounds._southWest.lat, "lng": bounds._southWest.lng } }
    fetch('/api/GetSensorInTimeBounds', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(request)
    }).then(response => response.json()).then((Json) => {
        var Newdata = new Array;
        graphOptions.min = Json[0].datetime;
        for (const record of Json) {// Loop through the recived JSON
            // Make a marker to place on the map with the colour based on the PM levels
            var pmMarker = L.AwesomeMarkers.icon({
                icon: 'cloud',
                prefix: 'ion',
                iconColor: 'rgb(' + pmtoColour(record.pm25).join() + ')'
            });
            var LamMarker = new L.marker([record.lat, record.lng], { icon: pmMarker });
            var GraphData = { x: new Date(record.datetime), y: record.pm25 } // Add the date and PM to the graph
            Newdata.push(GraphData) // 

            LamMarker.bindPopup("<b style='text-align: center;'>" + moment(record.datetime).format('HH:MM DD-MM-YYYY') + "</b><br><b>PM2.5</b>" + record.pm25);

            Markers.push(LamMarker);
            map.addLayer(LamMarker);
        }

        // Put the new chart in the page
        var ctx = document.getElementById('DataChart');
        lineChart = new Chart(ctx, {
            type: 'scatter',
            data: { labels: ["pm2.5 pollution"], datasets: [{ label: "Sensors In View", showLine: true, data: Newdata }] }, options: graphOptions
        });
    });
    timerObj = setInterval(updateSensors, 30*1000);
}

updateSensors();
