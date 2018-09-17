var Websites = function () {
    var handleRecords = function () {
       var table = $('#datatable_websites');
       table.DataTable({
        "processing": true,
        "serverSide": true,
        "paginate": true,
        "pageLength": 10,
        "searching": false,
        "ajax": Websites.options.fetchUrl,
        "columns": [
                { "data": "id" },
                { "data": "website" },
                {
                    data: function (row) {
                            return '<a href="' + Websites.options.viewUrl + '/'  + row.id + '" class="btn btn-info" ><i class="fa fa-search"></i></a>';
                    }
                }
            ]

        });
    };
    return {
        dataTable: null,
        options: {},
        init: function (options) {
            this.options = options;
            handleRecords();
        }
    };
}();