      function initAutocomplete() {
        var map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 30.3165, lng: 78.0322},
          zoom: 10,
          mapTypeId: 'roadmap'
        });
        //To make the marker bounce`
        //animation:google.maps.Animation.BOUNCE

        //To make the marker drop
        //animation:google.maps.Animation.Drop

        //Function to get your current location
        /*function locate(){
	        document.getElementById("btnAction").disabled = true;
	        document.getElementById("btnAction").innerHTML = "Processing...";
	        if ("geolocation" in navigator){
		    navigator.geolocation.getCurrentPosition(function(position){
			    var currentLatitude = position.coords.latitude;
			    var currentLongitude = position.coords.longitude;

			    var infoWindowHTML = "Latitude: " + currentLatitude + "<br>Longitude: " + currentLongitude;
			    var infoWindow = new google.maps.InfoWindow({map: map, content: infoWindowHTML});
			    var currentLocation = { lat: currentLatitude, lng: currentLongitude };
			    infoWindow.setPosition(currentLocation);
			    document.getElementById("btnAction").style.display = 'none';
		        });
	        }
        }*/

        // Create the search box and link it to the UI element.
        var input = document.getElementById('pac-input');
        var searchBox = new google.maps.places.SearchBox(input);
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        // Bias the SearchBox results towards current map's viewport.
        map.addListener('bounds_changed', function() {
          searchBox.setBounds(map.getBounds());
        });

        var markers = [];
        // Listen for the event fired when the user selects a prediction and retrieve
        // more details for that place.
        searchBox.addListener('places_changed', function() {
          var places = searchBox.getPlaces();

          if (places.length == 0) {
            return;
          }

          // Clear out the old markers.
          markers.forEach(function(marker) {
            marker.setMap(null);
          });
          markers = [];

          // For each place, get the icon, name and location.
          var bounds = new google.maps.LatLngBounds();
          places.forEach(function(place) {
            if (!place.geometry) {
              console.log("Returned place contains no geometry");
              return;
            }

            var icon = {
              url: place.icon,
              size: new google.maps.Size(71, 71),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 34),
              scaledSize: new google.maps.Size(25, 25)
            };

            // Create a marker for each place.
            markers.push(new google.maps.Marker({
              map: map,
              icon: icon,
              title: place.name,
              position: place.geometry.location
            }));
            if (place.geometry.viewport) {
              // Only geocodes have viewport.
              bounds.union(place.geometry.viewport);
            } else {
              bounds.extend(place.geometry.location);
            }
            document.getElementById('cord1').value = place.geometry.location.lat();
            document.getElementById('cord2').value = place.geometry.location.lng();
          });
          map.fitBounds(bounds);
        });
      }
