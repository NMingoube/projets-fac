<?php

use function PHPSTORM_META\type;

require_once "../autoload.php";

/* ==============================
 *    User zone
 * ==============================
 */

 /**
 * Return every data from User, Address and Subscriber table of a subscriber from it's id
 * @param int $id User's id
 * @return array User's data OR false if id is not valid
 */
function g_getSubscriberFromId(int $id)
{
    $connexion = myPDO::getInstance();
    // Get information
    $request = $connexion->prepare(<<<SQL_g_getSubscriberFromId
    SELECT u.id,
           firstname,
           lastname,
           birthday,
           email,
           street,
           city,
           postalCode
      FROM User u, Address a, Subscriber s
     WHERE u.id   = :id
       AND a.id   = u.address
       AND s.user = :id
    ;  
SQL_g_getSubscriberFromId
    );
    $request->execute(array("id" => $id));
    // return
    return $request->fetchall();
}

 /**
 * Return every data of a Book from some of it's data
 * @param array $data This array should be $columnName => $value
 * @return array Book's data OR false if no match was founded
 */
function g_getSubscriberFromData(array $data)
{
    $connexion = myPDO::getInstance();
    // Dynamically build prepare request
    $builtRequest = NULL;
    $builtArray = array();
    foreach($data as $column => $value)
    {
        // Break if none value given
        if($value == NULL || $column == "action")
            continue;
        // Switch on column
        if($column == "firstname" || $column == "lastname" || $column == "email" || $column == "street" || $column == "city")
        {
            $builtRequest .= " AND UPPER($column) = UPPER(:$column)";
            $builtArray[$column] = $value;
        }
        else if($column == "rightLevel" || $column == "postalCode")
        {
            $builtRequest .= " AND $column = :$column";
            $builtArray[$column] = intval($value);
        }
        else if($column == "birthday")
        {
            $builtRequest .= " AND $column = STR_TO_DATE(:$column, '%Y-%m-%d');";
            $builtArray[$column] = $value;
        }
    }
    
    $request = $connexion->prepare("SELECT u.id, firstname, lastname, birthday, email, street, city, postalCode FROM User u, Address a, Subscriber s WHERE TRUE $builtRequest AND u.address = a.id AND s.user = u.id ");
    $request->execute($builtArray);
    return $request->fetchall();
}

/**
 * Insert a new Subscriber in the base from the data editor and return it's id
 * @param string $firstname
 * @param string $lastname
 * @param string $birthday string format : YYYY-MM-DD
 * @param string $email
 * @param string $street
 * @param string $city
 * @param int $postalCode
 * @param int $rightLevel id of corresponding right level in rightLevel table
 * @return int Return the new User's id OR false if an error occurred
 */
function g_insertSubscriber(string $firstname, string $lastname, string $birthday, string $email, string $password, string $street, string $city, int $postalCode, int $rightLevel)
{
    $connexion = myPDO::getInstance();
    // Check if user exists
    if(g_getSubscriberFromData(array("firstname" => $firstname, "lastname" => $lastname, "email" => $email)) != false)
        return null;
    // Check if address already exists
    $addressId = g_getAddressId($street, $city, $postalCode);
    // Create address instance if one does not already exists
    if($addressId == NULL)
    {
        $request = $connexion->prepare("INSERT INTO address (street, city, postalCode) VALUES (:street, :city, :postalCode);");
        $request->execute(array( 'street'     => $street,
                                 'city'       => $city,
                                 'postalCode' => $postalCode
        ));
        $addressId = $connexion->lastInsertId();
    }
    // Insert User
    $request = $connexion->prepare("INSERT INTO user (firstname, lastname, address, email, password, rightlevel) VALUES (:firstname, :lastname, :address, :email, :password, :rightlevel);");
    $request->execute(array( 'firstname'  => $firstname,
                             'lastname'   => $lastname,
                             'address'    => $addressId,
                             'email'      => $email,
                             'password'   => $password,
                             'rightlevel' => $rightLevel
    ));
    $userId = $connexion->lastInsertId();
    // Insert subscriber
    $request = $connexion->prepare("INSERT INTO subscriber (id, user, birthday) VALUES (:id, :user, STR_TO_DATE(:birthday, '%Y-%m-%d'));");
    $request->execute(array( 'id'       => $userId,
                             'user'     => $userId,
                             'birthday' => $birthday
    ));
    // Return subscriber's id
    return $connexion->lastInsertId();
}

