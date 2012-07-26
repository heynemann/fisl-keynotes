$(function() {
    // Brazilian Portuguese 
    jQuery.timeago.settings.strings = {
       suffixAgo: "atrás",
       suffixFromNow: "",
       seconds: "alguns segundos",
       minute: "daqui a um minuto",
       minutes: "daqui a %d minutos",
       hour: "daqui a uma hora",
       hours: "daqui a %d horas",
       day: "daqui a um dia",
       days: "daqui a %d dias",
       month: "daqui a um mês",
       months: "daqui a %d meses",
       year: "daqui a um ano",
       years: "daqui a %d anos"
    };
    jQuery.timeago.settings.allowFuture = true;
    $('.talks .talk .info .location .time').timeago();

    var talks = $('.talks');
    var currTalks = $('.current-talks');

    $('.talks .talk').click(function(ev) {
        if ($(this).is('.current')) {
            talks.removeClass('has-current');
            $(this).toggleClass('current').detach().prependTo(talks);
        } else {
            talks.addClass('has-current');
            $(this).toggleClass('current').detach().appendTo(currTalks);
        }
    });

    var top = false;
    window.setTimeout(function() {
        $('.talks').autoscroll({
            direction: "down", 
            step: 20, 
            delay: 5000,
            speed: "fast",
            scroll: true,
            onEdge: function (edge) { 
                var element = $(this);
                element.autoscroll('pause');
                element.autoscroll('reverse');
                if (top) {
                    window.setTimeout(function() {
                        element.autoscroll('resume');
                    }, 5000);
                } else {
                    element.autoscroll('resume');
                }
                top = !top;
            }
        });
    }, 5000);
});
