$(document).ready(function ()
{
    // Type
    $.post(
        '../DAO/userDAO.php',
        { action : "getWorkTypeList" },
        fillWorkTypeSelect,
        'json'
    );

    // Frequency
    $.post(
        '../DAO/userDAO.php',
        { action : "getFrequencyList" },
        fillFrequencySelect,
        'json'
    );

    // Right level
    $.post(
        '../DAO/userDAO.php',
        { action : "getRightLevelList" },
        fillRightLevelSelect,
        'json'
    );
    
    // State
    $.post(
        '../DAO/libriarianDAO.php',
        { action : "getStateList" },
        fillStateSelect,
        'json'
    );

    $('[type="date"][name!="end"]').prop('max', function() {
        return new Date().toJSON().split('T')[0];
    });

    $('#start, #end').prop('min', function() {
        return new Date().toJSON().split('T')[0];
    });
});

function fillWorkTypeSelect(workTypeList)
{
    $("select[name='type']").each((index, select) => {
        workTypeList.forEach(type => {
            $(select).append("<option value=\"" + type.id + "\">" + type.name + "</option>");
        });
    });
}

function fillFrequencySelect(workTypeList)
{
    $("select[name='frequency']").each((index, select) => {
        workTypeList.forEach(type => {
            $(select).append("<option value=\"" + type.id + "\">" + type.name + "</option>");
        });
    });
}

function fillRightLevelSelect(workTypeList)
{
    $("select[name='rightLevel']").each((index, select) => {
        workTypeList.forEach(type => {
            $(select).append("<option value=\"" + type.id + "\">" + type.name + "</option>");
        });
    });
}

function fillStateSelect(workTypeList)
{
    $("select[name='state']").each((index, select) => {
        workTypeList.forEach(type => {
            $(select).append("<option value=\"" + type.id + "\">" + type.name + "</option>");
        });
    });
}