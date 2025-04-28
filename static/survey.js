let searchParams = new URLSearchParams(window.location.search)
let campaign     = searchParams.get('campaign')
let email        = searchParams.get('mail')
let guid         = searchParams.get('guid')

$("#btnSend").click(function () {
    var r1 = $('input[name="numero1"]:checked').val()
    var r2 = $('input[name="numero2"]:checked').val()
    var r3 = $('input[name="numero3"]:checked').val()
    var r4 = $('input[name="numero4"]:checked').val()
    var r5 = $('input[name="numero5"]:checked').val()

    var rating1 = typeof r1 !== 'undefined' ? r1 : null;
    var rating2 = typeof r2 !== 'undefined' ? r2 : null;
    var rating3 = typeof r3 !== 'undefined' ? r3 : null;
    var rating4 = typeof r4 !== 'undefined' ? r4 : null;
    var rating5 = typeof r5 !== 'undefined' ? r5 : null;

    if (!guid) {
        var message = 'Encuesta no valida.'
        alert(message)
    } else {
        if (rating1 != null) {
            $.ajax({
                url: "/webhookSurvey",
                type: "POST",
                contentType: "application/json",
                "data": JSON.stringify({
                    "rating": rating1,
                    "rating2": rating2,
                    "rating3": rating3,
                    "rating4": rating4,
                    "rating5": rating5,
                    "guid": guid
                }),
                success: function () {
                    // let message = 'Gracias por contestar la encuesta.'
                    // alert(message)
                    window.location.href = "/form"; // Corrected syntax
                },
            });
        } else {
            let message = 'Debe seleccionar una calificación';
            alert(message)
        }
    }
});


$(document).ready(function () {
	$(".loader-wrapper").fadeOut("slow");
})