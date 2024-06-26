class Helpers {
    static Debounce(t, e, r) {
        var n; 
        return function () {
            var s = this, 
            o = arguments, 
            a = function () { n = null, r || t.apply(s, o) },
            c = r && !n; 
            clearTimeout(n), 
            n = setTimeout(a, e),
            c && t.apply(s, o)
        }
    }
    static NextId(t, e) {
        if (!t) return void console.error("NextId data is null");
        const r = t.reduce((function (t, r) { return +parseInt(r[e]) > +parseInt(t[e]) ? r : t }));
        return parseInt(r[e]) + 1
    }

    static FetchJSON(t, e) {
        fetch(t).then((t => {
            if (!t.ok) throw new Error("Network response was not ok");
            return t
        })).then((t => t.json())).then((t => e(t))).catch((t => { console.error("Problem with the fetching JSON data: ", t) }))
    }
    static AddCommas(t) {
        for (var e = (t += "").split("."), r = e[0], n = e.length > 1 ? "." + e[1] : "", s = /(\d+)(\d{3})/; s.test(r);)r = r.replace(s, "$1,$2");
        return r + n
    }
    static UrlFix(t) {
        const e = document.documentElement.dataset.urlPrefix;
        if (!e) return t; return `${e.endsWith("/") ? e : `${e}/`}${t.startsWith("/") ? t.slice(1, t.length) : t}`
    }
}