/**
 * Function to delete a Subscriber from it's id
 */
function g_deleteSubscriber(int $id)
{
    $request = myPDO::getInstance()->prepare("DELETE FROM Subscriber WHERE user = :id");
    $res = $request->execute(array( 'id' => $id));
    $request = myPDO::getInstance()->prepare("DELETE FROM User WHERE id = :id");
    return $res && $request->execute(array( 'id' => $id));
}

/** Search an address in database and return its id if exists
      * @param string $street
      * @param string $city
      * @param string $postalCode
      * @return int address' id if exists
      */
function g_getAddressId(string $street, string $city, int $postalCode)
{
    // Prepare query
    $request = myPDO::getInstance()->prepare(<<<SQL_g_getAddressId
        SELECT id
          FROM address a
         WHERE a.street     = :street 
           AND a.city       = :city
           AND a.postalCode = :postalCode
        ;
SQL_g_getAddressId
    );
    // Execute query
    $request->execute(array (
        'street'     => $street,
        'city'       => $city,
        'postalCode' => $postalCode
    ));
    // Return
    $array = $request->fetch();
    return isset($array['id']) ? $array['id'] : NULL;
}

/* ==============================
 *    Book zone
 * ==============================
 */

 /**
 * Return every data of a Book from some of it's data
 * @param array $data This array should be $columnName => $value
 * @return array Book's data OR false if no match was founded
 */
function g_getBookFromData(array $data)
{    
    $connexion = myPDO::getInstance();
    // Dynamically build prepared request
    $builtRequest = NULL;
    $builtArray = array();
    foreach($data as $column => $value)
    {
        // Break if none value given
        if($value == NULL || $column == "action")
            continue;
        // Switch on column
        if($column == "title" || $column == "editor" || $column == "author" || $column == "isbn")
        {
            $builtRequest .= " AND UPPER($column) = UPPER(:$column)";
            $builtArray[$column] = $value;
        }
        else if($column == "id" || $column == "type")
        {
            $builtRequest .= " AND $column = :$column";
            $builtArray[$column] = intval($value);
        }
        else if($column == "age")
        {
            $builtRequest .= " AND $column <= :$column";
            $builtArray[$column] = intval($value);
        }
        else if($column == "publish")
        {
            $builtRequest .= " AND $column = STR_TO_DATE(:$column, '%Y-%m-%d');";
            $builtArray[$column] = $value;
        }
    }

    $request = $connexion->prepare("SELECT b.id, isbn, title, name, age, author, editor, publish FROM book b, type t WHERE b.type = t.id $builtRequest");
    $request->execute($builtArray);
    return $request->fetchall();
}

 /**
 * Insert a new Book in the base from the data editor and return it's id
 * @param string $isbn
 * @param string $title
 * @param string $author
 * @param string $editor
 * @param int $type id of corresponding type in Type table
 * @param int $age
 * @param string $publish string format : YYYY-MM-DD
 * @return int Return the new Book's id OR false if an error occurred
 */
function g_insertBook(string $isbn, string $title, string $author, string $editor, int $type, int $age, string $publish)
{
    $connexion = myPDO::getInstance();
    // Check if book does not exists
    if(g_getBookFromData(array("title" => $title, "author" => $author, "editor" => $editor)) != false)
        return null;
    // Insert Book
    $request = $connexion->prepare("INSERT INTO Book (isbn, title, type, age, author, editor, publish) VALUES (:isbn, :title, :type, :age, :author, :editor, STR_TO_DATE(:publish, '%Y-%m-%d'));");
    $request->execute(array( 'isbn'    => $isbn,
                             'title'   => $title,
                             'type'    => $type,
                             'age'     => $age,
                             'author'  => $author,
                             'editor'  => $editor,
                             'publish' => $publish
    ));
    // Return book's id
    return $connexion->lastInsertId();
}

