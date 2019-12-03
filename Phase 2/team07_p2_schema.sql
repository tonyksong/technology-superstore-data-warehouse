-- CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
CREATE USER IF NOT EXISTS team07@localhost IDENTIFIED BY 'gatech';

DROP DATABASE IF EXISTS `cs6400_sp19_team07`; 
SET default_storage_engine=InnoDB;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS cs6400_sp19_team07 
    DEFAULT CHARACTER SET utf8mb4 
    DEFAULT COLLATE utf8mb4_unicode_ci;
USE cs6400_sp19_team07;

GRANT SELECT, INSERT, UPDATE, DELETE, FILE ON *.* TO 'team07'@'localhost';
GRANT ALL PRIVILEGES ON `team07`.* TO 'team07'@'localhost';
GRANT ALL PRIVILEGES ON `cs6400_sp19_team07`.* TO 'team07'@'localhost';
FLUSH PRIVILEGES;


-- Tables

CREATE TABLE CategorizedBy (
PID INT UNSIGNED NOT NULL,
categoryName VARCHAR (50) NOT NULL,
PRIMARY KEY (PID, categoryName));

CREATE TABLE Category (
categoryName VARCHAR (50) NOT NULL,
PRIMARY KEY(categoryName));

CREATE TABLE City (
cityName VARCHAR (50) NOT NULL,
state VARCHAR (50) NOT NULL,
population INT UNSIGNED NOT NULL,
PRIMARY KEY (cityName, state));

CREATE TABLE GoesOnSale (
PID INT UNSIGNED NOT NULL,
saleDate DATE NOT NULL,
salePrice DECIMAL (19, 2) NOT NULL,
PRIMARY KEY (saleDate, PID));

CREATE TABLE Holiday (
holidayDate DATE NOT NULL,
holidayName VARCHAR (50) NOT NULL,
PRIMARY KEY(holidayDate));

CREATE TABLE Manager (
emailAddress VARCHAR (50) NOT NULL,
managerName VARCHAR (50) NOT NULL,
PRIMARY KEY (emailAddress));

CREATE TABLE Manages (
emailAddress VARCHAR (50) NOT NULL,
storeNumber INT UNSIGNED NOT NULL,
PRIMARY KEY (emailAddress, storeNumber));

CREATE TABLE Manufacturer (
manufacturerName VARCHAR (50) NOT NULL,
maximumDiscount FLOAT NULL,
PRIMARY KEY (manufacturerName));

CREATE TABLE Product (
PID INT UNSIGNED NOT NULL,
productName VARCHAR (50) NOT NULL,
price DECIMAL(19, 2) NOT NULL,
manufacturerName VARCHAR (50) NOT NULL,
PRIMARY KEY (PID));

CREATE TABLE Store (
storeNumber INT UNSIGNED NOT NULL,
streetAddress VARCHAR (50) NOT NULL,
phoneNumber VARCHAR (50) NOT NULL,
cityName VARCHAR (50) NOT NULL,
state VARCHAR (50) NOT NULL,
PRIMARY KEY (storeNumber));

CREATE TABLE StoreSellsProduct (
PID INT UNSIGNED NOT NULL,
storeNumber INT UNSIGNED NOT NULL,
transactionDate DATE NOT NULL,
quantity INT UNSIGNED NOT NULL,
PRIMARY KEY (transactionDate, PID, storeNumber));


-- Constraints   Foreign Keys: fk_ChildTable_childColumn_ParentTable_parentColumn

ALTER TABLE CategorizedBy
ADD CONSTRAINT fk_CategorizedBy_PID_Product_PID FOREIGN KEY (PID) REFERENCES Product(PID),
ADD CONSTRAINT fk_CategorizedBy_categoryName_Category_categoryName FOREIGN KEY (categoryName) REFERENCES Category (categoryName);

ALTER TABLE GoesOnSale
ADD CONSTRAINT fk_GoesOnSale_PID_Product_PID FOREIGN KEY (PID) REFERENCES Product (PID);

ALTER TABLE Manages
ADD CONSTRAINT fk_Manages_emailAddress_Manager_emailAddress FOREIGN KEY (emailAddress) REFERENCES Manager (emailAddress),
ADD CONSTRAINT fk_Manages_storeNumber_Store_storeNumber FOREIGN KEY (storeNumber) REFERENCES Store (storeNumber);

ALTER TABLE Product
ADD CONSTRAINT fk_Product_manufacturerName_Manufacturer_manufacturerName FOREIGN KEY (manufacturerName) REFERENCES Manufacturer (manufacturerName);

ALTER TABLE Store
ADD CONSTRAINT fk_Store_cityName_state_City_cityName_state FOREIGN KEY (cityName, state) REFERENCES City (cityName, state);


ALTER TABLE StoreSellsProduct
ADD CONSTRAINT fk_StoreSellsProduct_PID_Product_PID FOREIGN KEY (PID) REFERENCES Product (PID),
ADD CONSTRAINT fk_StoreSellsProduct_storeNumber_Store_storeNumber FOREIGN KEY (storeNumber) REFERENCES Store (storeNumber);
