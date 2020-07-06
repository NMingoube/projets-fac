window.onload = function () {
    $( "#searchSubscriber" ).submit(function( event ) {
        event.preventDefault();
        onSubmitSearchSubscriberHandler();
    });
}

function onSubmitSearchSubscriberHandler()
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action    : "getSubscriberFromData",
            firstname : $("input[id='firstname']").val(),
            lastname  : $("input[id='lastname']").val(),
            email     : $("input[id='email']").val()
        },
        displaySubscriber,
        'json'
    );
    
    function displaySubscriber(subList)
    {
        $('#subList').html("");
        subList.forEach(sub => {
            var table = $("<table>");
            for (var i in sub)
                if (sub.hasOwnProperty(i))
                    table.append($('<tr><td class="label">' + i + '</td><td>' + sub[i] + '</td></tr>'));
                    $('#subList')
            $('#subList').append(table);            
        });
    };
}