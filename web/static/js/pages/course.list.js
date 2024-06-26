class CourseList {
    constructor() {
        this.menuButton = document.getElementById("menuButton"), 
        this.menuModal = new bootstrap.Modal(document.getElementById("menuModal")),
            this._addListeners(), 
            this._initMenuMoveContent(), 
            this._initBarrating()
    }

    _addListeners() { this.menuButton && this.menuButton.addEventListener("click", this._showMenuModal.bind(this)) }

    _initMenuMoveContent() {
        const t = this; 
        if (document.querySelector("#menuMoveContent")) {
            const e = document.querySelector("#menuMoveContent"), 
            n = e.getAttribute("data-move-target"),
                i = e.getAttribute("data-move-breakpoint");
            new MoveContent(e, { 
                targetSelector: n, 
                moveBreakpoint: i, 
                afterMove: e => { t._initBarratingForFilters() } 
                })
        }
    }
    _hideMenuModal() { this.menuModal.hide() }
    _showMenuModal() { this.menuModal.show() }

    _initBarrating() {
        jQuery().barrating && jQuery(".rating").each((function () {
            const t = jQuery(this).data("initialRating"),
                e = jQuery(this).data("readonly"), n = jQuery(this).data("showSelectedRating"),
                i = jQuery(this).data("showValues");
            jQuery(this).barrating({
                initialRating: t, 
                readonly: e, 
                showValues: i, 
                showSelectedRating: n, 
                onSelect: function (t, e) { },
                onClear: function (t, e) { }
            })
        }))
    }

    _initBarratingForFilters() { 
        jQuery().barrating && jQuery(".rating-filter").each((function () { 
        var t = jQuery(this).data("initialRating"), 
        e = jQuery(this).data("readonly"), 
        n = jQuery(this).data("showSelectedRating"), 
        i = jQuery(this).data("showValues"); 
        jQuery(this).barrating({ 
            initialRating: t, 
            readonly: e, 
            showValues: i, 
            showSelectedRating: n, 
            onSelect: function (t, e) { }, 
            onClear: function (t, e) { } }) 
        })) 
    }
}