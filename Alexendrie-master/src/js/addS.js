window.onload = function() {
	$('#addSubscriber').submit( function( event ) {
		event.preventDefault();
		onSubmitAddSubscriberHandler();
    });
    
    $('#deleteSubscriber').submit( function( event ) {
		event.preventDefault();
		onSubmitDeleteSubscriberHandler();
    });
};

function onSubmitAddSubscriberHandler()
{	
	var hash = sha256.create();
    hash.update($("#password").val());
    console.log(hash.hex());
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action     : "insertSubscriber",
            firstname  : $("#firstname").val(),
            lastname   : $("#lastname").val(),			
			birthday   : $("#birthday").val(),
            email      : $("#email").val(),			
			street     : $("#street").val(),			
			city       : $("#city").val(),			
			postalCode : $("#postalCode").val(),			
			rightLevel : $("#rightLevel").val(),			
			password   : hash.hex()
        },
        displaySubscriber,
        'json'
    );

    function displaySubscriber(subList)
    {
        console.log(subList);
    }
}

function onSubmitDeleteSubscriberHandler()
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action : "deleteSubscriber",
            id     : $('#subscriberId').val()
        },
        deleteSubscriber,
        'json'
    );
}

function deleteSubscriber(value)
{
    $('#result').html("");
        $('#result').html(value == true ? 'L\'abonné a été supprimé où n\'existe pas' : 'L\'abonné n\'a pas supprimé');
}