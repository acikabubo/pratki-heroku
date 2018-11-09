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

$('#info-body').ready(function() {
    // Function to update counters on all elements with class counter
    var frame = function() {
        $('.cache-timer').each(function() {
            var count = parseInt($(this).html());
            if (count !== 1) {
                $(this).html(--count);
            } else {
                $(this).html('');
                return false;
            }
        });
    };

    // Schedule the update to happen once every second
    setInterval(frame, 1000);
});

$('.message a').click(function(){
   $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});

var $checks = $("input[type='checkbox']").change(function() {
    var checked = $checks.is(':checked');
    $("#rm_pkgs").toggle(checked);
});
$checks.first().change();

// $('#rm_pkgs').click(function(){
$('#confirmed').click(function(){
    var pkgs = [];
    $.each($("input[name='rm_pkg']:checked"), function(){
        pkgs.push($(this).val());
    });

    if (pkgs.length == 0) {
        alert('Please choose at least one value.');
    }
    else {
        data = JSON.stringify(pkgs);

        $.ajax({
            url: '/delete_pkgs/' + data + '/',
            type: 'DELETE',
            success: function(result) {
                window.location.replace("/info");
            }
        });
    }
});

$("#username").attr("placeholder", $("#logged-username").text());
