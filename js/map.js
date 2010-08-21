Parcel.Map = (function() {
	this.initialize = function() {
		var latlng = new google.maps.LatLng(48.821333, 31.26709);
	  
	  var options = {
	  	zoom: 6,
	    center: latlng,
	    mapTypeId: google.maps.MapTypeId.ROADMAP,
	    disableDefaultUI: true,
		  scaleControl: false,
		  navigationControl: true
	  };
	
	  this._map = new google.maps.Map(document.getElementById("map_canvas"), options);
	};
	
	this.show = function(parcel) {
		/*
		var location = new google.maps.LatLng(parcel.lat, parcel.long) 
		
		this._marker = new google.maps.Marker({
		  position: location, 
		  map: this._map, 
		  title: parcel.name
		});
		
		this._infoWindow = new google.maps.InfoWindow({
		  content: parcel.status,
		  maxWidth: 200
		});
		*/
		
		var location = new google.maps.LatLng("48.482935", "34.976349")
	
		this._marker = new google.maps.Marker({
			position: location, 
			map: this._map, 
			title: "Название Отделения"
		});

		this._infoWindow = new google.maps.InfoWindow({
		  content: "Посылка бла бла бла",
		  maxWidth: 200
		});
	
		this._infoWindow.open(this._map, this._marker);
	}
	
	return this;
}());