class Nav {
    get options() {

        return {
            matchUrl: !0, disablePinning: !1, verticalUnpinned: Globals.xxl.replace("px", ""),
            verticalMobile: Globals.lg.replace("px", ""),
            horizontalMobile: Globals.lg.replace("px", "")
        }
    }

    constructor(e, t = {}) {
        e && (
            this.settings = Object.assign(this.options, t),
            this.settings = Object.assign(this.settings, e.dataset),
            this.element = e, this._init()
            )
    }

    _init() {
        this.mobileButton = this.element.querySelector("#mobileMenuButton"),
        this.pinButton = this.element.querySelector("#pinButton"),
        this.colorButton = this.element.querySelector("#colorButton"),
        this.menuContainer = this.element.querySelector(".menu-container"),
        this.menuPlainOuter = this.element.querySelector("#menu").outerHTML, 
        this.menuPlainInner = this.element.querySelector("#menu").innerHTML, 
        this.html = document.documentElement, 
        this._onCollapseShow = this._onCollapseShow.bind(this),
        this._onCollapseHide = this._onCollapseHide.bind(this),
        this._onCollapseShown = this._onCollapseShown.bind(this),
        this._onVerticalMenuClick = this._onVerticalMenuClick.bind(this),
        this._onHorizontalMenuDropdownHidden = this._onHorizontalMenuDropdownHidden.bind(this),
        this._onHorizontalMenuDropdownClick = this._onHorizontalMenuDropdownClick.bind(this),
        document.querySelector("#menuSide") && (this.menuSideInner = document.querySelector("#menuSide").innerHTML),
        this._initMenuVariables(),
        this.verticalUnpinned = this.settings.verticalUnpinned, 
        this.verticalMobile = this.settings.verticalMobile, 
        this.horizontalMobile = this.settings.horizontalMobile, 
        this.placementStatus = 0, 
        this.behaviourStatus = 0, 
        this.selectedMenuBehaviour = this.html.getAttribute("data-behaviour"),
        this.selectedMenuPlacement = this.html.getAttribute("data-placement"),
        this.scrollbar, this.prevScrollpos = window.pageYOffset, 
        this.windowScrolled = !1, 
        this.collapseTimeout, 
        this.settings.disablePinning && this._disablePinButton(),
        this._initMenuPlacement(),
        this._addListeners()
    }

 _initMenuVariables() {
        this.menuVertical = document.createElement("DIV"),
        this.menuVertical.innerHTML = this.menuPlainOuter, this.menuVertical = this.menuVertical.firstChild, this.menuHorizontal = document.createElement("DIV"),
        this.menuHorizontal.innerHTML = this.menuPlainOuter, 
        this.menuHorizontal = this.menuHorizontal.firstChild, 
        this.menuSideInner && (
        "mobile" == this.html.getAttribute("data-dimension") ? (this.menuVertical = document.createElement("DIV"), 
        this.menuVertical.innerHTML = '<ul id="menu" class="menu">' + this.menuSideInner + this.menuPlainInner + "</ul>", 
        this.menuVertical = this.menuVertical.firstChild) : (
            this.menuVertical = document.createElement("DIV"), 
            this.menuVertical.innerHTML = '<ul id="menu" class="menu">' + this.menuPlainInner + "</ul>", 
            this.menuVertical = this.menuVertical.firstChild
            )
        )
    }

 _addListeners() {
        window.addEventListener("click", (e => { this._onWindowClick(e) })),
        window.addEventListener("resize", (e => { this._onWindowResize(e) })),
        window.addEventListener("scroll", (e => { this._onWindowScroll(e) })),
        this.element.addEventListener("mouseenter", (e => { this._onMouseEnter(e) })),
        this.element.addEventListener("mouseleave", (e => { this._onMouseLeave(e) })),
        this.html.addEventListener(Globals.menuPlacementChange, (e => this._onMenuPlacementChange(e))),
        this.html.addEventListener(Globals.menuBehaviourChange, (e => this._onMenuBehaviourChange(e))),
        this.colorButton && this.colorButton.addEventListener("click", (e => { this._onColorClick(e) })),
        this.mobileButton && this.mobileButton.addEventListener("click", (e => { this._showMobileMenu(e) })),
        this.pinButton && this.pinButton.addEventListener("click", (e => { this._onPinClick(e) })),
       
        setInterval((() => { this._onWindowScrollInterval() }), 200)
    }

