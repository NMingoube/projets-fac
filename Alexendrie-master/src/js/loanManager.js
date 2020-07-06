window.onload = function() {
	$('#createLoan').submit( function( event ) {
		event.preventDefault();
		onSubmitCreateLoanHandler();
    });

    $('#searchLoan').submit( function( event ) {
		event.preventDefault();
		onSubmitSearchLoanHandler();
    });
};

// Add copy

function onSubmitCreateLoanHandler()
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action : "createLoan",
            subId  : $("#loanSubscriberId").val(),
            copyId : $("#loanCopyId").val(),
            start  : $("#start").val(),
            end    : $("#end").val()
        },
        loanCreated(),
        'json'
    );
}

function loanCreated(value)
{
    console.log(value);
}

function onSubmitSearchLoanHandler()
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action : "searchLoan",
            subId  : $("#searchLoanSubscriberId").val()
        },
        loanSearch,
        'json'
    );
}

function loanSearch(loanList)
{
    $('#loanList').html("");
    loanList.forEach(loan => {
        var table = $("<table>");
        for (var i in loan)
            if (loan.hasOwnProperty(i))
                table.append($('<tr><td class="label">' + i + '</td><td>' + loan[i] + '</td></tr>'));
                $('#loanList')
        var div = $('<div>');
        div.append(table);
        div.append($('<button onclick="endLoan(' + loan.id + ');">Return</button>'));
        $('#loanList').append(div);
    });
}

function endLoan(id)
{
    $.post(
        '../DAO/libriarianDAO.php',
        {
            action : "endLoan",
            id     : id
        },
        onEndLoan,
        'json'
    );
}

function onEndLoan(value)
{
    console.log(value);
}