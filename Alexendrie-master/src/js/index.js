$(document).ready(function ()
{
    $.post(
        '../DAO/userDAO.php',
        { action : "getWorkTypeList" },
        fillWorkTypeSelect,
        'json'
    );
    
    function fillWorkTypeSelect(workTypeList)
    {
        $("select[name='type']").each((index, select) => {
            workTypeList.forEach(type => {
                $(select).append("<option value=\"" + type.id + "\">" + type.name + "</option>");
            });
        });
    }
});