 _addVerticalMenu() {
        document.querySelector("#menu").remove(),
        this._initMenuVariables(); this.menuVertical.querySelectorAll("a").forEach((e => {
            e.nextElementSibling && "UL" === e.nextElementSibling.tagName && (e.setAttribute("data-bs-toggle", "collapse"),
                e.setAttribute("data-role", "button"),
                e.setAttribute("aria-expanded", !1),
                e.nextElementSibling.classList.add("collapse"),
                new bootstrap.Collapse(e.nextElementSibling, { toggle: !1 }),
                e.getAttribute("data-bs-target") && e.nextElementSibling.setAttribute("id", e.getAttribute("data-bs-target").substring(1)))
        })),

        this.menuContainer.insertAdjacentElement("beforeend", this.menuVertical),
        document.querySelector("#menu").classList.add("show"),
        this._matchUrl(),
        this._initVerticalMenu(),
        this._initIcons()
    }

 _initVerticalMenu() {
        this._removeHorizontalMenuListeners(),
        this._addVerticalMenuListeners(); 
        this.menuVertical.querySelectorAll("a.active").forEach((e => {
            e.nextElementSibling && "UL" === e.nextElementSibling.tagName && (e.setAttribute("data-clicked", !0),
                e.setAttribute("aria-expanded", !0),
                e.nextElementSibling.classList.add("show"))
        })),
        
        this._destroyScrollbar(),
        this._initScrollbar(),
        this._initOtherDropdownsVertical()
    }

 _initOtherDropdownsVertical() {
        this.userDropdown && this.userDropdown.dispose(),
        this.languageDropdown && this.languageDropdown.dispose(),
        this.notificationDropdown && this.notificationDropdown.dispose(),
        document.querySelector(".user-container .user") && (this.userDropdown = new bootstrap.Dropdown(document.querySelector(".user-container .user"),
            { popperConfig: function (e) { return { placement: "bottom" } } })),
        document.querySelector(".language-switch-container .language-button") && (this.languageDropdown = new bootstrap.Dropdown(document.querySelector(".language-switch-container .language-button"),
            { popperConfig: function (e) { return { placement: "bottom" } } })),
        document.querySelector(".menu-icons .notification-button") && (this.notificationDropdown = new bootstrap.Dropdown(document.querySelector(".menu-icons .notification-button"),
            {
                reference: document.querySelector(".menu-icons"),
                popperConfig: function (e) { return { placement: "bottom" } }
            }))
    }

 _hideOtherDropdownsVertical() {
        this.userDropdown && this.userDropdown.hide(),
        this.languageDropdown && this.languageDropdown.hide(),
        this.notificationDropdown && this.notificationDropdown.hide()
    }

 _addVerticalMenuListeners() {
        this._removeVerticalMenuListeners(),
        document.querySelectorAll("#menu .collapse").forEach((e => { e.addEventListener("show.bs.collapse", this._onCollapseShow) })),
        document.querySelectorAll("#menu .collapse").forEach((e => { e.addEventListener("hide.bs.collapse", this._onCollapseHide) })),
        document.querySelectorAll("#menu .collapse").forEach((e => { e.addEventListener("shown.bs.collapse", this._onCollapseShown) })),
        document.querySelector("#menu").addEventListener("click", this._onVerticalMenuClick)
    }

 _removeVerticalMenuListeners() {
        document.querySelector("#menu").removeEventListener("click", this._onVerticalMenuClick),
        document.querySelectorAll("#menu .collapse").forEach((e => { e.removeEventListener("show.bs.collapse", this._onCollapseShow) })),
        document.querySelectorAll("#menu .collapse").forEach((e => { e.removeEventListener("hide.bs.collapse", this._onCollapseHide) })),
        document.querySelectorAll("#menu .collapse").forEach((e => { e.removeEventListener("shown.bs.collapse", this._onCollapseShown) }))
    }

