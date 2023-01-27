const submit_button = document.getElementById("Submit");
const data = document.getElementById("info");

    submit_button.onclick = function(){
        var major_code = document.getElementById("m_code").value;
        var area = document.getElementById("area").value;
        var l_cost = document.getElementById("l_cost").value;                
        var h_cost = document.getElementById("h_cost").value;
        var miles = document.getElementById("miles_from_home").value;                
        var SAT = document.getElementById("sat").value;
        var GPA = document.getElementById("gpa").value;                
        var l_accept = document.getElementById("l_acceptance").value;
        var h_accept = document.getElementById("h_acceptance").value;    
        const dict_values = {major_code, area, l_cost, h_cost, miles, SAT, GPA, l_accept, h_accept} //Pass the javascript variables to a dictionary.
        const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
        console.log(s); // Prints the variables to console window, which are in the JSON format
        //window.alert(s);
        $.ajax({
            url:"/calculate",
            type:"POST",
            contentType: "application/json",
            data: JSON.stringify(s),
            success: function(result) {
                console.log(result);
                var temp = JSON.parse(result)
                data.innerHTML = temp.rank;
            },
            error: function(error){
                console.log(error)
            }
        }); 
}

const add_button = document.getElementById('Add_Button');
add_button.onclick = function(){
    var major_code = document.getElementById("m_code").value;
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
    const dict_values = {major_code, area, l_cost, h_cost, miles, SAT, GPA, l_accept, h_accept, zip, college, c_ID}
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