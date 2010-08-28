Parcel.CodeInputValidator = function(input, button) {
	this.input = input;
	this.button = button;
}

Parcel.CodeInputValidator.prototype = {
	activate: function() {
		var input = this.input;
		var button = this.button;
		var validator = this;
		
		input.keyup(function() {
			validator.validate();
		});
		
		validator.validate();
	},
	
	validate: function() {
		var input = this.input;
		var button = this.button;
		
		var value = input.val();
		
		if (value.length == 13) {
			button.attr("disabled", "");
		}
		else {
			button.attr("disabled", "true");
		}
	}
}