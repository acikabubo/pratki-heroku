$('.cache-timer').ready(function() {
    // Function to update counters on all elements with class counter
    var doUpdate = function() {
        $('.cache-timer').each(function() {
            var count = parseInt($(this).html());
            if (count !== 1) {
                $(this).html(--count);
            } else {
                $(this).html('');
            }
        });
    };

    // Schedule the update to happen once every second
    setInterval(doUpdate, 1000);
});