/**
 * Function to delete a Book from it's id
 */
function g_deleteBook(int $id)
{
    $request = myPDO::getInstance()->prepare("DELETE FROM Book WHERE id = :id");
    return $request->execute(array( 'id' => $id));
}

/* ==============================
 *    DVD zone
 * ==============================
 */

 /**
 * Return every data of a DVD from some of it's data
 * @param array $data This array should be $columnName => $value
 * @return array DVD's data OR false if no match was founded
 */
function g_getDVDFromData(array $data)
{
    $connexion = myPDO::getInstance();
    // Dynamically build prepare request
    $builtRequest = NULL;
    $builtArray = array();
    foreach($data as $column => $value)
    {
        // Break if none value given
        if($value == NULL || $column == "action")
            continue;
        // Switch on column
        if($column == "title" || $column == "director")
        {
            $builtRequest .= " AND UPPER($column) = UPPER(:$column)";
            $builtArray[$column] = $value;
        }
        else if($column == "id" || $column == "type")
        {
            $builtRequest .= " AND $column = :$column";
            $builtArray[$column] = intval($value);
        }
        else if($column == "age")
        {
            $builtRequest .= " AND $column <= :$column";
            $builtArray[$column] = intval($value);
        }
        else if($column == "publish")
        {
            $builtRequest .= " AND $column = STR_TO_DATE(:$column, '%Y-%m-%d');";
            $builtArray[$column] = $value;
        }
    }
    
    $request = $connexion->prepare("SELECT d.id, title, director, name, age, publish FROM DVD d, type t WHERE d.type = t.id $builtRequest");
    $request->execute($builtArray);
    return $request->fetchall();
}

 /**
 * Insert a new DVD in the base from the data editor and return it's id
 * @param string $title
 * @param string $director
 * @param int $age
 * @param int $type id of corresponding type in Type table
 * @param string $publish string format : YYYY-MM-DD
 * @return int Return the new DVD's id OR false if an error occurred
 */
function g_insertDVD(string $title, string $director, int $age, int $type, string $publish)
{
    $connexion = myPDO::getInstance();
    // Check if book does not exists
    if(g_getDVDFromData(array("title" => $title, "director" => $director, "age" => $age, "type" => $type, "publish" => $publish)) != false)
        return null;
    // Insert Book
    $request = $connexion->prepare("INSERT INTO DVD (title, director, age, type, publish) VALUES (:title, :director, :age, :type, STR_TO_DATE(:publish, '%Y-%m-%d'));");
    $request->execute(array( 'title'    => $title,
                             'director' => $director,
                             'age'      => $age,
                             'type'     => $type,
                             'publish'  => $publish
    ));
    // Return book's id
    return $connexion->lastInsertId();
}

/**
 * Function to delete a DVD from it's id
 */
function g_deleteDVD(int $id)
{
    $request = myPDO::getInstance()->prepare("DELETE FROM DVD WHERE id = :id");
    return $request->execute(array( 'id' => $id));
}

/* ==============================
 *    Magazine zone
 * ==============================
 */

 /**
 * Return every data of a Magazine from some of it's data
 * @param array $data This array should be $columnName => $value
 * @return array Magazine's data OR false if no match was founded
 */
function g_getMagazineFromData(array $data)
{
    $connexion = myPDO::getInstance();
    // Dynamically build prepare request
    $builtRequest = NULL;
    $builtArray = array();
    foreach($data as $column => $value)
    {
        // Break if none value given
        if($value == NULL || $column == "action")
            continue;
        // Switch on column
        if($column == "title" || $column == "editor")
        {
            $builtRequest .= " AND UPPER($column) = UPPER(:$column)";
            $builtArray[$column] = $value;
        }
        else if($column == "id" || $column == "frequency" || $column == "number" || $column == "type")
        {
            $builtRequest .= " AND $column = :$column";
            $builtArray[$column] = intval($value);
        }
        else if($column == "age")
        {
            $builtRequest .= " AND $column <= :$column";
            $builtArray[$column] = intval($value);
        }
        else if($column == "publish")
        {
            $builtRequest .= " AND $column = STR_TO_DATE(:$column, '%Y-%m-%d');";
            $builtArray[$column] = $value;
        }
    }

    $request = $connexion->prepare("SELECT m.id, title, number, t.name, age, editor, publish, f.name FROM magazine m, type t, frequency f WHERE m.type = t.id AND m.frequency = f.id $builtRequest");
    $request->execute($builtArray);
    return $request->fetchall();
}

 /**
 * Insert a new Magazine in the base from the data editor and return it's id
 * @param string $title
 * @param int $number
 * @param int $type id of corresponding type in Type table
 * @param int $age
 * @param string $editor
 * @param string $publish string format : YYYY-MM-DD
 * @param int $frequency id of corresponding frequency in Frequency table
 * @return int Return the new DVD's id OR false if an error occurred
 */
