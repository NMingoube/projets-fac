DROP TABLE IF EXISTS Reservation;
DROP TABLE IF EXISTS Loan;
DROP TABLE IF EXISTS Librarian;
DROP TABLE IF EXISTS Subscriber;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS RightLevel;
DROP TABLE IF EXISTS Address;
DROP TABLE IF EXISTS Copy;
DROP TABLE IF EXISTS DVD;
DROP TABLE IF EXISTS Magazine;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS Frequency;
DROP TABLE IF EXISTS Type;
DROP TABLE IF EXISTS State;

CREATE TABLE State
(
    id   INTEGER     NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    CONSTRAINT pk_state PRIMARY KEY (id)
);

CREATE TABLE Type
(
    id   INTEGER     NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    CONSTRAINT pk_type PRIMARY KEY (id)
);

CREATE TABLE Frequency
(
    id   INTEGER     NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    CONSTRAINT pk_frequency PRIMARY KEY (id)
);

CREATE TABLE Book
(
    id      INTEGER     NOT NULL AUTO_INCREMENT,
    isbn    VARCHAR(13) NOT NULL,
    title   VARCHAR(50) NOT NULL,
    type    INTEGER     NOT NULL,
    age     INTEGER     NOT NULL,
    author  VARCHAR(50) NOT NULL,
    editor  VARCHAR(50) NOT NULL,
    publish DATE        NOT NULL,
    CONSTRAINT pk_book      PRIMARY KEY (id),
    CONSTRAINT fk_book_type FOREIGN KEY (type) REFERENCES Type(id)
);

CREATE TABLE Magazine
(
    id        INTEGER     NOT NULL AUTO_INCREMENT,
    title     VARCHAR(50) NOT NULL,
    number    INTEGER     NOT NULL,
    type      INTEGER     NOT NULL,
    age       INTEGER     NOT NULL,
    Editor    VARCHAR(50) NOT NULL,
    publish   DATE        NOT NULL,
    frequency INTEGER     NOT NULL,
    CONSTRAINT pk_magazine           PRIMARY KEY (id),
    CONSTRAINT fk_magazine_type      FOREIGN KEY (type)      REFERENCES Type(id),
    CONSTRAINT fk_magazine_frequency FOREIGN KEY (frequency) REFERENCES Frequency(id)
);

CREATE TABLE DVD
(
    id       INTEGER     NOT NULL AUTO_INCREMENT,
    title    VARCHAR(50) NOT NULL,
    director VARCHAR(30) NOT NULL,
    type     INTEGER     NOT NULL,
    age      INTEGER     NOT NULL,
    publish  DATE        NOT NULL,
    CONSTRAINT pk_dvd      PRIMARY KEY (id),
    CONSTRAINT fk_dvd_type FOREIGN KEY (type) REFERENCES Type(id)
);

CREATE TABLE Copy
(
    id       INTEGER NOT NULL AUTO_INCREMENT,
    book     INTEGER NULL,
    magazine INTEGER NULL,
    dvd      INTEGER NULL,
    state    INTEGER NOT NULL,
    CONSTRAINT pk_dvd        PRIMARY KEY (id),
    CONSTRAINT fk_copy_state    FOREIGN KEY (state)    REFERENCES State(id),
    CONSTRAINT fk_copy_book     FOREIGN KEY (book)     REFERENCES Book(id),
    CONSTRAINT fk_copy_magazine FOREIGN KEY (magazine) REFERENCES Magazine(id),
    CONSTRAINT fk_copy_dvd      FOREIGN KEY (dvd)      REFERENCES DVD(id)
);

CREATE TABLE Address
(
    id         INTEGER     NOT NULL AUTO_INCREMENT,
    street     VARCHAR(50) NOT NULL,
    city       VARCHAR(50) NOT NULL,
    postalCode CHAR(5)     NOT NULL,
    CONSTRAINT pk_address PRIMARY KEY (id)
);

CREATE TABLE RightLevel
(
    id    INTEGER     NOT NULL AUTO_INCREMENT,
    label VARCHAR(30) NOT NULL,
    CONSTRAINT pk_rightLevel PRIMARY KEY (id)
);

CREATE TABLE User
(
    id         INTEGER      NOT NULL AUTO_INCREMENT,
    firstname  VARCHAR(30)  NOT NULL,
    lastname   VARCHAR(30)  NOT NULL,
    address    INTEGER      NOT NULL,
    email      VARCHAR(100) NOT NULL,
    password   VARCHAR(512) NOT NULL,
    rightLevel INTEGER      NOT NULL,
    CONSTRAINT pk_user            PRIMARY KEY (id),
    CONSTRAINT fk_user_rightLevel FOREIGN KEY (rightLevel) REFERENCES RightLevel(id),
    CONSTRAINT fk_user_address    FOREIGN KEY (address)    REFERENCES Address(id)
);

CREATE TABLE Subscriber
( 
    id         INTEGER NOT NULL AUTO_INCREMENT,
    user       INTEGER NOT NULL,
    birthday   DATE    NOT NULL,
    CONSTRAINT pk_subscriber      PRIMARY KEY (id),
    CONSTRAINT fk_subscriber_user FOREIGN KEY (user) REFERENCES User(id)
);

CREATE TABLE Librarian
( 
    id   INTEGER NOT NULL AUTO_INCREMENT,
    user INTEGER NOT NULL,
    CONSTRAINT pk_librarian      PRIMARY KEY (id),
    CONSTRAINT fk_librarian_user FOREIGN KEY (user) REFERENCES User(id)
);

