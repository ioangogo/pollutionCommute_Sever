    /*
    percent to gradient code modified from this stack overflow question: https://stackoverflow.com/a/30144587
    Thank You Felipe Ribeiro
    */
   function pmtoColour(pm) {
    var color1 = [255, 0, 0];
    var color2 = [0, 255, 0];
    var p = (pm/25.0);
    console.log(pm);
    console.log(p);
    var w = p * 2 - 1;
    var w1 = (w/1+1) / 2;
    var w2 = 1 - w1;
    var rgb = [Math.round(color1[0] * w1 + color2[0] * w2),
        Math.round(color1[1] * w1 + color2[1] * w2),
        Math.round(color1[2] * w1 + color2[2] * w2)];
    return rgb;
}

var Sevendays = moment().subtract(7,'d').format('YYYY-MM-DD')
var SevendaysWH = moment().subtract(7,'d')
var today = moment()

var startpost = new Array
var Markers = new Array;
console.log(startpost)

var map = L.map('map',{worldCopyJump:true});
function doGeo(){
    var options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
    };

    navigator.geolocation.getCurrentPosition(function(pos){
        map.panTo(new L.LatLng(pos.coords.latitude, pos.coords.longitude));
        },
        function(err){console.warn(`ERROR(${err.code}): ${err.message}`);},
        options);
    
}
map.whenReady(doGeo);
map.setView([0,0], 7);



var ctx = document.getElementById('DataChart');

const graphOptions = {scales: {xAxes: [{type: 'time', time:{unit:"day"}, ticks:{min:Sevendays, max: today}}]}};

var lineChart=new Chart(ctx, {type: 'scatter',
    data: {datasets:[{label: "Sensors In View", data:[]}]},
    options: graphOptions
});



L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
map.on('zoomend', updateSensors);
map.on('moveend', updateSensors);



function updateSensors(ev){
    Markers.forEach(mark => {map.removeLayer(mark);});
    lineChart.destroy();
    Markers = new Array;
    var bounds = map.getBounds();
    var markeri=0;
    var request = {"after": Sevendays.toString(), "bottom": { "lat": bounds._northEast.lat, "lng": bounds._northEast.lng }, "top": { "lat": bounds._southWest.lat, "lng": bounds._southWest.lng } }
    fetch('/api/GetSensorInTimeBounds', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(request)
    }).then(response => response.json()).then((myJson) => {
        console.log(myJson)
        var Newdata = new Array;
        for (const record of myJson){
            var pmMarker = L.AwesomeMarkers.icon({
                                                    icon: 'cloud',
                                                    prefix:'ion',
                                                    iconColor: 'rgb('+pmtoColour(record.pm25).join()+')'});
            var LamMarker = new L.marker([record.lat, record.lng], {icon:pmMarker});
            var GraphData = {x: new Date(record.datetime), y: record.pm25}
            Newdata.push(GraphData)
            
            LamMarker.bindPopup("<b style='text-align: center;'>"+record.datetime+"</b><br><b>PM2.5</b>"+record.pm25);
            
            Markers.push(LamMarker);
            map.addLayer(LamMarker);
            markeri+=1;
        }
        var ctx = document.getElementById('DataChart');
        lineChart=new Chart(ctx, {type: 'scatter',
        data: {labels:["pm2.5 pollution"], datasets:[{label: "Sensors In View", showLine: true, data: Newdata}]},options: graphOptions
        });
    });
}