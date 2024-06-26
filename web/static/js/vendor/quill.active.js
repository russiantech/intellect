const Active = function (t, s) {
    this.quill = t, this.options = s, this.container = t.container, this.activeClass = s.activeClass || "active";
    this.quill.on("selection-change",
        ((t, s, i) => {
            null === t && null !== s ? this.container.parentNode.classList.contains("editor-container") ?
                this.container.parentNode.classList.remove(this.activeClass) : this.container.classList.remove(this.activeClass) : null !== t && null === s && (this.container.parentNode.classList.contains("editor-container") ? this.container.parentNode.classList.add(this.activeClass) : this.container.classList.add(this.activeClass))
        }))
};
"undefined" != typeof module && void 0 !== module.exports && (module.exports = Active);