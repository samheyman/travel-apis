(function () {
    //"use strict";
    var th = {};
    var client; 

    th = {
        $loader: $("#hourglass"),
        $submit: $("#btn-call"),
        $reproUrl: $("#repro-url"),
        $testHarnessProgress: $("#test-harness-progress"),
        $form: $("form"),
        $results: $(".results"),
        $rawDataTab: $("#raw-data-tab"),
        $previewDataTab: $("#preview-data-tab"),
        $rawDataTemplate: $("#rawDataTemplate"),
        $dataPreviewTemplate: $("#resultstable"),

        init: function () {
            th.$results.hide();
            th.$submit.click(th._onSubmitClick);
            $(document).on("click", ".page", function (e) {
                e.preventDefault();
            });
            //th._setUpAutosuggest();
        },

        _onSubmitClick: function(e) {
            e.preventDefault();
            th._clearResults();
            th.$loader.show();
            client = new Skyscanner.LivePricingClient({
                onResults: th.onResults
            });
            $formData = th.$form.serializeArray();
            var options = {};
            for (var i = 0; i < $formData.length; i++){
                options[$formData[i]['name']] = $formData[i]['value'];
            }
            client.getHotels(options);
        },
        onResults: function (data, isComplete) {
            console.log("getting results");
            //th.$testHarnessProgress.show();
            //th.$testHarnessProgress.html("Hotels Price List Service: Polling the session");
            if (th._hasData(data)) {
                console.log("rendering first page");
                th._renderData(data, 0); //render first page
            } else if (isComplete) {
                console.log("Results complete.");
                console.log(data);
                //testHarnessProgress.sendMessage("No results found or invalid place ID");
                //var table = th.$results;
                //table.append("<h4 class='test-harness-info-message txt-align-center'>No results found or invalid place ID</h4>");
                th.$loader.hide();
                //th.$submit.prop("disabled", false);
                return;
            }
            if (isComplete) {
                console.log("Data complete");
                th.$loader.hide();
                allData = data; //store all data
                results = allData.results.hotels;
                console.log(results);
                for (var i = 0; i < results.length; i++) {
                    var tr = $('<tr/>');
                    var hotel_info = "<td class=\"hotel-image\">" 
                        + "<img src=\"" +  results[i].images[0].thumbnail + "\" alt=\"hotel thumbnail\"/>"
                        + "</td>"
                        + "<td>"
                        + "<h5>" + results[i].name + "</h5>"
                        + "<ul>"
                        + "<li><b>Stars: </b>" + results[i].stars + "</li>"
                        + "<li><b>Property type: </b>" + results[i].property_type + "</li>"
                        + "</ul>"
                        + "</td>";
                    tr.append(hotel_info);
                    
                    th.$dataPreviewTemplate.append(tr);
                }
                //th.$rawDataTemplate.show();
                //th._getTruncatedRawContents(data)

                //testHarnessProgress.sendMessage("Hotels Details service: Creating the details for 10 hotels.", "get");
                //client.getHotelBookingDetails(th._buildUrls(data, 0), null, true);
            }
        },
        _getTruncatedRawContents: function (originalData) {
            console.log("truncating data");
            //Truncate data to avoid crashing the browser when displaying it in the DOM
            var new_data = originalData;
                
            // for (var key in new_data) {
            //     if (typeof(new_data[key]) === "object" && new_data[key].length && new_data[key].length > max) {
            //         new_data[key].length = max;
            //         truncated.push(key);
            //     }
            // // }
            // if (truncated.length > 0) {
            //     contents += "<div class='test-harness-warning'><span class='icon-attention-circled'></span>Note that the json below contains only the first ";
            //     contents += max + " " + truncated.join(", ") + "...</div>";
            // }
            //th.$rawDataTemplate.show();
            
            th.rawDataTemplate.text(JSON.stringify(new_data));
            console.log("adding nore content");
            return contents;
        },
        _hasData: function (data) {
            return data.count && (data.count > 0);
        },
        _renderData: function (data, page) {
            console.log("rendering data...");
            if (!th._hasData(data))
                return;
            //th._getTruncatedRawContents(data);
            th.$results.show();
            th.$rawDataTab.tab('show');
            th.$rawDataTemplate.text(JSON.stringify(data,null, 2));
        },
        _clearResults: function () {
            th.$rawDataTemplate.empty();
            th.$dataPreviewTemplate.empty();
            th.$results.hide();
        },
        _setUpAutosuggest: function () {
            th.testHarnessAutosuggest = new Skyscanner.TestHarnessAutosuggest(
                $(".test-harness-autosuggest"),
                "/apiservices/hotels/autosuggest/v2/UK/EUR/en-GB/",
                "<a class='ui-corner-all' tabindex='-1'><%= display_name %> (<%= individual_id %>)</a>");
            th.testHarnessAutosuggest._getUrl = function (request) {
                return this._url + request.term;
            };
            th.testHarnessAutosuggest._value = function (item) {
                return item.individual_id;
            };
            th.testHarnessAutosuggest._label = function (item) {
                return item.display_name;
            };
            th.testHarnessAutosuggest._filter = function (data) {
                return _.map(data.results, function (result) {
                    var parent_place = _.find(data.places, {place_id: result.parent_place_id});
                    if (parent_place) {
                        result.display_name += ", " + parent_place.admin_level1 + ", " + parent_place.country_name;
                    }
                    return result;
                });
            };
        },

    };
    

    th.init();


    $(document).ready(function(){
        $('[data-toggle="tooltip"]').tooltip(); 
        $('.datepicker-container .input-group.date').datepicker({
            format: "yyyy-mm-dd",
            startDate: "today"
        });

        var places = [
        {value:"London (27544008)", label:"London"},
        {value:"Paris (27539733)", label:"Paris"},
        {value:"Paris ()", label:"Paris2 "}
        ];
        $('#entity').autocomplete(
        {
            source: places, 
        });
        var element = $('.ui-helper-hidden-accessible').detach();
        $('.test-hareness-autosuggest-wrap').append(element);
    });


}());