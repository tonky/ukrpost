Parcel.Lookup = {
	find: function(parcelId, callback) {
		$.get("/track/" + parcelId, 
			function(data) {
				if (!data) {
					return;
				}
				
				data.parcelId = parcelId;
				callback(data);
			}
		)
	}
}