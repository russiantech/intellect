class Scripts {
    constructor() {
        this._initSettings(),
        this._initVariables(),
        this._addListeners(),
        this._init()
    }

    _init() {
        setTimeout((() => {
            document.documentElement.setAttribute("data-show", "true"),
                document.body.classList.remove("spinner"),
                this._initBase(),
                this._initCommon(),
                this._initPages(),
                //this._initTimer(),
                this._initForms()
        }), 50)
    }

    _initBase() {
        if ("undefined" != typeof Nav) { new Nav(document.getElementById("nav")) }
        if ("undefined" != typeof Search) { new Search } "undefined" != typeof AcornIcons && (new AcornIcons).replace()
    }

    _initCommon() { if ("undefined" != typeof Common) { new Common } }

    _initPages() {
        if ("undefined" != typeof ElearningDashboard) { new ElearningDashboard }
        if ("undefined" != typeof SchoolDashboard) { new SchoolDashboard }
        if ("undefined" != typeof CourseDetail) { new CourseDetail }
        if ("undefined" != typeof CourseList) { new CourseList }
        if ("undefined" != typeof CourseExplore) { new CourseExplore }
        if ("undefined" != typeof InstructorList) { new InstructorList }
        if ("undefined" != typeof InstructorDetail) { new InstructorDetail }
        if ("undefined" != typeof QuizDetail) { new QuizDetail }
        if ("undefined" != typeof PathList) { new PathList }
        if ("undefined" != typeof PathDetail) { new PathDetail }
        if ("undefined" != typeof MiscPlayer) { new MiscPlayer }
        if ("undefined" != typeof MiscSyllabus) { new MiscSyllabus }
        //
        if ("undefined" != typeof TagControls) { new TagControls } //initialize-tags
        
        if ("undefined" != typeof AccountSettings) { new AccountSettings } //initialize editor-page

     //   if ("undefined" != typeof ProfileSettings) { new ProfileSettings } 
     //   if ("undefined" != typeof ProfileStandard) { new ProfileStandard }  

        /*
        if ("undefined" != typeof Analysis) { new Analysis } 
        if ("undefined" != typeof Communitylist) { new Communitylist } 
        if ("undefined" != typeof ServicesDatabase) { new ServicesDatabase } 
        if ("undefined" != typeof ServicesDatabaseAdd) { new ServicesDatabaseAdd } 
        if ("undefined" != typeof ServicesDatabaseDetail) { new ServicesDatabaseDetail } 
        if ("undefined" != typeof ServicesStorage) { new ServicesStorage } 
        if ("undefined" != typeof SupportDocs) { new SupportDocs } 
        if ("undefined" != typeof SupportTicketsDetail) { new SupportTicketsDetail } 
        */
    }

    /*
    _initTimer() {
        if ("undefined" != typeof Countdown) {
            var i = new Date((new Date).setMinutes((new Date).getMinutes() + 15));
            new Countdown(
                {
                    selector: "#timer", 
                    leadingZeros: !0, 
                    msgBefore: "", 
                    msgAfter: "", 
                    msgPattern: '\n \
                    <div class="row gx-5">\n <div class="col-auto">\n  \
                    <div class="display-5 text-primary mb-1">{minutes}</div>\n \
                    <div>Minutes</div>\n </div>\n<div class="col-auto">\n  \
                    <div class="display-5 text-primary mb-1">{seconds}</div>\n \
                    <div>Seconds</div>\n</div>\n </div>', 
                    dateEnd: i
                });
        }
    }
        */
    _initForms() {
        if ("undefined" != typeof FormLayouts) { new FormLayouts }
        if ("undefined" != typeof FormValidation) { new FormValidation }
        if ("undefined" != typeof FormWizards) { new FormWizards }
        if ("undefined" != typeof InputMask) { new InputMask }
        if ("undefined" != typeof GenericForms) { new GenericForms }
        if ("undefined" != typeof AutocompleteControls) { new AutocompleteControls }
        if ("undefined" != typeof DatePickerControls) { new DatePickerControls }
        if ("undefined" != typeof DropzoneControls) { new DropzoneControls }
        if ("undefined" != typeof EditorControls) { new EditorControls }
        if ("undefined" != typeof SpinnerControls) { new SpinnerControls }
        if ("undefined" != typeof RatingControls) { new RatingControls }
        if ("undefined" != typeof Select2Controls) { new Select2Controls }
        if ("undefined" != typeof SliderControls) { new SliderControls }
        if ("undefined" != typeof TagControls) { new TagControls }
        if ("undefined" != typeof TimePickerControls) { new TimePickerControls }
    }

    _initSettings() {
        if ("undefined" != typeof Settings) {
            new Settings({
                attributes: { placement: "vertical", layout: "boxed", behaviour: "unpinned", color: "dark-purple" },
                showSettings: !0, storagePrefix: "acorn-elearning-portal-"
            })
        }
    }

    _initVariables() { if ("undefined" != typeof Variables) { new Variables } }
    _addListeners() {
        document.documentElement.addEventListener(Globals.menuPlacementChange, 
            (e => { setTimeout((() => { window.dispatchEvent(new Event("resize")) }), 25) })),
            document.documentElement.addEventListener(Globals.layoutChange, 
                (e => { setTimeout((() => { window.dispatchEvent(new Event("resize")) }), 25) })),
            document.documentElement.addEventListener(Globals.menuBehaviourChange, (
                e => { setTimeout((() => { window.dispatchEvent(new Event("resize")) }), 25) }))
    }
}
window.addEventListener("DOMContentLoaded", (() => { void 0 !== Scripts && new Scripts })),
    "undefined" != typeof Dropzone && (Dropzone.autoDiscover = !1);
