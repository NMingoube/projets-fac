<?php

require_once "../autoload.php";
require_once "globalDAO.php";

if ( isset($_REQUEST['action']) && !empty($_REQUEST['action']))
{
    $action = $_REQUEST['action'];

    switch( $action )
    {
        case "insertSubscriber": { insertSubscriber(); break; }
        case "getSubscriberFromData": { getSubscriberFromData(); break; }
        case "deleteSubscriber": { deleteSubscriber(); break; }
        case "insertBook": { insertBook(); break; }
        case "insertDVD": { insertDVD(); break; }
        case "insertMagazine": { insertMagazine(); break; }
        case "getDVDFromData": { getDVDFromData(); break; }
        case "getMagazineFromData": { getMagazineFromData(); break; }
        case "getBookFromData": { getBookFromData(); break; }
        case "deleteBook": { deleteBook(); break; }
        case "deleteDVD": { deleteDVD(); break; }
        case "deleteMagazine": { deleteMagazine(); break; }
        case "getStateList": { getStateList(); break; }
        case "insertCopy" : {insertCopy(); break; }
        case "getCopyFromData" : {getCopyFromData(); break; }
        case "deleteCopy" : {deleteCopy(); break; }
        case "createLoan" : {createLoan(); break; }
        case "searchLoan" : {searchLoan(); break; }
        case "endLoan" : {endLoan(); break; }
        
    }
}

/* ==============================
 *    Function called from JS
 * ==============================
 */

/**
 * Insert a new subscriber and return it's id if no error occurred in json object format
 */
function insertSubscriber()
{
    if(isset($_REQUEST))
        echo json_encode(g_insertSubscriber($_REQUEST["firstname"], $_REQUEST["lastname"], $_REQUEST["birthday"], $_REQUEST["email"], $_REQUEST["password"], $_REQUEST["street"], $_REQUEST["city"], intval($_REQUEST["postalCode"]), intval($_REQUEST["rightLevel"])));
}

/**
 * Return a list of every matching User with given filters
 */
function getSubscriberFromData()
{
    if(isset($_REQUEST))
        echo json_encode(g_getSubscriberFromData($_REQUEST));
}

function deleteSubscriber()
{
    if(isset($_REQUEST["id"]))
        echo json_encode(g_deleteSubscriber($_REQUEST["id"]));
}

/**
 * Insert a new book in database if every given data are valid
 */
function insertBook()
{
    if(isset($_REQUEST))
        echo json_encode(g_insertBook($_REQUEST["isbn"], $_REQUEST["title"], $_REQUEST["author"], $_REQUEST["editor"], $_REQUEST["type"], $_REQUEST["age"], $_REQUEST["publish"]));
}

/**
 * Return a list of every matching Books with given filters
 */
function getBookFromData()
{
    if(isset($_REQUEST))
        echo json_encode(g_getBookFromData($_REQUEST));
}

/**
 * Delete a Book from it's id
 */
function deleteBook()
{
    if(isset($_REQUEST["id"]))
        echo json_encode(g_deleteBook($_REQUEST["id"]));
}

/**
 * Insert a new DVD in database if every given data are valid
 */
function insertDVD()
{
    if(isset($_REQUEST))
        echo json_encode(g_insertDVD($_REQUEST["title"], $_REQUEST["director"], $_REQUEST["age"], $_REQUEST["type"], $_REQUEST["publish"]));
}

/**
 * Return a list of every matching DVD with given filters
 */
function getDVDFromData()
{
    if(isset($_REQUEST))
        echo json_encode(g_getDVDFromData($_REQUEST));
}

/**
 * Delete a DVD from it's id
 */
function deleteDVD()
{
    if(isset($_REQUEST["id"]))
        echo json_encode(g_deleteDVD($_REQUEST["id"]));
}

/**
 * Insert a new Magazine in database if every given data are valid
 */
function insertMagazine()
{
    if(isset($_REQUEST))
        echo json_encode(g_insertMagazine($_REQUEST["title"], $_REQUEST["number"], $_REQUEST["type"], $_REQUEST["age"], $_REQUEST["editor"], $_REQUEST["publish"], $_REQUEST["frequency"]));
}

/**
 * Return a list of every matching magazine with given filters
 */
function getMagazineFromData()
{
    if(isset($_REQUEST))
        echo json_encode(g_getMagazineFromData($_REQUEST));
}

/**
 * Delete a Magazine from it's id
 */
function deleteMagazine()
{
    if(isset($_REQUEST["id"]))
        echo json_encode(g_deleteMagazine($_REQUEST["id"]));
}

/**
 * Return a list of every state
 */
function getStateList()
{
    echo json_encode(g_getStateList());
}

function insertCopy()
{
    try {
        echo json_encode(g_insertCopy(intval($_REQUEST["copyType"]), intval($_REQUEST["id"]), intval($_REQUEST["state"])));
    }
    catch(Exception $e)
    {
        echo json_encode(false);
    }
}

/**
 * Return a list of every matching copy with given filters
 */
function getCopyFromData()
{
    if(isset($_REQUEST))
        echo json_encode(g_getCopyFromData(intval($_REQUEST["copyType"]), intval($_REQUEST["id"])));
}

/**
 * Delete a Magazine from it's id
 */
function deleteCopy()
{
    if(isset($_REQUEST["id"]))
        echo json_encode(g_deleteCopy($_REQUEST["id"]));
}

/**
 * Create a loan
 */
function createLoan()
{
    if(isset($_REQUEST))
    {
        if(strtotime($_REQUEST["start"]) < strtotime($_REQUEST["end"]))
            echo json_encode(g_createLoan(intval($_REQUEST["subId"]), intval($_REQUEST["copyId"]), $_REQUEST["start"], $_REQUEST["end"]));
        else
            echo json_encode("invalid date");
    }
}

/**
 * Return list of loan of a sub
 */
function searchLoan()
{
    if(isset($_REQUEST))
        echo json_encode(g_searchLoan(intval($_REQUEST["subId"])));
}

function endLoan()
{
    if(isset($_REQUEST))
        echo json_encode(g_endLoan(intval($_REQUEST["id"])));
}
?>