function g_insertMagazine(string $title, int $number, int $type, string $age, string $editor, string $publish, int $frequency)
{
    $connexion = myPDO::getInstance();
    // Check if magazine does not exists
    if(g_getMagazineFromData(array("title" => $title, "number" => $number)) != false)
        return null;
    // Insert Book
    $request = $connexion->prepare("INSERT INTO Magazine (title, number, type, age, editor, publish, frequency) VALUES (:title, :number, :type, :age, :editor, STR_TO_DATE(:publish, '%Y-%m-%d'), :frequency);");
    $request->execute(array( 'title'     => $title,
                             'number'    => $number,
                             'type'      => $type,
                             'age'       => $age,
                             'editor'    => $editor,
                             'publish'   => $publish,
                             'frequency' => $frequency
    ));
    // Return magazine's id
    return $connexion->lastInsertId();
}

/**
 * Function to delete a Magazine from it's id
 */
function g_deleteMagazine(int $id)
{
    $request = myPDO::getInstance()->prepare("DELETE FROM Magazine WHERE id = :id");
    return $request->execute(array( 'id' => $id));
}

/* ==============================
 *    enum zone
 * ==============================
 */

 /**
 * Function to return content of table type
 * @return array an array of every type OR false if an error occured
 */
function g_getWorkTypeList()
{
    $request = myPDO::getInstance()->prepare("SELECT id, name FROM type");
    $request->execute();
    return $request->fetchall();
}

 /**
 * Function to return content of table rightLevel
 * @return array an array of every rightLevel OR false if an error occured
 */
function g_getRightLevelList()
{
    $request = myPDO::getInstance()->prepare("SELECT id, label FROM rightLevel");
    $request->execute();
    return $request->fetchall();
}

 /**
 * Function to return content of table frequency
 * @return array an array of every frequency OR false if an error occured
 */
function g_getFrequencyList()
{
    $request = myPDO::getInstance()->prepare("SELECT id, name FROM frequency");
    $request->execute();
    return $request->fetchall();
}

/* ==============================
 *    copy zone
 * ==============================
 */

 /**
 * Function to return content of table frequency
 * @return array an array of every frequency OR false if an error occured
 */
function g_getStateList()
{
    $request = myPDO::getInstance()->prepare("SELECT id, name FROM state");
    $request->execute();
    return $request->fetchall();
}

 /**
 * Insert a new Magazine in the base from the data editor and return it's id
 * @param int $type (0, 1 or 2)
 * @param int $id id of targeted work
 * @param int $state id of corresponding state in State table
 * @return int Return the new copy's id OR false if an error occurred
 */
function g_insertCopy(int $type, int $id, int $state)
{    
    $copyTypeList = array(0 => "book", 1 => "dvd", 2 => "magazine");
    $copyType = $copyTypeList[$type];
    $connexion = myPDO::getInstance();
    $request = $connexion->prepare("INSERT INTO Copy ($copyType, state) VALUES (:copyType, :state);");
    $request->execute(array( 'copyType'  => $id,
                             'state'     => $state
    ));
    // Return magazine's id
    return $connexion->lastInsertId();
}

/**
 * Insert a new Magazine in the base from the data editor and return it's id
 * @param int $type (0, 1 or 2)
 * @param int $id id of targeted work
 * @return array an array of every matching copy OR false if an error occured
 */