 _onCollapseHide(e) { const t = e.target.previousElementSibling; t && "A" === t.tagName && t.setAttribute("aria-expanded", !1) } 
_onCollapseShow(e) { const t = e.target.previousElementSibling; t && "A" === t.tagName && t.setAttribute("aria-expanded", !0) } 
_onCollapseShown(e) { const t = e.target.previousElementSibling; t && "A" === t.tagName && t.setAttribute("data-clicked", !0) } 
_onVerticalMenuClick(e) { const t = e.target.closest("a"); t && "true" === t.getAttribute("data-clicked") && t.removeAttribute("data-clicked") } 
_addHorizontalMenu() {
        document.querySelector("#menu").remove(),
        this._initMenuVariables(); const e = this.menuHorizontal; e.querySelectorAll("li").forEach((e => { e.querySelector(":scope > ul") && e.classList.add("dropdown") })),
            e.querySelectorAll(":scope > li").forEach((e => {
                let t = "a"; if (e.classList.contains("mega")) {
                    t = ":scope > a"; const i = e.querySelectorAll(":scope > ul>li").length; e.querySelectorAll(":scope > ul").forEach((e => {
                        e.classList.add("row"),
                        e.classList.add("align-items-start"),
                        e.classList.add("row-cols-" + i),
                        e.querySelectorAll("li").forEach((e => {
                            e.classList.add("col"),
                            e.classList.add("d-flex"),
                            e.classList.add("flex-column")
                        }))
                    }))
                } e.querySelectorAll(t).forEach((e => {
                    e.nextElementSibling && "UL" === e.nextElementSibling.tagName && (e.setAttribute("href", "#"),
                        e.nextElementSibling.classList.add("dropdown-menu"),
                        e.nextElementSibling.classList.add("opacityIn"))
                })),
                    e.querySelectorAll("a").forEach((e => { e.nextElementSibling && "UL" === e.nextElementSibling.tagName && e.classList.add("dropdown-toggle") })),
                    e.querySelectorAll(":scope > a").forEach((e => { e.nextElementSibling && "UL" === e.nextElementSibling.tagName && e.setAttribute("data-bs-toggle", "dropdown") }))
            })),
            this.menuContainer.insertAdjacentElement("beforeend", this.menuHorizontal),
            document.querySelector("#menu").classList.add("show"),
            this._matchUrl(),
            this._initHorizontalMenu(),
            this._initIcons()
    }

 _initHorizontalMenu() {
        this._removeVerticalMenuListeners(),
        this._addHorizontalMenuListeners(),
        this._destroyScrollbar(),
        this._initOtherDropdownsHorizontal()
    }

 _initOtherDropdownsHorizontal() {
        this.userDropdown && this.userDropdown.dispose(),
        this.languageDropdown && this.languageDropdown.dispose(),
        this.notificationDropdown && this.notificationDropdown.dispose(),
        document.querySelector(".user-container .user") && (this.userDropdown = new bootstrap.Dropdown(document.querySelector(".user-container .user"),
            { popperConfig: function (e) { return { placement: "bottom-end" } } })),
        document.querySelector(".language-switch-container .language-button") && (this.languageDropdown = new bootstrap.Dropdown(document.querySelector(".language-switch-container .language-button"),
            { popperConfig: function (e) { return { placement: "bottom-end" } } })),
        document.querySelector(".menu-icons .notification-button") && (this.notificationDropdown = new bootstrap.Dropdown(document.querySelector(".menu-icons .notification-button"),
            { popperConfig: function (e) { return { placement: "bottom-end" } } }))
    }

 _initIcons() { "undefined" != typeof AcornIcons && (new AcornIcons).replace() } 
 
_removeHorizontalMenuListeners() {
        document.querySelectorAll("#menu > li").forEach((e => { e.removeEventListener("hidden.bs.dropdown", this._onHorizontalMenuDropdownHidden) })),
        document.querySelectorAll("#menu .dropdown-menu a.dropdown-toggle").forEach((e => { e.removeEventListener("click", this._onHorizontalMenuDropdownClick) }))
    }

