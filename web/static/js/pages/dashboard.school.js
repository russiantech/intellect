class SchoolDashboard {
    constructor() {
        this._initBarrating()
    }
    _initBarrating() {
        jQuery().barrating && jQuery(".rating").each((function () {
            const a = jQuery(this).data("initialRating"),
                t = jQuery(this).data("readonly"),
                i = jQuery(this).data("showSelectedRating"),
                n = jQuery(this).data("showValues");
            jQuery(this).barrating({
                initialRating: a,
                readonly: t,
                showValues: n,
                showSelectedRating: i,
                onSelect: function (a, t) { },
                onClear: function (a, t) { }
            })
        }
        ))
    }
}