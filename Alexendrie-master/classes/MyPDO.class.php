<?php

/*
 * Class to use PDO.
 */

require_once "MyPDO.config.php";

final class myPDO
{
    /**
     * @var myPDO $_PDOInstance Unique instance.
     */
    private static $_PDOInstance   = null;
    /**
     * @var string $_DSN Data Source Name
     */
    private static $_DSN           = null;
    /**
     * @var string $_username Username for database connexion
     */
    private static $_username      = null;
    /**
     * @var string $_password Password for database connexion
     */
    private static $_password      = null;
    /**
     * @var array $_driverOptions Options
     */
    private static $_driverOptions = array (
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    );

    /**
     * Private constructor
     */
    private function __construct()
    {
    }

    /**
     * Get unique instance
     * @throws Exception In case of bad arguments
     * @return myPDO Unique instance
     */
    public static function getInstance()
    {
        if (is_null(self::$_PDOInstance))
        {
            if (self::hasConfiguration())
                self::$_PDOInstance = new PDO(self::$_DSN, self::$_username, self::$_password, self::$_driverOptions);
            else
                throw new Exception(__CLASS__ . ": Configuration not set");
        }
        return self::$_PDOInstance;
    }

    /**
     * Set connexion to database
     *
     * @param string $dsn Data Source Name
     * @param string $username Username for database connexion
     * @param string $password Password for database connexion
     * @param array $driver_options Options
     * @return void
     */
    public static function setConfiguration($dsn, $username='', $password='', array $driver_options=array())
    {
        self::$_DSN           = $dsn;
        self::$_username      = $username;
        self::$_password      = $password;
        self::$_driverOptions = $driver_options + self::$_driverOptions;
    }

    /**
     * Check if connexion is set
     * @return bool
     */
    private static function hasConfiguration()
    {
        return self::$_DSN !== null;
    }
}