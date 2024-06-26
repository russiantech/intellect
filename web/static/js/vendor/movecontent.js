class MoveContent{
    get options(){return{targetSelector:"",moveBreakpoint:"",beforeMove:null,afterMove:null}}
    
    constructor(t,e={}){
        this.settings=Object.assign(this.options,e),
        this.content="",
        this.currentPlacement=null,this.sourceContainer=t,
        this.targetContainer=document.querySelector(this.settings.targetSelector),
        this.targetContainer?this._init():console.error("No target container for move content")
    }
    
    _init(){
        this.content=this.sourceContainer.innerHTML,
        this.sourceContainer.innerHTML="",
        this.breakpoint=parseInt(Globals[this.settings.moveBreakpoint]),
        window.addEventListener("resize",(t=>{this._onWindowResize(t)})),
        this._onWindowResize(null)
    }
    
    _onWindowResize(t){
        window.innerWidth>=this.breakpoint?
        "target"!==this.currentPlacement&&(this.currentPlacement="target",this._moveToTarget()) :
        this.movedToSmaller||"source"!==this.currentPlacement&&(this.currentPlacement="source",this._moveToSource())
    }
        
    _moveToSource(){
        this._clearBoth(),
        this.sourceContainer.insertAdjacentHTML("beforeend",this.content),
        this.settings.afterMove&&this.settings.afterMove(this.currentPlacement)
    }
    
    _moveToTarget(){
        this._clearBoth(),
        this.targetContainer.insertAdjacentHTML("beforeend",this.content),
        this.settings.afterMove&&this.settings.afterMove(this.currentPlacement)
    }
    
    _clearBoth(){
        this.settings.beforeMove&&this.settings.beforeMove(this.currentPlacement),
        this.sourceContainer.innerHTML="",this.targetContainer.innerHTML=""}
    
    }
