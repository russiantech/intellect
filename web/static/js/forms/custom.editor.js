class EditorControls{
    constructor(){

        /* customed */
        const headField = document.getElementById('headings');
        const contentField = document.getElementById('contents');


        "undefined" !=typeof Quill ?

        (this.quillToolbarOptions=[
            ["bold","italic","underline","strike"],
            ["blockquote","code-block"],
            [{list:"ordered"},{list:"bullet"}],
            [{indent:"-1"}, {indent:"+1"}],
            [{size:["small", !1, "large", "huge"]}],
            [{header:[1, 2, 3, 4, 5, 6, !1]}],
            [{font:[]}],
            [{align:[]}],
            ["clean"]
        ],
        this.quillBubbleToolbarOptions=[
            ["bold","italic","underline","strike"],
            [{header:[1,2,3,4,5,6,!1]}],
            [{list:"ordered"},{list:"bullet"}],
            [{align:[]}]
        ],
        this._initStandardEditor(),
        this._initQuillBubble(),
        this._initQuillFilled(),
        this._initQuillTopLabel(),
        this._initQuillFloatingLabel(),

        /* custom */
        this._initHeaderEditor(),
        this._initContentEditor()

        ) : console.log("Quill is undefined!")
    }

    /**
     * my custom editors
     */

    _initContentEditor(){
        document.getElementById("contentEditor")&&
        new Quill(
            "#contentEditor",
            {
                modules:{
                toolbar:this.quillToolbarOptions,
                active:{}
            },
            theme:"snow", 
            placeholder:"Description"
        }
    )
    }

    _initHeaderEditor(){
        document.getElementById("headerEditor") &&
        new Quill(
            "#headerEditor",
            {
                modules:{
                toolbar:this.quillBubbleToolbarOptions,
                active:{}
                }, 
                theme:"bubble", 
                placeholder:"Heading"
            }
        )//.on('editor-change', function(){alert('changed'); document.getElementById('headings').innerHTML=this.getText();});

    }

    _initHeaderEditor(){
        if(document.getElementById("headerEditor")){
            const h = new Quill(
                "#headerEditor",
                {
                    modules:{toolbar:this.quillBubbleToolbarOptions,
                    active:{}},
                    theme:"bubble",
                    placeholder:"Heading"
                }
            );
        h.on(
            "editor-change",
            (
                function(){
                    //alert( h.getText()) //text-typed in
                    'undefined' != typeof this.headField ? 
                    alert('it\'s defined') : 'Header-filed is blank or Not defined';
                    //this.headField.innerHTML = h.getText() : 'Header-filed is blank or Not defined';
                    //this.headField.innerHTML = h.getText();
                   // this.headField.value = h.getText();
                    //return this.value = h.getText();
                    //console.log(h.getText())
                    //document.getElementById('headings').innerHTML=h.getText();
                    //h.getLength() > 1 ? console.log(h.getText()) : 'Header-filed is blank';
                }
            )
        )
        }
    }

/*
    var editor = new Quill('#quillEditor', options);
    var preciousContent = document.getElementById('myPrecious');
    var justTextContent = document.getElementById('justText');
    var justHtmlContent = document.getElementById('justHtml');

    editor.on('text-change', function() {
    var delta = editor.getContents();
    var text = editor.getText();
    var justHtml = editor.root.innerHTML;
    preciousContent.innerHTML = JSON.stringify(delta);
    justTextContent.innerHTML = text;
    justHtmlContent.innerHTML = justHtml;
    }); */

    /**
     * end custom editors
     */
    ////////////////////////////////////////////////


    _initStandardEditor(){
        document.getElementById("quillEditor")&&
        new Quill(
            "#quillEditor",
            {
                modules:{
                toolbar:this.quillToolbarOptions,
                active:{}
            },
            theme:"snow", 
            placeholder:"Description"
        }
    )
    }

    _initQuillBubble(){
        document.getElementById("quillEditorBubble")&&
        new Quill(
            "#quillEditorBubble",
            {
            modules:{
                toolbar:this.quillBubbleToolbarOptions,
                active:{}
            },
                theme:"bubble"
            }
            )
            }

    _initQuillFilled(){
        document.getElementById("quillEditorFilled")&&
        new Quill(
            "#quillEditorFilled",
            {modules:{
                toolbar:this.quillBubbleToolbarOptions,
                active:{}
            }, 
            theme:"bubble", 
            placeholder:"Heading"
        }
        )
    }

    _initQuillTopLabel(){
        document.getElementById("quillEditorTopLabel")&&
        new Quill(
            "#quillEditorTopLabel",
            {
                modules:{
                    toolbar:this.quillBubbleToolbarOptions,
                    active:{}
                },
            theme:"bubble"
            }
        )
    }

    _initQuillFloatingLabel(){
        if(document.getElementById("quillEditorFloatingLabel")){
            const l = new Quill(
                "#quillEditorFloatingLabel",
                {
                    modules:{toolbar:this.quillBubbleToolbarOptions,
                    active:{}},
                    theme:"bubble"
                }
            );
        l.on(
            "editor-change",
            (
                function(i,...e){
                l.getLength() > 1 ?
                document.getElementById("quillEditorFloatingLabel").classList.add("full"):
                document.getElementById("quillEditorFloatingLabel").classList.remove("full")
            }
            )
        )
        }
    }
}


document.load(function(){
    document.getElementById('headings').innerHTML=h.getText();
});