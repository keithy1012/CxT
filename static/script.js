const button = document.getElementById("Submit");
const data = document.getElementById("info");

    button.onclick = function(){
        var major_code = document.getElementById("m_code").value;
        var area = document.getElementById("area").value;
        var l_cost = document.getElementById("l_cost").value;                
        var h_cost = document.getElementById("h_cost").value;
        var miles = document.getElementById("miles_from_home").value;                
        var SAT = document.getElementById("sat").value;
        var GPA = document.getElementById("gpa").value;                
        var l_accept = document.getElementById("l_acceptance").value;
        var h_accept = document.getElementById("h_acceptance").value;    
        //var zip = document.getElementById("zip_code").value;

        //const dict_values = {major_code, area, l_cost, h_cost, miles, SAT, GPA, l_accept, h_accept, zip}
        const dict_values = {major_code, area, l_cost, h_cost, miles, SAT, GPA, l_accept, h_accept} //Pass the javascript variables to a dictionary.
        const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
        console.log(s); // Prints the variables to console window, which are in the JSON format
        //window.alert(s);
        $.ajax({
            url:"/test",
            type:"POST",
            contentType: "application/json",
            data: JSON.stringify(s),
            success: function(result) {
                console.log(result);
                data.innerHTML = result;
            },
            error: function(error){
                console.log(error)
            }
        });

      
}