class QuizDetail { 
    constructor() { this._initTimer() } 
    _initTimer() { 
        if ("undefined" != typeof Countdown) { 
            var i = new Date((new Date).setMinutes((new Date).getMinutes() + 15)); 
            new Countdown({ selector: "#timer", 
            leadingZeros: !0, msgBefore: "", msgAfter: "", 
            msgPattern: 
            '\n<div class="row gx-5">\n<div class="col-auto">\n<div class="display-5 text-primary mb-1">{minutes}</div>\n<div>Minutes</div>\n </div>\n <div class="col-auto">\n<div class="display-5 text-primary mb-1">{seconds}</div>\n<div>Seconds</div>\n   </div>\n</div>', 
            dateEnd: i }) 
        } }  }