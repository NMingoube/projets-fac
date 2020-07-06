// 0 : book --- 1 : dvd --- 2 : magazine
var lastInsertType = -1;
var funcNames = ['reserveBook', 'reserveDVD','reserveMagazine'];

window.onload = function () {
    $( "#searchDVD").submit(function( event ) {
        event.preventDefault();
        onSubmitSearchDVDHandler();
    });

    $( "#searchBook").submit(function( event ) {
        event.preventDefault();
        onSubmitSearchBookHandler();
    });

    $( "#searchMagazine").submit(function( event ) {
        event.preventDefault();
        onSubmitSearchMagazineHandler();
    });
}

function onSubmitSearchDVDHandler()
{
    lastInsertType = 0;
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action   : "getDVDFromData",
            title    : $("#dvdTitle").val(),
            director : $("#dvdDirector").val(),
            type     : $("#dvdType").val(),
            age      : $("#dvdAge").val(),
            publish  : $("#dvdPublish").val()
        },
        displayWork,
        'json'
    );
}

function onSubmitSearchBookHandler()
{
    lastInsertType = 1;
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action  : "getBookFromData",
            isbn    : $("#bookIsbn").val(),
            title   : $("#bookTitle").val(),
            type    : $("#bookType").val(),
            age     : $("#bookAge").val(),
            author  : $("#bookAuthor").val(),
            editor  : $("#bookEditor").val(),
            publish : $("#bookPublish").val()
        },
        displayWork,
        'json'
    );    
}

function onSubmitSearchMagazineHandler()
{
    lastInsertType = 2;
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action    : "getMagazineFromData",
            title     : $("#magazineTitle").val(),
            number    : $("#magazineNumber").val(),
            type      : $("#magazineType").val(),
            age       : $("#magazineAge").val(),
            editor    : $("#magazineEditor").val(),
            publish   : $("#magazinePublish").val(),
            frequency : $("#magazineFrequency").val()
        },
        displayWork,
        'json'
    );    
}

function displayWork(subList)
{
    $('#subList').html("");
    subList.forEach(sub => {
        var table = $("<table>");
        for (var i in sub)
            if (sub.hasOwnProperty(i))
                table.append($('<tr><td class="label">' + i + '</td><td>' + sub[i] + '</td></tr>'));
        var div = $('<div>');
        div.append(table);
        div.append($('<button onclick="' + funcNames[lastInsertType] + '(' + sub.id + ');">Réserver</button>'));
        $('#subList').append(div);        
    });
};