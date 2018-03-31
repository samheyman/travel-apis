/*
skyscanner.api.v2.data.hotels.js
Copyright (c) <2014> Skyscanner Limited
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Skyscanner or any of its subsidiaries or affiliates nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. TO THE EXTENT PERMITTED BY LAW,  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
(function() {
    window.Skyscanner = window.Skyscanner || {};
    var root = window.Skyscanner;
    root.LivePricingClient = (function() {
        LivePricingClient.ON_RESULTS = 'onResults';
        LivePricingClient.ON_HOTELS_DETAILS = "onHotelsDetails";
        LivePricingClient.ON_SERVER_FAILURE = 'onServerFailure';
        LivePricingClient.ON_VALIDATION_FAILURE = 'onValidationFailure';
        LivePricingClient._HOTELS_LIVE_PRICING = 'https://gateway.skyscanner.net/hbe-bellboy/v1/web/prices/search/';
        LivePricingClient._MAX_POLLING_ATTEMPTS = 22;
        function LivePricingClient(callbacks) {
            this._apiService = '';
            this._callbacks = [];
            this._completeResult = {};
            this._images = [];
            this._hotels = [];
            this._pollUrl = '';
            this.device = 'N';
            if (callbacks) {
                this._registerCallback(LivePricingClient.ON_RESULTS, callbacks.onResults, this);
                this._registerCallback(LivePricingClient.ON_SERVER_FAILURE, callbacks.onServerFailure, this);
                this._registerCallback(LivePricingClient.ON_VALIDATION_FAILURE, callbacks.onValidationFailure, this);
                this._registerCallback(LivePricingClient.ON_HOTELS_DETAILS, callbacks.onHotelsDetails, this);
            }
            this.defaults = {
                market: "FR",
                currency: "GBP",
                locale: "en-GB"
            };
        }
        LivePricingClient.prototype.getHotels = function(options) {
            this._apiService = LivePricingClient._HOTELS_LIVE_PRICING;
            options = $.extend(this.defaults, options || {});
            //alert(JSON.stringify(options));
            this._composeResults(options);
            return options;
        };
        /* Create and Poll Session */
        LivePricingClient.prototype._composeResults = function(options) {
            var that = this;
            this._createSession(options)
                .then(this._pollForResults)
                .progress(function(data) {
                    that._inflateAndAppend(data);
                    //that._completeResult.images = that._images;
                    console.log("polling results from _composeResults");
                    that._callCallback(LivePricingClient.ON_RESULTS, that._completeResult, false);
                })
                .done(function(data) {
                    that._inflateAndAppend(data);
                    console.log("polling complete");
                    //that._completeResult.images = that._images;
                    that._callCallback(LivePricingClient.ON_RESULTS, that._completeResult, true);
                })
                .fail(function(callback, failure, source) {
                    console.log("_composeResults fail. callback " + JSON.stringify(callback) +
                        " failure: " + JSON.stringify(failure) + " source: " + JSON.stringify(source));
                    that._callCallback(callback, failure, source);
                });
        };
        LivePricingClient.prototype._createSession = function(query) {
            // get the entity id
            var that = this;
            var rex = /\(([^)]+)\)/;
            var entityId = rex.exec(query.entity)[1];
            var enhancers = "";
            for(param in query) {
                if (param.indexOf('enhancers_') !== -1) {
                    enhancers += query[param] + ',';                
                }
            };
            enhancers = enhancers.slice(0,-1);
            console.log("enhancers: " + enhancers);
            var dfd = $.Deferred();
            var device = query.deviceType;
            var qry = "entity/" + entityId + "?"
                + "market=" + query.market
                + "&currency=" + query.currency
                + "&locale=" + query.locale
                + "&checkin_date=" + encodeURIComponent(query.checkindate)
                + "&checkout_date=" + encodeURIComponent(query.checkoutdate)
                + "&adults=" + query.adults
                + "&rooms=" + query.rooms
                + "&apikey=" + query.apikey
                + "&enhanced=" + enhancers;
            $.ajax({
                beforeSend: function(request) {
                    request.setRequestHeader("x-user-agent", device + ";B2B");
                },
                type: 'GET',
                url: that._apiService + qry,
                dataType: 'json',

            }).always(function(result, textStatus, xhr) {
                if (xhr.status >= 500 || result.status >= 500) {
                    dfd.reject(LivePricingClient.ON_SERVER_FAILURE, that._composeRejection(result), 'session creation');
                    return;
                } else if (xhr.status >= 400 || result.status >= 400) {
                    dfd.reject(LivePricingClient.ON_VALIDATION_FAILURE, that._composeRejection(result), 'session creation');
                    return;
                } else if (xhr.status >= 200) {
                    that._pollUrl = that._apiService + qry;
                    that.device = query.deviceType;
                    dfd.resolveWith(that, [result]);
                    return;
                } else {
                    dfd.reject(LivePricingClient.ON_VALIDATION_FAILURE, that._composeRejection(result), 'session creation');
                    return;
                }
            });
            return dfd.promise();
        };
        LivePricingClient.prototype._pollForResults = function(data) {
            console.log("polling for results");
            var that = this;
            var dfd = $.Deferred();
            var attemptCount = 1;
            var getTimeoutMs = function() {
                if (attemptCount < 2)
                    return 500;
                if (attemptCount < 16)
                    return 1500;
                return 3000;
            };
            var testAndSetTimeout = function() {
                if (dfd.state() === 'resolved')
                    return false;
                attemptCount++;
                if (attemptCount < LivePricingClient._MAX_POLLING_ATTEMPTS) {
                    setTimeout(timeoutHandler, getTimeoutMs());
                    return true;
                }
                return false;
            };
            var notifyOrResolve = function(result) {
                if (result.meta.status == 'PENDING') {
                    console.log("... results pending, polling again...");
                    if (testAndSetTimeout()) {
                        console.log("notify");
                        dfd.notify(result);
                    } else {
                        console.log("resolve");
                        dfd.resolve(result);
                    }
                } else {
                    console.log("polling complete, status is COMPLETED");
                    dfd.resolve(result);
                }
            };
            var timeoutHandler = function() {
                var opts = {
                    beforeSend: function(request) {
                        request.setRequestHeader("x-user-agent", that.device + ";B2B");
                    },
                    type: 'GET',
                    url: that._pollUrl,
                    dataType: 'JSON'
                };
                $.ajax(opts).always(function(result, textStatus, xhr) {
                    switch (xhr.status) {

                    case 200:
                    case 400:
                        notifyOrResolve(result);
                        break;
                    case 204:
                    case 304:
                    case 500: // poll again silently, or mark as complete if attempt limit reached
                        if (!testAndSetTimeout()
                            && dfd.state() !== 'completed') {
                            dfd.resolve(that._completeResult);
                        }
                        break;
                    // case 400:
                    //     //dfd.reject(LivePricingClient.ON_VALIDATION_FAILURE, that._composeRejection(xhr), 'polling for results');
                    //     if (!testAndSetTimeout()
                    //         && dfd.state() !== 'completed') {
                    //         dfd.resolve(that._completeResult);
                    //     }
                    //     break;
                    case 403:
                    case 410:
                    case 429:
                    default:
                        dfd.reject(LivePricingClient.ON_SERVER_FAILURE, that._composeRejection(xhr), 'polling for results');
                    }
                });
            };
            notifyOrResolve(data);
            return dfd.promise();
        };
        LivePricingClient.prototype._createSessionFail = function(that, failure, source) {
            that._callCallback(LivePricingClient.ON_SERVER_FAILURE, failure, source);
        };
        LivePricingClient.prototype._inflateAndAppend = function(data) {
            if (data.results) {
                data = this._inflateHotels(data);
                //todo sort by prices. this should be done in API
                $.extend(true, this._completeResult, data);
                // this._completeResult.hotels_prices.sort(function(a, b) {
                //     var aPrice = a.agent_prices[0].price_total;
                //     var bPrice = b.agent_prices[0].price_total;
                //     if (a.agent_prices[0].price_total === null || isNaN(a.agent_prices[0].price_total) || a.agent_prices[0].price_total < 0) aPrice = 9999999;
                //     if (b.agent_prices[0].price_total === null || isNaN(b.agent_prices[0].price_total) || b.agent_prices[0].price_total < 0) bPrice = 9999999;
                //     var sortValue = aPrice - bPrice;
                //     if (sortValue === 0) // if the prices are the same, sort on the deeplink
                //         //return a.deeplink_url.localeCompare(b.deeplink_url); //todo
                //         return -1; //todo
                //     else
                //         return sortValue;
                // });
            }
        };
        LivePricingClient.prototype._inflateHotels = function(data) {
            if (!data || !data.results)
                return data;
            //amenities
            // $.each(data.hotels, function (h, hotel) {
            //     $.each(hotel.amenities, function (ha, hAmenity) {
            //         $.each(data.amenities, function (a, amenity) {
            //             if (amenity.id == hAmenity)
            //                 hotel.amenities[ha] = amenity.name;
            //         });
            //     });
            // });
            //images
            //$.each(data.hotels, function(h, hotel) {
            //    for (var i = 0; i < hotel.amenities.length; i++)
            //        hotel.amenities[i] = data.amenities[i].name;
            //});
            //hotels_prices
            // $.each(data.hotels_prices, function(i, hp) {
            //     $.each(data.hotels, function(j, hotel) {
            //         if (hp.id == hotel.hotel_id) {
            //             hp.hotel = hotel;
            //             if (data.urls)
            //                 hp.hotel.url = data.urls.hotel_details + "&hotelIds=" + hotel.hotel_id;
            //         }
            //     });
            // });
            return data;
        };
        LivePricingClient.prototype._composeRejection = function(xhr) {
            var debugInfo;
            try {
                debugInfo = JSON.parse(xhr.responseText || "");
            } catch(e) {
                debugInfo = "Could not provide further help" + e;
            }
            var rejection = {
                status: xhr.status,
                statusText: xhr.statusText,
                debugInformation: debugInfo
            };
            return rejection;
        };
        LivePricingClient.prototype._registerCallback = function(callbackId, callbackFunc, context) {
            this._callbacks.push({
                id: callbackId,
                func: callbackFunc,
                context: context
            });
        };
        LivePricingClient.prototype._callCallback = function() {
            var callbackId = arguments[0];
            var payload = arguments.length > 1 ? [].slice.call(arguments, 1) : [];
            for (var i = 0; i < this._callbacks.length; i++) {
                if (this._callbacks[i].id === callbackId) {
                    if (this._callbacks[i].func) {
                        try {
                            this._callbacks[i].func.apply(this._callbacks[i].context, payload);
                            return;
                        } catch(err) {
                            // An error happened in user-land code.
                            console.debug("An exception was thrown when calling your " + callbackId + " callback");
                            return;
                        }
                    }
                }
            }
            console.debug("A " + callbackId + " event occurred, but no callback is registered to handle it");
        };
        return LivePricingClient;
    })();
})();