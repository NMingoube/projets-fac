window.onload = function() {
	$('#addBook').submit( function( event ) {
		event.preventDefault();
		onSubmitAddBookHandler();
    });
    
    $('#addDVD').submit( function( event ) {
		event.preventDefault();
		onSubmitAddDVDHandler();
    });
    
    $('#addMagazine').submit( function( event ) {
		event.preventDefault();
		onSubmitAddMagazineHandler();
    });
    
    $('#deleteBook').submit( function( event ) {
		event.preventDefault();
		onSubmitDeleteBookHandler();
    });

    $('#deleteDVD').submit( function( event ) {
		event.preventDefault();
		onSubmitDeleteDVDHandler();
    });

    $('#deleteMagazine').submit( function( event ) {
		event.preventDefault();
		onSubmitDeleteMagazineHandler();
    });
};

function onSubmitAddBookHandler()
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action  : "insertBook",
            isbn    : $("#bookIsbn").val(),
            title   : $("#bookTitle").val(),
            type    : $("#bookType").val(),
            age     : $("#bookAge").val(),
            author  : $("#bookAuthor").val(),
            editor  : $("#bookEditor").val(),
            publish : $("#bookPublish").val()
        },
        addWork,
        'json'
    );
}

function onSubmitAddDVDHandler()
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action   : "insertDVD",
            title    : $("#dvdTitle").val(),
            director : $("#dvdDirector").val(),
            type     : $("#dvdType").val(),
            age      : $("#dvdAge").val(),
            publish  : $("#dvdPublish").val()
        },
        addWork,
        'json'
    );
}

function onSubmitAddMagazineHandler()
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action    : "insertMagazine",
            title     : $("#magazineTitle").val(),
            number    : $("#magazineNumber").val(),
            type      : $("#magazineType").val(),
            age       : $("#magazineAge").val(),
            editor    : $("#magazineEditor").val(),
            publish   : $("#magazinePublish").val(),
            frequency : $("#magazineFrequency").val()
        },
        addWork,
        'json'
    );
}

function addWork(value)
{
    $('#result').html("");
    if(value != null)
        $('#result').html('L\'oeuvre a été correctement ajoutée et rattachée à l\'identifiant ' + value);
    else
        $('#result').html('L\'oeuvre n\'a pas été ajoutée. Peut-être existe-t-elle déjà.');
}

// ===========
// DELETE ZONE
// ===========

function onSubmitDeleteBookHandler()
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action : "deleteBook",
            id     : $('#bookId').val()
        },
        deleteWork,
        'json'
    );
}

function onSubmitDeleteDVDHandler()
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action : "deleteDVD",
            id     : $('#DVDId').val()
        },
        deleteWork,
        'json'
    );
}

function onSubmitDeleteMagazineHandler()
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action : "deleteMagazine",
            id     : $('#magazineId').val()
        },
        deleteWork,
        'json'
    );
}

function deleteWork(value)
{
    $('#result').html("");
        $('#result').html(value == true ? 'L\'oeuvre a été supprimée où n\'existe pas' : 'L\'oeuvre n\'a pas supprimée');
}