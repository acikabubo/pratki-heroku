function loading(){
    $(".loading").fadeIn(3000);
    $(".content").fadeOut(2000);
}

$("#l-submit" ).click(function() {
    loading();
});

$(window).on('load', function(){
    $(".loading").fadeOut('slow');
});