 _addHorizontalMenuListeners() {
        this._removeHorizontalMenuListeners(),
        document.querySelectorAll("#menu > li").forEach((e => { e.addEventListener("hidden.bs.dropdown", this._onHorizontalMenuDropdownHidden) })),
        document.querySelectorAll("#menu .dropdown-menu a.dropdown-toggle").forEach((e => { e.addEventListener("click", this._onHorizontalMenuDropdownClick) }))
    }

 _onHorizontalMenuDropdownClick(e) {
        const t = e.currentTarget; e.stopPropagation(),
            e.preventDefault(); const i = t.closest(".dropdown-menu").querySelector(".show"); return i && !t.nextElementSibling.classList.contains("show") && (i.classList.remove("show"),
                i.querySelectorAll(".dropdown").forEach((e => { e.classList.remove("show") })),
                i.querySelectorAll(".dropdown-menu").forEach((e => { e.classList.remove("show") }))),
                "UL" === t.nextElementSibling.tagName && (t.nextElementSibling.classList.contains("show") ? (t.nextElementSibling.classList.remove("show"),
                    t.parentNode.classList.remove("show")) : (t.nextElementSibling.classList.add("show"),
                        t.parentNode.classList.add("show"))),
                !1
    }

 _onHorizontalMenuDropdownHidden(e) { this._hideDropdowns() } 
_matchUrl() {
        this.settings.matchUrl && (this._matchUrlByMenu("#menu"),
            this._matchUrlByMenu("#menuSide"))
    }

 _matchUrlByMenu(e) {
        const t = window.location.pathname.toLowerCase().replace(/^\/+/g, "").replace(/\.[^/.]+$/, ""); let i; if (document.querySelectorAll(e + " a").forEach((e => {
            const n = e.getAttribute("href").toLowerCase().replace(/^\/+/g, "").replace(/\.[^/.]+$/, ""),
            o = e.getAttribute("data-href") && e.getAttribute("data-href").toLowerCase().replace(/^\/+/g, "").replace(/\.[^/.]+$/, ""); (t.includes(n) || t.includes(o)) && (e.classList.add("active"),
                i = e)
        })),
            i) { for (var n = [], o = i; o && !(o = o.parentNode).matches(e);)o.matches("ul") && n.unshift(o); n.forEach((e => { e.previousElementSibling.matches("a") && e.previousElementSibling.classList.add("active") })) }
    }

 _initScrollbar() {
        "undefined" != typeof OverlayScrollbars && (this.scrollbar = OverlayScrollbars(document.querySelectorAll(".menu-container"),
            { scrollbars: { autoHide: "leave", autoHideDelay: 600 }, overflowBehavior: { x: "hidden", y: "scroll" } }))
    }

 _destroyScrollbar() {
        this.scrollbar && (this.scrollbar.destroy(),
            this.scrollbar = null)
    }

 _onWindowClick(e) { this.element.classList.contains("mobile-side-in") && !e.target.closest("#nav") && this._hideMobileMenu() } 
_initMenuPlacement() {
        var e = window.innerWidth, t = this.placementStatus; this._hideOtherDropdownsVertical(),
            "horizontal" === this.selectedMenuPlacement && (this.horizontalMobile > e ? 1 !== this.placementStatus && (this.html.setAttribute("data-placement", "horizontal"),
                this.html.setAttribute("data-dimension", "mobile"),
                this._addVerticalMenu(),
                this.placementStatus = 1, this._dispatchMobileEvent()) : 2 !== this.placementStatus && (this._hideMobileMenuQuick(),
                    this._addHorizontalMenu(),
                    this.html.setAttribute("data-dimension", "desktop"),
                    this.html.setAttribute("data-placement", "horizontal"),
                    this.placementStatus = 2, this._dispatchDesktopEvent())),
            "vertical" === this.selectedMenuPlacement && (this.verticalMobile > e ? 3 !== this.placementStatus && (this.html.setAttribute("data-dimension", "mobile"),
                this.html.setAttribute("data-placement", "horizontal"),
                this._addVerticalMenu(),
                this.placementStatus = 3, this._dispatchMobileEvent()) : 4 !== this.placementStatus && (this._hideMobileMenuQuick(),
                    this.html.setAttribute("data-dimension", "desktop"),
                    this.html.setAttribute("data-placement", "vertical"),
                    this._addVerticalMenu(),
                    this.placementStatus = 4, this._dispatchDesktopEvent())),
            this._initMenuBehaviour(),
            t !== this.placementStatus && this._removeAnimationAttributes()
    }

