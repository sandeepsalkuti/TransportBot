var map, infoWindow, msg;

function createMap () {
  
  var options = {
    center: { lat: 43.654, lng: -79.383 },
    zoom: 10
  };

  map = new google.maps.Map(document.getElementById('map'), options);
  infoWindow = new google.maps.InfoWindow;

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (p) {
      var position = {
        lat: p.coords.latitude,
        lng: p.coords.longitude,
      };
      var msg = 'longitude:' + position["lng"] + ':latitude:' + position["lat"];
      //document.getElementsByTd("result").innerHTML = msg;

      outputResult(msg);
      //alert( msg );
      //document.write(msg);
      infoWindow.setPosition(position);
      infoWindow.setContent('Your location!');
      infoWindow.open(map);
      map.setCenter(position);
    }, function () {
      handleLocationError('Geolocation service failed', map.getCenter());
    });
    
    //document.write(lat)
  } else {
    handleLocationError('No geolocation available.', map.getCenter());
  }
  
  function outputResult(msg){
    document.getElementById("result").innerHTML = msg;
  }
  
  //document.write(msg);
  //document.getElementById("result").innerHTML = msg;
  
  //console.log(lat);
}
function outputResult1(msg){
  //$('.result').addClass('result').html(msg);
  //document.getElementById("result").innerHTML = msg;
  document.getElementsByClassName("result").innerHTML = msg;
}

function handleLocationError (content, position) {
  infoWindow.setPosition(position);
  infoWindow.setContent(content);
  infoWindow.open(map);
}

