(function () {
    "use strict";
    var Autosuggest = function ($elements, url, template) {
        this.$elements = $elements;
        this._template = template ? _.template(template) : _.template("<a class='ui-corner-all' tabindex='-1'><%= PlaceName %> (<%= PlaceId %>)</a>");
        this._url = "https://partners.api.skyscanner.net";
        this._url += "/apiservices/xd/autosuggest/v1.0/UK/GBP/en-GB/";
        //this._cache = {};
        this.init();
    };
    Autosuggest.prototype.init = function () {
        var self = this;
        this.$elements.autocomplete({
            minLength: 3,
            focus: function (event, ui) {
                $(this).val(self._value(ui.item));
                $(this).attr("title", self._label(ui.item));
                $(this).next().text(self._label(ui.item)).attr("title", self._label(ui.item));
                return false;
            },
            select: function (event, ui) {
                $(this).val(self._value(ui.item));
                $(this).attr("title", self._label(ui.item));
                $(this).next().text(self._label(ui.item)).attr("title", self._label(ui.item));
                return false;
            },
            source: function (request, response) {
                if (self._cache[request.term]) {
                    response(self._cache[request.term]);
                    return;
                }
                $.ajax({
                    url: self._getUrl(request),
                    type: "GET",
                    dataType: "jsonp",
                    data: {
                        query: request.term
                    },
                    success: function (data) {
                        data = self._filter(data);
                        self._cache[request.term] = data;
                        response(data);
                    }
                });
            }
        }).each(function () {
            $(this).data("uiAutocomplete")._renderItem = $.proxy(self._renderItem, self);
            $(this).after("<span class='test-hareness-autosuggest-label'></span>");
        });
    };
    Autosuggest.prototype._getUrl = function (request) {
        return this._url;
    };
    Autosuggest.prototype._value = function (item) {
        return item.PlaceId;
    };
    Autosuggest.prototype._label = function (item) {
        return item.PlaceName;
    };
    Autosuggest.prototype._filter = function (data) {
        return _.filter(data.Places, function (place) {
            return place.PlaceId !== place.CountryId;
        });
    };
    Autosuggest.prototype._renderItem = function (ul, item) {
        return $("<li>").html(this._template(item)).appendTo(ul);
    };
    
    Skyscanner.TestHarnessAutosuggest = Autosuggest;
    
}());