 _initMenuBehaviour() {
        var e = this.behaviourStatus, t = window.innerWidth, i = this.html.getAttribute("data-placement"); "vertical" === i && "unpinned" === this.selectedMenuBehaviour && (this.verticalMobile > t || this.verticalUnpinned <= t ? 1 !== this.behaviourStatus && (this.verticalUnpinned !== this.verticalMobile ? this.html.setAttribute("data-behaviour", "unpinned") : this.html.setAttribute("data-behaviour", "pinned"),
            this._enablePinButton(),
            this.behaviourStatus = 1, this._hideShowMenu()) : 2 !== this.behaviourStatus && (this.html.setAttribute("data-behaviour", "unpinned"),
                this._disablePinButton(),
                this.behaviourStatus = 2, this._hideShowMenu())),
            "vertical" === i && "pinned" === this.selectedMenuBehaviour && (this.verticalMobile > t || this.verticalUnpinned <= t ? 3 !== this.behaviourStatus && (this.html.setAttribute("data-behaviour", "pinned"),
                this._enablePinButton(),
                this.behaviourStatus = 3, this._unCollapseMenu()) : 4 !== this.behaviourStatus && (this.html.setAttribute("data-behaviour", "unpinned"),
                    this._disablePinButton(),
                    this.behaviourStatus = 4, this._hideShowMenu())),
            "horizontal" === i && "unpinned" === this.selectedMenuBehaviour && 5 !== this.behaviourStatus && (this.html.setAttribute("data-behaviour", "unpinned"),
                this._enablePinButton(),
                this.behaviourStatus = 5),
            "horizontal" === i && "pinned" === this.selectedMenuBehaviour && 6 !== this.behaviourStatus && (this.html.setAttribute("data-behaviour", "pinned"),
                this._enablePinButton(),
                this.behaviourStatus = 6),
            e !== this.behaviourStatus && this._removeAnimationAttributes()
    }

 _removeAnimationAttributes() { this.html.removeAttribute("data-menu-animate") } 
_collapseMenu() {
        document.querySelectorAll("#menu>li>a").forEach((e => { if ("true" === e.getAttribute("data-clicked")) { const t = bootstrap.Collapse.getInstance(e.nextElementSibling); t && t.hide() } 
})),
        this._hideDropdowns()
    }

 _unCollapseMenu() { document.querySelectorAll("#menu>li>a").forEach((e => { if ("true" === e.getAttribute("data-clicked")) { const t = bootstrap.Collapse.getInstance(e.nextElementSibling); t && t.show() } 
})) } 
_hideDropdowns() {
        [].slice.call(document.querySelectorAll('#menu>li>ul [data-bs-toggle="dropdown"]')).map((function (e) { if (e.classList.contains("show")) { const t = bootstrap.Dropdown.getInstance(e); t && t.hide() } 
})),
        document.querySelectorAll(".dropdown-menu .show").forEach((e => {
            e.classList.remove("show"),
            e.closest("ul") && e.closest("ul").classList.remove("show")
        })),
        this._hideOtherDropdownsVertical()
    }

 _enablePinButton() { this.settings.disablePinning || this.pinButton && this.pinButton.classList.remove("disabled") } 
_disablePinButton() { this.pinButton && this.pinButton.classList.add("disabled") } 
_onWindowResize(e) { this._initMenuPlacement() } 
_hideShowMenu() {
        if ("vertical" === this.html.getAttribute("data-placement") && "true" !== this.html.getAttribute("data-mobile") && "unpinned" === this.html.getAttribute("data-behaviour")) {
            var e = !1; if (document.querySelectorAll("#menu>li>a").forEach((t => { t.nextElementSibling && "UL" === t.nextElementSibling.tagName && t.nextElementSibling.classList.contains("collapsing") && (e = !0) })),
                e) 
                return void this._hideShowMenuDelayed(); 
                "show" === this.html.getAttribute("data-menu-animate") ? this._unCollapseMenu() : this._collapseMenu()
        } 
        clearTimeout(this.collapseTimeout)
    } 
    _hideShowMenuDelayed() {
        this.collapseTimeout && clearTimeout(this.collapseTimeout),
        this.collapseTimeout = setTimeout((() => { this._hideShowMenu() }),
            60)
    }

