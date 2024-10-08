class EditorControls {
    constructor() {
        "undefined" != typeof Quill ?
        (this.quillToolbarOptions = [
            ["bold", "italic", "underline", "strike"],
            ["blockquote", "code-block"],
            [{ list: "ordered" }, { list: "bullet" }],
            [{ indent: "-1" }, { indent: "+1" }],
            [{ size: ["small", !1, "large", "huge"] }],
            [{ header: [1, 2, 3, 4, 5, 6, !1] }],
            [{ font: [] }],
            [{ align: [] }],
            ["clean"]
        ],
            this.quillBubbleToolbarOptions = [
                ["bold", "italic", "underline", "strike"],
                [{ header: [1, 2, 3, 4, 5, 6, !1] }],
                [{ list: "ordered" }, { list: "bullet" }],
                [{ align: [] }]
            ],
            this._initStandardEditor(),
            this._initQuillBubble(),
            this._initQuillFilled(),
            this._initQuillTopLabel(),
            this._initQuillFloatingLabel()) : console.log("Quill is undefined!")
    }

    _initStandardEditor() {
        document.getElementById("quillEditor") &&
            new Quill("#quillEditor",
                {
                    modules: {
                        toolbar: this.quillToolbarOptions,
                        active: {}
                    },
                    theme: "snow",
                    placeholder: "Description"
                })
    }

    _initQuillBubble() {
        document.getElementById("quillEditorBubble") &&
            new Quill("#quillEditorBubble", {
                modules: {
                    toolbar: this.quillBubbleToolbarOptions,
                    active: {}
                },
                theme: "bubble"
            }
            )
    }

    _initQuillFilled() {
        document.getElementById("quillEditorFilled") &&
            new Quill(
                "#quillEditorFilled",
                {
                    modules: {
                        toolbar: this.quillBubbleToolbarOptions,
                        active: {}
                    },
                    theme: "bubble",
                    placeholder: "Heading"
                }
            )
    }

    _initQuillTopLabel() {
        document.getElementById("quillEditorTopLabel") &&
            new Quill(
                "#quillEditorTopLabel",
                {
                    modules: {
                        toolbar: this.quillBubbleToolbarOptions,
                        active: {}
                    },
                    theme: "bubble"
                }
            )
    }

    _initQuillFloatingLabel() {
        if (document.getElementById("quillEditorFloatingLabel")) {
            const l = new Quill("#quillEditorFloatingLabel",
                {
                    modules: {
                        toolbar: this.quillBubbleToolbarOptions,
                        active: {}
                    },
                    theme: "bubble"
                }
            );
            l.on(
                "editor-change",
                (
                    function (i, ...e) {
                        l.getLength() > 1 ?
                            document.getElementById("quillEditorFloatingLabel").classList.add("full") :
                            document.getElementById("quillEditorFloatingLabel").classList.remove("full")
                    }
                )
            )
        }
    }
}