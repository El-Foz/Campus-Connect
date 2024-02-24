var periods=document.getElementById("per")
var days=document.getElementById("days")
var schedule=document.getElementById("schedule")
function resizeTable(){
    schedule.innerHTML=''
    for(var i=0; i<parseInt(periods.value); i++){
        var entry=document.createElement("TR")
        for(var c=0; c<parseInt(days.value); c++){
            var val=document.createElement("TH")
            var input=document.createElement("INPUT")
            input.type="checkbox"
            val.appendChild(input)
            entry.appendChild(val)
        }
        schedule.append(entry)
    }
}