 _onMouseEnter(e) {
        "vertical" === this.html.getAttribute("data-placement") && "true" !== this.html.getAttribute("data-mobile") && "unpinned" === this.html.getAttribute("data-behaviour") && (this.html.setAttribute("data-menu-animate", "show"),
            setTimeout((() => { this._initOtherDropdownsVertical() }),
                Globals.transitionTime),
            this._hideShowMenuDelayed())
    }

 _onMouseLeave(e) {
        "vertical" === this.html.getAttribute("data-placement") && "true" !== this.html.getAttribute("data-mobile") && "unpinned" === this.html.getAttribute("data-behaviour") && (this.html.setAttribute("data-menu-animate", "hidden"),
            this._hideShowMenuDelayed(),
            this._hideOtherDropdownsVertical())
    }

 _onMenuPlacementChange(e) { this.selectedMenuPlacement = e.detail, this._initMenuPlacement() } 
_onMenuBehaviourChange(e) { this.selectedMenuBehaviour = e.detail, this._initMenuBehaviour() } 
_onWindowScroll(e) { this.windowScrolled = !0 }

 _onWindowScrollInterval() {
        if (this.windowScrolled) {
            var e = window.pageYOffset, t = this.element.offsetHeight; if (this.windowScrolled = !1, Math.abs(this.prevScrollpos - e) <= t && e > t) return void (this.prevScrollpos = e); "horizontal" === this.html.getAttribute("data-placement") && "true" !== this.html.getAttribute("data-mobile") && "unpinned" === this.html.getAttribute("data-behaviour") && (this.prevScrollpos > e || e <= t ? this._removeAnimationAttributes() : this.prevScrollpos <= e && e > t && (this.html.setAttribute("data-menu-animate", "hidden"),
                this._hideDropdowns())),
                this.prevScrollpos = e
        }
    }

 _onPinClick(e) {
        e.preventDefault(),
        this.pinButton.classList.contains("disabled") || this.html.dispatchEvent(new CustomEvent(Globals.pinButtonClick))
    }

 _onColorClick(e) {
        e.preventDefault(),
        this.html.dispatchEvent(new CustomEvent(Globals.lightDarkModeClick))
    } 
    _showMobileMenu(e) {
        e.preventDefault(),
        this.html.setAttribute("data-mobile", "true"),
        this.element.classList.add("mobile-top-out"),
        this.element.classList.remove("mobile-top-in"),
        this.element.classList.remove("mobile-top-ready"),
        setTimeout((() => {
            this.element.classList.remove("mobile-top-out"),
            this.element.classList.add("mobile-side-ready")
        }),

        200),

        setTimeout((() => { this.element.classList.add("mobile-side-in") }),
            230)
    }

 _hideMobileMenu() {
        this.element.classList.add("mobile-side-out"),
        this.element.classList.remove("mobile-side-in"),
        setTimeout((() => {
            this.element.classList.remove("mobile-side-ready"),
            this.element.classList.remove("mobile-side-out"),
            this.element.classList.add("mobile-top-ready")
        }),
            200),
        setTimeout((() => {
            this.element.classList.add("mobile-top-in"),
            this.html.removeAttribute("data-mobile")
        }),
            230)
    } 
    _hideMobileMenuQuick() {
        this.element.classList.remove("mobile-top-out"),
        this.element.classList.remove("mobile-top-in"),
        this.element.classList.remove("mobile-top-ready"),
        this.element.classList.remove("mobile-side-in"),
        this.element.classList.remove("mobile-side-ready"),
        this.element.classList.remove("mobile-side-out"),
        this.html.removeAttribute("data-mobile")
    } 
    _dispatchDesktopEvent() { this.html.dispatchEvent(new CustomEvent(Globals.switchedToDesktop)) } 

    _dispatchMobileEvent() { this.html.dispatchEvent(new CustomEvent(Globals.switchedToMobile)) }
}