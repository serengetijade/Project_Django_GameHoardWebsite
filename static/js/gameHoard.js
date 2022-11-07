//----------ADD ITEM MODAL----------
//STICKY ADDGAME FORM
function openaddGame(){
    document.getElementById("add-item").style.display = "block";
}

function closeForm() {
    document.getElementById("add-item").style.display = "none";
}

//CLOSE FORM IF USER CLICKS OUTSIDE THE CONTACT-CONTAINER WINDOW
document.addEventListener("click",
    function(event){
        if (
          event.target.matches("#add-item")
          )
          {closeForm()}
        }
);

//TOGGLE DISPLAY of GAME.DB as a TABLE
function showHideElement() {
    //document.getElementById("gameLibraryTable").style.width="100%";
    var peekaboo = document.getElementById("gameDBtable");
    if (peekaboo.style.display === "none") {
        peekaboo.style.display = "table";   //Ensure you choose the appropriate display option, i.e. block, inline, table, etc.
        var text = document.getElementById("showHideElement").innerHTML ="&nbsp;Hide List&nbsp;";
    }
    else {
        peekaboo.style.display = "none";
        var text = document.getElementById("showHideElement").innerHTML ="Show List";
    }
}
//----------ADD ITEM MODAL----------


//----------DELETE ITEM MODAL----------
//DELETE FORM modal
function opendeletemodal(){
    document.getElementById("delete-item").style.display = "block";
}

function closedeletemodal() {
    document.getElementById("delete-item").style.display = "none";
}

//CLOSE FORM IF USER CLICKS OUTSIDE THE CONTACT-CONTAINER WINDOW
document.addEventListener("click",
    function(event){
        if (
          event.target.matches("#delete-item")
          )
          {closedeletemodal()}
        }
);
//----------DELETE ITEM MODAL----------