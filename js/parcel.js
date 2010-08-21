if (typeof(Parcel) == "undefined") Parcel = new Object();

Parcel.Main = (function() {
	var main = this;
	
	this.onReady = function() {
		$(document).ajaxError(function() {
		  alert("ajax error");
		});
				
		Parcel.Map.initialize();
		
		$.address.change(function(event) {
			value = event.value;
			
			if (value == '/') {
				main.reset();
				return;
			}
			
			var parts = value.split("/");
			if (parts.length < 3) return;
			
			if (parts[1] == 'find') {
				main.findParcel(parts[2]);
				return;
			}
		});
		
		$("#welcome_overlay button").click(function() { 
			var parcelId = $("#welcome_overlay input[type=text]").val();
			$.address.value("find/" + parcelId);
		});
	};
	
	this.findParcel = function(parcelId) {
		Parcel.Lookup.find(parcelId, this.onFindSuccess);
	};
	
	this.onFindSuccess = function(result) {
		$("#welcome_overlay p").hide();
		$("#welcome_overlay button").html("Проверить другую посылку");
		$("#welcome_overlay").removeClass("waiting-for-input").addClass("with-input");
		
		Parcel.Map.show(result);
		//alert(result.name + "[" + result.index + "] " + result.explanation);
	};
	
	this.reset = function() {
		$("#welcome_overlay p").show();
		$("#welcome_overlay button").html("Проверить посылку");
		$("#welcome_overlay").removeClass("with-input").addClass("waiting-for-input");
	};
	
	$(document).ready(this.onReady);
	
	return this;
}());

//Parcel.Main.printA();