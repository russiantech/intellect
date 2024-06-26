class MiscPlayer {
    constructor() { this._contentsScrollbar = null, this._initPlayer(), this._initMoveContent() }
    _initPlayer() { document.querySelectorAll(".player").forEach((e => { new Plyr(e) })) }
    _initMoveContent() {
        if ("undefined" != typeof MoveContent && document.querySelector("#tableOfContentsMoveContent")) {
            const e = document.querySelector("#tableOfContentsMoveContent"), t = e.getAttribute("data-move-target"),
                o = e.getAttribute("data-move-breakpoint");
            new MoveContent(e, {
                targetSelector: t, moveBreakpoint: o, beforeMove: e => { this._contentsScrollbar && this._contentsScrollbar.destroy() },
                afterMove: e => {
                    "undefined" != typeof OverlayScrollbars && (this._contentsScrollbar = OverlayScrollbars(document.querySelectorAll(".table-of-contents-scroll"),
                        { scrollbars: {}, overflowBehavior: { x: "hidden", y: "scroll" } })),
                    jQuery("#tableOfContentsModal").modal("hide")
                }
            })
        }
    }
}