function g_getCopyFromData(int $type, int $id)
{
    $connexion = myPDO::getInstance();
    if($type == 0)
    {
        $request = $connexion->prepare("SELECT c.id, title, name FROM copy c, state s, book b WHERE c.book = :id AND c.state = s.id AND c.book = b.id");
        $request->execute(array('id' => $id));
        return $request->fetchall();
    }
    if($type == 1)
    {
        $request = $connexion->prepare("SELECT c.id, title, name FROM copy c, state s, dvd d WHERE c.dvd = :id AND c.state = s.id AND d.id = :id");
        $request->execute(array('id' => $id));
        return $request->fetchall();
    }
    if($type == 2)
    {
        $request = $connexion->prepare("SELECT c.id, title, name FROM copy c, state s, magazine m WHERE c.magazine = :id AND c.state = s.id AND c.magazine = m.id");
        $request->execute(array('id' => $id));
        return $request->fetchall();
    }
}

/**
 * Delete a copy from it's id
 * @param int $type (0, 1 or 2)
 * @param int $id id of targeted work
 * @return array an array of every matching copy OR false if an error occured
 */
function g_deleteCopy(int $id)
{
    $request = myPDO::getInstance()->prepare("DELETE FROM Copy WHERE id = :id");
    return $request->execute(array( 'id' => $id)) == false ? false : $id;
}

/* ==============================
 *    loan zone
 * ==============================
 */

 /**
 * Insert a new Magazine in the base from the data editor and return it's id
 * @param int $subscriber
 * @param int $copy
 * @param string $start
 * @param string $end
 * @return array Return the new loan's id OR false if an error occurred
 */
function g_createLoan(int $subscriber, int $copy, string $start, string $end)
{
    $connexion = myPDO::getInstance();
    // Check number of book / magazine loan
    $request = $connexion->prepare("SELECT COUNT(l.id) FROM Loan l, Copy c WHERE subscriber = :subscriber AND l.copy = c.id AND (c.book IS NOT NULL OR c.magazine IS NOT NULL) AND end >= STR_TO_DATE(:start, '%Y-%m-%d') GROUP BY l.id");
    $request->execute(Array('subscriber' => $subscriber, 'start' => $start));
    $res = $request->fetchall();
    if($res != false)
        if($res[0]["COUNT(l.id)"] >= 4)
            return false;
    // Check number of dvd
    $request = $connexion->prepare("SELECT COUNT(l.id) FROM Loan l, Copy c WHERE subscriber = :subscriber AND l.copy = c.id AND c.dvd IS NOT NULL AND end >= STR_TO_DATE(:start, '%Y-%m-%d')");
    $request->execute(Array('subscriber' => $subscriber, 'start' => $start));
    $res = $request->fetchall();
    if($res != false)
        if($res[0]["COUNT(l.id)"] >= 2)
            return false;
    // Check copy is available
    $request = $connexion->prepare("SELECT id FROM Loan WHERE copy = :copy AND end > STR_TO_DATE(:start, '%Y-%m-%d')");
    $request->execute(Array('copy' => $copy, 'start' => $start));
    if($request->fetchall() != false)
        return false;
    // Then
    $request = $connexion->prepare("INSERT INTO Loan (subscriber, copy, start, end) VALUES (:subscriber, :copy, STR_TO_DATE(:start, '%Y-%m-%d'), STR_TO_DATE(:end, '%Y-%m-%d'))");
    $request->execute(array( 'subscriber' => $subscriber,
                             'copy'       => $copy,
                             'start'      => $start,
                             'end'        => $end
    ));
    // Return magazine's id
    return $connexion->lastInsertId();
}

function g_searchLoan(int $id)
{
    $request =  myPDO::getInstance()->prepare("SELECT * FROM Loan WHERE subscriber = :subscriber");
    $request->execute(array('subscriber' => $id));
    return $request->fetchall();
}

function g_endLoan(int $id)
{
    $request =  myPDO::getInstance()->prepare("UPDATE Loan SET end = SYSDATE() WHERE id = :id");
    return $request->execute(array('id' => $id));
}

?>