
const add_button = document.getElementById('Add_Button');
add_button.onclick = function(){
    var major_code = document.getElementById("m_code").value;
    var major_name = document.getElementById("major_name").value;
    var area = document.getElementById("area").value;
    var l_cost = document.getElementById("l_cost").value;                
    var h_cost = document.getElementById("h_cost").value;
    var miles = document.getElementById("miles_from_home").value;                
    var SAT = document.getElementById("sat").value;
    var GPA = document.getElementById("gpa").value;                
    var l_accept = document.getElementById("l_acceptance").value;
    var h_accept = document.getElementById("h_acceptance").value;    
    var zip = document.getElementById("zip_code").value;
    var college = document.getElementById("college").value;    
    var c_ID= document.getElementById("c_id").value;
    const dict_values = {major_code, major_name, area, l_cost, h_cost, miles, SAT, GPA, l_accept, h_accept, zip, college, c_ID}
    const s = JSON.stringify(dict_values);
    console.log(s); 

    $.ajax({
        url:"/write_to_db",
        type:"POST",
        contentType: "application/json",
        data: JSON.stringify(s),
        success: function(result) {
            console.log(result);
        },
        error: function(error){
            console.log(error)
        }
    }); 
}

var list_of_colleges = [];
const fs = require('fs');
fs.readFile('CollegexTinder\\csv\\test.txt', (err, inputD) => {
   if (err) throw err;
      console.log(inputD.toString());
      list_of_colleges.push(inputD.toString());
})
console.log(list_of_colleges)


function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments, the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
          /*check if the item starts with the same letters as the text field value:*/
          if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
            /*create a DIV element for each matching element:*/
            b = document.createElement("DIV");
            /*make the matching letters bold:*/
            b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
            b.innerHTML += arr[i].substr(val.length);
            /*insert a input field that will hold the current array item's value:*/
            b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
            /*execute a function when someone clicks on the item value (DIV element):*/
                b.addEventListener("click", function(e) {
                /*insert the value for the autocomplete text field:*/
                inp.value = this.getElementsByTagName("input")[0].value;
                /*close the list of autocompleted values, (or any other open lists of autocompleted values:*/
                closeAllLists();
            });
            a.appendChild(b);
          }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
          /*If the arrow DOWN key is pressed, increase the currentFocus variable:*/
          currentFocus++;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 38) { //up
          /*If the arrow UP key is pressed, decrease the currentFocus variable:*/
          currentFocus--;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 13) {
          /*If the ENTER key is pressed, prevent the form from being submitted,*/
          e.preventDefault();
          if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            if (x) x[currentFocus].click();
          }
        }
    });
    function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      /*add class "autocomplete-active":*/
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document, except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
  }

  var college_input = document.getElementById("college");
  college_input.onchange = function(){
    autocomplete(document.getElementById("college"), list_of_colleges);
  }
