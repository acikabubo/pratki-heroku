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
