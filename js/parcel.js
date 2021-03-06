if (typeof(Parcel) == "undefined") Parcel = {};

Parcel.Main = {
	onReady: function() {
		$(document).ajaxError(function(e, xhr, settings, exception) {
		  Parcel.Main._stopProgress();
		  $("#welcome_overlay").hide();

			if (xhr.status == 404) {
				$("#not_found").show();
			}
			else {
		    $("#error .parcel-no").html(Parcel.Main._lastParcelId);			
			  $("#error").show();
		    Parcel.Main._ajaxErrorText = xhr.responseText;
			}
		});
		
		$("#error .explain").click(function(e) {
			e.preventDefault();
			alert(Parcel.Main._ajaxErrorText);
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
		
		$.address.change(Parcel.Main._onAddressChange);
		
		var button = $("#welcome_overlay button");
		var input = $("#welcome_overlay input[type=text]");
		
		button.click(function() { 
			var parcelId = input.val();
			$.address.value("find/" + parcelId);
		});
		
		var validator = new Parcel.CodeInputValidator(input, button);
		validator.activate();
		
		$("#welcome_overlay a.sample").click(function(e) {
			e.preventDefault();
			input.val($(this).html());
			validator.validate();
		});
		
		$("#about").tooltip({
			events: {
				def: "mouseenter click, mouseleave click"
			},
			tip: "#about_tip"
		});
		
		$("#about").click(function(e) { e.preventDefault(); });
		$("#feedback").click(function(e) {
			e.preventDefault();
			
			UserVoice.Popin.show(uservoiceOptions);
		});
	},
	
	findParcel: function(parcelId) {
		Parcel.Map.reset();
		$("#error").hide();
		$("#not_found").hide();
		
		this._lastParcelId = parcelId;
		this._startProgress(parcelId);
		
		Parcel.Lookup.find(parcelId, this._onFindSuccess);
	},
	
	_onAddressChange: function(event) {
		value = event.value;
		
		if (value == '/') {
			Parcel.Main._reset();
			return;
		}
		
		var parts = value.split("/");
		if (parts.length < 3) return;
		
		if (parts[1] == 'find') {
			Parcel.Main.findParcel(parts[2]);
			return;
		}
	},
	
	_onFindSuccess: function(result) {
		$("#welcome_overlay").hide();
	
		Parcel.Main._stopProgress();

		Parcel.Map.showParcel(result);
		Parcel.Main.list.showParcel(result);
	},
	
	_startProgress: function(parcelId) {
		$("#progress .parcel-no").html(parcelId);
		$("#progress").show();
	},
	
	_stopProgress: function()
	{
		$("#progress").hide();
	},
	
	_reset: function() {
		if (this.list.count() == 0) {
			$("#welcome_overlay").show();
		}
		$("#error").hide();
		Parcel.Map.reset();
		this.list.reset();
	}
};

$(document).ready(Parcel.Main.onReady);