CREATE TABLE Loan
( 
    id         INTEGER NOT NULL AUTO_INCREMENT,
    start      DATE    NOT NULL,
    end        DATE    NOT NULL,
    copy       INTEGER NOT NULL,
    subscriber INTEGER NOT NULL,
    CONSTRAINT pk_loan            PRIMARY KEY (id),
    CONSTRAINT fk_loan_copy       FOREIGN KEY (copy)       REFERENCES Copy(id),
    CONSTRAINT fk_loan_subscriber FOREIGN KEY (subscriber) REFERENCES Subscriber(id)
);

CREATE TABLE Reservation
( 
    id         INTEGER NOT NULL AUTO_INCREMENT,
    orderDate  DATE    NOT NULL,
    pickupDate DATE    NOT NULL,
    copy       INTEGER NOT NULL,
    subscriber INTEGER NOT NULL,
    CONSTRAINT pk_reservation            PRIMARY KEY (id),
    CONSTRAINT fk_reservation_copy       FOREIGN KEY (copy)       REFERENCES Copy(id),
    CONSTRAINT fk_reservation_subscriber FOREIGN KEY (subscriber) REFERENCES Subscriber(id)
);

/* Some defalut pieces of data */
INSERT INTO Type(name) VALUES ("Horror");
INSERT INTO Type(name) VALUES ("Sc-Fi");
INSERT INTO Type(name) VALUES ("Comedy");

INSERT INTO State(name) VALUES ("New");
INSERT INTO State(name) VALUES ("Good");
INSERT INTO State(name) VALUES ("Correct");
INSERT INTO State(name) VALUES ("Used");
INSERT INTO State(name) VALUES ("Bad");

INSERT INTO RightLevel(label) VALUES ("Suscriber lv1");
INSERT INTO RightLevel(label) VALUES ("Suscriber lv2");
INSERT INTO RightLevel(label) VALUES ("Suscriber lv3");

INSERT INTO Frequency(name) VALUES ("Daily");
INSERT INTO Frequency(name) VALUES ("Weekly");
INSERT INTO Frequency(name) VALUES ("Monthly");

INSERT INTO DVD(title, director, type, age, publish) VALUES ("Film1", "dir1", 1, 18, STR_TO_DATE("01-01-2000", "%d-%m-%Y"));
INSERT INTO DVD(title, director, type, age, publish) VALUES ("Film2", "dir1", 1, 20, STR_TO_DATE("01-01-2001", "%d-%m-%Y"));
INSERT INTO DVD(title, director, type, age, publish) VALUES ("Film3", "dir2", 1, 20, STR_TO_DATE("01-01-2001", "%d-%m-%Y"));
INSERT INTO DVD(title, director, type, age, publish) VALUES ("Film4", "dir2", 2, 20, STR_TO_DATE("01-01-2010", "%d-%m-%Y"));
INSERT INTO DVD(title, director, type, age, publish) VALUES ("Film5", "dir3", 2, 20, STR_TO_DATE("01-01-2010", "%d-%m-%Y"));
INSERT INTO DVD(title, director, type, age, publish) VALUES ("Film6", "dir3", 2, 30, STR_TO_DATE("01-01-2015", "%d-%m-%Y"));

INSERT INTO Magazine(title, number, type, age, editor, publish, frequency) VALUES ("Mag1", 100, 1, 10, "editor1", STR_TO_DATE("01-01-2000", "%d-%m-%Y"), 1);
INSERT INTO Magazine(title, number, type, age, editor, publish, frequency) VALUES ("Mag2", 101, 1, 10, "editor1", STR_TO_DATE("01-01-2001", "%d-%m-%Y"), 1);
INSERT INTO Magazine(title, number, type, age, editor, publish, frequency) VALUES ("Mag3", 102, 1, 12, "editor1", STR_TO_DATE("01-01-2002", "%d-%m-%Y"), 1);
INSERT INTO Magazine(title, number, type, age, editor, publish, frequency) VALUES ("Mag4", 100, 1, 12, "editor2", STR_TO_DATE("01-01-2000", "%d-%m-%Y"), 3);
INSERT INTO Magazine(title, number, type, age, editor, publish, frequency) VALUES ("Mag5", 101, 2, 12, "editor2", STR_TO_DATE("01-01-2001", "%d-%m-%Y"), 3);
INSERT INTO Magazine(title, number, type, age, editor, publish, frequency) VALUES ("Mag6", 102, 3, 16, "editor2", STR_TO_DATE("01-01-2002", "%d-%m-%Y"), 3);

INSERT INTO Book(isbn, title, type, age, author, editor, publish) VALUES ("isbn1", "book1", 1, 10, "auth1", "editor1", STR_TO_DATE("01-01-2002", "%d-%m-%Y"));
INSERT INTO Book(isbn, title, type, age, author, editor, publish) VALUES ("isbn2", "book1", 1, 10, "auth1", "editor2", STR_TO_DATE("01-01-2003", "%d-%m-%Y"));
INSERT INTO Book(isbn, title, type, age, author, editor, publish) VALUES ("isbn3", "book2", 2, 12, "auth2", "editor1", STR_TO_DATE("01-01-2005", "%d-%m-%Y"));
INSERT INTO Book(isbn, title, type, age, author, editor, publish) VALUES ("isbn4", "book3", 3, 16, "auth3", "editor1", STR_TO_DATE("01-01-2002", "%d-%m-%Y"));
INSERT INTO Book(isbn, title, type, age, author, editor, publish) VALUES ("isbn5", "book3", 3, 16, "auth3", "editor2", STR_TO_DATE("01-01-2004", "%d-%m-%Y"));
INSERT INTO Book(isbn, title, type, age, author, editor, publish) VALUES ("isbn6", "book3", 3, 16, "auth3", "editor3", STR_TO_DATE("01-01-2006", "%d-%m-%Y"));