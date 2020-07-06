window.onload = function() {
	$('#addCopy').submit( function( event ) {
		event.preventDefault();
		onSubmitAddCopyHandler();
    });
    
    $('#searchCopy').submit( function( event ) {
		event.preventDefault();
		onSubmitSearchCopyHandler();
    });
};

// Add copy

function onSubmitAddCopyHandler()
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action   : "insertCopy",
            copyType : $("#addCopyType").val(),
            id       : $("#addCopyId").val(),			
			state    : $("#state").val()
        },
        copyAdded,
        'json'
    );
}

function copyAdded(value)
{
    console.log(value);
    $('#copyList').html("");
        $('#copyList').html(value == false ? 'La copie n\'a pas été ajoutée' : 'La copie été ajoutée');
}

// Search copy


function onSubmitSearchCopyHandler()
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action   : "getCopyFromData",
            copyType : $("#searchCopyType").val(),
            id       : $("#searchCopyId").val(),
        },
        searchCopy,
        'json'
    );
}

function searchCopy(copyList)
{
    $('#copyList').html("");
    copyList.forEach(copy => {
        var table = $("<table>");
        for (var i in copy)
            if (copy.hasOwnProperty(i))
                table.append($('<tr><td class="label">' + i + '</td><td>' + copy[i] + '</td></tr>'));
        var div = $('<div>');
        div.append(table);
        div.append($('<button onclick="deleteCopy(' + copy.id + ');">Supprimer</button>'));
        $('#copyList').append(div);        
    });
}

function deleteCopy(value)
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action : "deleteCopy",
            id     : value
        },
        onDeleteCopy,
        'json'
    );
}

function onDeleteCopy(value)
{
    $('#copyList').html("");
    $('#copyList').html(value == false ? 'La copie n\'a pas été suprimée' : 'La copie été supprimée');
}