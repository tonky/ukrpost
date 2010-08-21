Parcel.Lookup = (function() {
	this.find = function(parcelId, callback) {
		$.get("/track/" + parcelId, 
			function(data) {
				if (!data) {
					return;
				}
				
				var result = eval(data);
				callback(data);
			}
		)
	};
	
	return this;
})();