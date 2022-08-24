$(document).ready(function(e){
    $(".toggleMenu").click(function(e){
        $(this).toggleClass("active");
        $(".sidebar,body").toggleClass("active");
    });
    $(".hasChild > a").click(function(e){
        e.preventDefault();
        if($(this).parents(".hasChild").find(".submenu").css("display") == "none"){
            $(this).parents(".hasChild").find(".submenu").slideToggle();
        }
        else{
            $(".submenu").slideUp();
        }
    });
    $(".coupan_head_text").click(function(e){
        $(this).toggleClass("active");
        $(".coupan_body").slideToggle();
    })
    $(".menu_icon_mobile").click(function(e){
        $(this).toggleClass("active");
        $(".header_menu").toggleClass("active");
    })
});
