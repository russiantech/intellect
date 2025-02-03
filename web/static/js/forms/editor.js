class EditorControls {

    headerEditor = document.getElementById("headerEditor") ;
    headField = document.getElementById("headerField");
    contentEditor = document.getElementById("contentEditor") ;
    contentField = document.getElementById("contentField");

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

                /* custom */
                this._initHeaderEditor(),
                this._initContentEditor()

            ) : console.log("Quill is undefined!")
    }

    _initContentEditor(){
        if(this.contentEditor){
        const c = new Quill(
            this.contentEditor,
            {
                modules:{
                toolbar:this.quillToolbarOptions,
                active:{}
            },
            theme:"snow", 
            placeholder:"Description"
            }
        )

        c.on( 'editor-change', (()=>{this.contentField ? this.contentField.value = c.getText() : console.log('specify an id (contentField) in form')})  )

        }
    }
    
    _initHeaderEditor() {
        if (this.headerEditor) {
            const h = new Quill(
                this.headerEditor,
                {
                    modules: {
                        toolbar: this.quillBubbleToolbarOptions,
                        active: {}
                    },
                    theme: "bubble",
                    placeholder: "Heading"
                }
            ); 
            h.on(
                "editor-change",
                (
                    () => {
                        //"undefined" != this.headField ? this.headField.value = h.getText() : alert('id not specified on any form element');
                        this.headField ? this.headField.value = h.getText() : console.log('missing id "headerField", that\'s why heading not set')
                        //if(this.headField){this.headField.value = h.getText()}
                    }
                )
            )
        }
    }

}
