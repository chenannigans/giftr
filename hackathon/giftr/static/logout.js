$('#logout_btn').click(function() {    
    console.log("HERE");
    $.ajax({
        url: 'lemme',
        method: 'GET', // or another (GET), whatever you need
        success: function (data) {   
            console.log("FUCKIG YEA"); 
            // success callback
            // you can process data returned by function from views.py
        }
    });
});