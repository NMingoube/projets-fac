<?php

require_once "../autoload.php";
require_once "globalDAO.php";

if ( isset($_REQUEST['action']) && !empty($_REQUEST['action']))
{
    $action = $_REQUEST['action'];

    switch( $action )
    {
        case "getDVDFromData": { getDVDFromData(); break; }
        case "getMagazineFromData": { getMagazineFromData(); break; }
        case "getBookFromData": { getBookFromData(); break; }
        case "getWorkTypeList": { getWorkTypeList(); break; }
        case "getRightLevelList": { getRightLevelList(); break; }
        case "getFrequencyList": { getFrequencyList(); break; }
    }
}

/* ==============================
 *    Function called from JS
 * ==============================
 */

/**
 * Return a list of ID of every matching Books with given filters
 */
function getBookFromData()
{
    if(isset($_REQUEST))
        echo json_encode(g_getBookFromData($_REQUEST));
}

/**
 * Return a list of ID of every matching DVD with given filters
 */
function getDVDFromData()
{
    if(isset($_REQUEST))
        echo json_encode(g_getDVDFromData($_REQUEST));
}

/**
 * Return a list of ID of every matching magazine with given filters
 */
function getMagazineFromData()
{
    if(isset($_REQUEST))
        echo json_encode(g_getMagazineFromData($_REQUEST));
}

/**
 * Return a list of every type
 */
function getWorkTypeList()
{
    echo json_encode(g_getWorkTypeList());
}

/**
 * Return a list of every right levels
 */
function getRightLevelList()
{
    echo json_encode(g_getRightLevelList());
}

/**
 * Return a list of every frequency
 */
function getFrequencyList()
{
    echo json_encode(g_getFrequencyList());
}

?>