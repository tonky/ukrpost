Parcel.Map = {
	initialize: function() {
		var latlng = new google.maps.LatLng(48.821333, 29.26709);
	  
	  var options = {
	  	zoom: 6,
	    center: latlng,
	    mapTypeId: google.maps.MapTypeId.ROADMAP,
	    disableDefaultUI: true,
		  scaleControl: false,
		  navigationControl: true
	  };
	
	  this._map = new google.maps.Map(document.getElementById("map_canvas"), options);
	},
	
	reset: function() {
		if (this._marker) {
			this._marker.setMap(null);
		}
		if (this._infoWindow) {
			this._infoWindow.close();
		}
	},
	
	showParcel: function(parcel) {
		var location = new google.maps.LatLng(parcel.coordinates.lat, parcel.coordinates.lng);
		
		this._marker = new google.maps.Marker({
		  position: location, 
		  map: this._map,
		  title: parcel.name
		});
		
		this._infoWindow = new google.maps.InfoWindow({
		  content: parcel.status_full,
		  maxWidth: 200
		});
	
		this._infoWindow.open(this._map, this._marker);
	}
};