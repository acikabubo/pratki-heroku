$('#info-body').ready(function() {
    var frame = setInterval(function(){
        $('.cache-timer').each(function() {
            var count = parseInt($(this).html());
            if (count !== 1) {
                $(this).html(--count);
            } else {
                clearInterval(frame);
                $(this).html('');
            }
        });
    }, 1000);
});
