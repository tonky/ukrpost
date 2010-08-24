if (typeof(Parcel) == "undefined") Parcel = {};

Parcel.Main = {
	onReady: function() {
		$(document).ajaxError(function() {
		  alert("ajax error");
		});
				
		Parcel.Map.initialize();
		Parcel.Main.list = new Parcel.List($("#my_parcels"));
		
		if (Parcel.Main.list.count() > 0) {
			Parcel.Main.list.show();
		}
		else {
			if (location.href.indexOf("#/find") < 0) {
				$("#welcome_overlay").show();
			}
		}
		
		$.address.change(Parcel.Main.onAddressChange);
		
		$("#welcome_overlay button").click(function() { 
			var parcelId = $("#welcome_overlay input[type=text]").val();
			$.address.value("find/" + parcelId);
		});
	},
	
	findParcel: function(parcelId) {
		Parcel.Lookup.find(parcelId, this.onFindSuccess);
	},
	
	onAddressChange: function(event) {
		value = event.value;
		
		if (value == '/') {
			Parcel.Main.reset();
			return;
		}
		
		var parts = value.split("/");
		if (parts.length < 3) return;
		
		if (parts[1] == 'find') {
			Parcel.Main.findParcel(parts[2]);
			return;
		}
	},
	
	onFindSuccess: function(result) {
		$("#welcome_overlay").hide();

		Parcel.Map.showParcel(result);
		Parcel.Main.list.showParcel(result);
	},
	
	reset: function() {
		if (this.list.count() == 0) {
			$("#welcome_overlay").show();
		}
		Parcel.Map.reset();
	}
};

$(document).ready(Parcel.Main.onReady);