class CourseDetail {
    constructor() {
        this._initPlayer(), 
        this._initBarrating(),
        this._initProgressBars()
    }

    _initPlayer() {
        null !== document.querySelector("#videoPlayer") && "undefined" != typeof Plyr && new Plyr(document.querySelector("#videoPlayer"))
    } 

    _initProgressBars() { 
        document.querySelectorAll(".progress-bar").forEach((t => { 
            const e = t.getAttribute("aria-valuenow"); 
            t.style.width = e + "%" })) 
        } 

    _initBarrating() { 
        jQuery().barrating && jQuery(".rating").each((function () { 
            const t = jQuery(this).data("initialRating"), 
            e = jQuery(this).data("readonly"), 
            r = jQuery(this).data("showSelectedRating"), 
            i = jQuery(this).data("showValues"); 
            jQuery(this).barrating({ 
                initialRating: t, 
                readonly: e, 
                showValues: i, 
                showSelectedRating: r, 
            onSelect: function (t, e) { }, 
            onClear: function (t, e) { } }) 
        })) }
}