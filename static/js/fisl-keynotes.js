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

    $('.talks .talk').click(function(ev) {
        $(this).toggleClass('current');
    });
});
