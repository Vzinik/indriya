$("form[name=signup_form").submit(function(e){
    var $form = $(this);
    var $error =$form.find(".error");
    var data = $form.serialize();
    var $password = $form.find("input[name=password]");
    var $confirmPassword = $form.find("input[name=confirm_password]");

    if ($password.val() !== $confirmPassword.val()) {
        $error.text("Passwords do not match.").removeClass("error--hidden");
        e.preventDefault();
        return;
    }
    
    $.ajax({
        url: "/user/signup/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp);
            window.location.href= "/dashboard/";
        },
        error: function(resp){
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
})



$("form[name=login_form").submit(function(e){
    var $form = $(this);
    var $error =$form.find(".error");
    var data = $form.serialize();
    

    $.ajax({
        url: "/user/login/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            console.log(resp);
            window.location.href= "/dashboard/";
        },
        error: function(resp){
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
})