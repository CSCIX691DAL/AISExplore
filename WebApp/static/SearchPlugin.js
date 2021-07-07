L.Control.Search = L.Control.extend({
    onAdd: function (map) {
        var div = L.DomUtil.create('div', 'search-leaflet-control');
        $(div).append('<input type="search" id="txtSearch" class="searchbar" placeholder="Search..."/>');
        $(div).append('<div id="searchResult" class="background-white"></div>');
        return div;
    },
    init: function () {
        $("#searchResult").hide();

        $("#txtSearch").on("blur", function () {
            if ($("#txtSearch").val().trim().length == 0) {
                $("#txtSearch").attr('style', '');
                $("#searchResult").toggle();
                $("#searchResult").html(" ");

            } else {
                $("#txtSearch").attr('style', 'width:100%;');
            }
        }).on("focus", function () {
            $("#searchResult").show('slow');
            var $this = $(this);
            $this.select();
        });
        $("#txtSearch").on("search", function (e) {
            if ($("#txtSearch").val().trim().length == 0) {
                $("#txtSearch").blur()
            }
        });
        timer = setTimeout(function () {
        }, 10);
        $('#txtSearch').keyup(function () {
            $("#searchResult").html(" ");

            clearTimeout(timer);
            timer = setTimeout(function (event) {
                let search = $('#txtSearch').val();
                $.get(`/search/${search}/`, function (data) {
                    let results = data.results;
                    let searchResults = $("#searchResult");
                    searchResults.html(" ");
                    for (let i = 0; i < results.length; i++) {
                        let item = `<div class=" search-item row">
                                        <div class="col-md-6" style="font-size:8px;">
                                            IMO: ${results[i].imo_num}<br>
                                            MMSI: ${results[i].mmsi}<br>
                                            NAME: ${results[i].name}
                                        </div>
                                        <div class="col-md-6">
                                        
                                        </div>
                                    </div><hr>
`;
                        searchResults.append(item);
                    }
                })
            }, 500);
        });

        $("#searchResult").on('mouseenter', function (e) {
            map.scrollWheelZoom.disable();
        });
        $("#searchResult").mouseleave(function (event) {
            var e = event.toElement || event.relatedTarget;
            if (e.parentNode == this || e == this) {
                return;
            }
            map.scrollWheelZoom.enable();
        });
    },
    onRemove: function (map) {
        // Nothing to do here
    }
});

L.control.search = function (opts) {
    return new L.Control.Search(opts);
};
