Parcel.List = function(root) {
	this._root = root;
	
	this._items = new Array();
	this._loadItems();
	
	var list = this;
	
	$.each(this._items, function(index, parcelId) {
		list._renderItem(parcelId);
	});
	
	var input = this._root.find("input[type=text]");
	var button = this._root.find("button");
	
	button.click(function() { 
		var parcelId = input.val();
		$.address.value("find/" + parcelId);
	});
	
	var validator = new Parcel.CodeInputValidator(input, button);
	validator.activate();
};

Parcel.List.prototype = {
	count: function() {
		return this._items.length;
	},
	
	hide: function() {
		this._root.hide();
		return this;
	},
	
	reset: function() {
		this._root.find("li a").removeClass("current");
	},
	
	show: function() {
		this._root.show();
		return this;
	},
	
	showParcel: function(parcel) {
		if (this.count() == 0) {
			this.show();
		}
		
		if ($.inArray(parcel.parcelId, this._items) < 0) {
			this._items.push(parcel.parcelId);
			this._saveItems();
			this._renderItem(parcel.parcelId);
		}
		
		this._root.find("li a").removeClass("current");
		$("#" + parcel.parcelId).addClass("current");
	},
	
	_loadItems: function() {
		if (!window.localStorage) {
			return;
		}
		
		var raw = window.localStorage.getItem("parcelList");
		if (!raw) return;
		
		this._items = raw.split("|");
	},
	
	_renderItem: function(parcelId) {
		this._root.find("ul").prepend("<li><a id=" + parcelId + " href='#/find/" + parcelId + "'>" + parcelId + "</a></li>");
	},
	
	_saveItems: function() {
		if (!window.localStorage) {
			return;
		}
		
		if (this.count() == 0) {
			return;
		}
		
		window.localStorage.setItem("parcelList", this._items.join("|"));
	}
}