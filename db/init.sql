USE medical;
CREATE TABLE insurance_company (
    insurance_company_id INT NOT NULL AUTO_INCREMENT,
    insurance_company_name VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address_street VARCHAR(255) NOT NULL,
    address_city VARCHAR(100) NOT NULL,
    address_state CHAR(2) NOT NULL,
    address_zip CHAR(10) NOT NULL,
    established_year YEAR NOT NULL,
    rating DECIMAL(3,2) DEFAULT NULL,
    specialization VARCHAR(255) DEFAULT NULL,
    is_active TINYINT(1) DEFAULT '1',
    PRIMARY KEY (insurance_company_id),
    UNIQUE KEY email (email),
    CONSTRAINT insurance_company_chk_1 CHECK ((rating >= 0 AND rating <= 5))
);
CREATE TABLE patients (
    patient_id INT NOT NULL AUTO_INCREMENT,
    patient_name VARCHAR(255) NOT NULL,
    patient_date_of_birth DATE NOT NULL,
    patient_ssn CHAR(11) NOT NULL,
    patient_address_street VARCHAR(255) NOT NULL,
    patient_address_city VARCHAR(100) NOT NULL,
    patient_address_state CHAR(2) NOT NULL,
    patient_address_zip CHAR(10) NOT NULL,
    insurance_company_id INT NOT NULL,
    PRIMARY KEY (patient_id),
    UNIQUE KEY patient_ssn (patient_ssn),
    FOREIGN KEY (insurance_company_id) REFERENCES insurance_company (insurance_company_id)
);

INSERT INTO insurance_company VALUES (1,'HealthFirst','123-456-7890','info@healthfirst.com','100 Main St','New York','NY','10001',1985,4.50,'Health Insurance',1),(2,'LifeCare','987-654-3210','support@lifecare.com','200 Oak St','Los Angeles','CA','90001',1990,4.70,'Life Insurance',1),(3,'AutoProtect','555-123-4567','contact@autoprotect.com','300 Elm St','Houston','TX','77001',1975,4.20,'Auto Insurance',1),(4,'SafeGuard','444-987-6543','hello@safeguard.com','400 Pine St','Chicago','IL','60601',1980,4.80,'Home Insurance',1),(5,'MediShield','222-333-4444','contact@medishield.com','500 Maple St','Phoenix','AZ','85001',1995,4.30,'Health Insurance',1),(6,'WellnessPlus','111-222-3333','info@wellnessplus.com','600 Cedar St','Philadelphia','PA','19101',2000,4.60,'Health Insurance',1),(7,'PrimeLife','999-888-7777','support@primelife.com','700 Birch St','San Antonio','TX','78201',1998,4.90,'Life Insurance',1),(8,'DriveSafe','888-999-6666','contact@drivesafe.com','800 Ash St','San Diego','CA','92101',1987,4.40,'Auto Insurance',1),(9,'HomeSecure','777-666-5555','info@homesecure.com','900 Walnut St','Dallas','TX','75201',1983,4.60,'Home Insurance',1),(10,'VitalCare','666-555-4444','support@vitalcare.com','1000 Cherry St','San Jose','CA','95101',1992,4.70,'Health Insurance',1),(11,'FamilyFirst','333-222-1111','hello@familyfirst.com','1100 Aspen St','Austin','TX','73301',2001,4.30,'Family Insurance',1),(12,'EcoLife','444-333-2222','contact@ecolife.com','1200 Spruce St','Jacksonville','FL','32201',1997,4.20,'Life Insurance',1),(13,'CareWell','555-444-3333','info@carewell.com','1300 Cypress St','Fort Worth','TX','76101',2005,4.40,'Health Insurance',1),(14,'ProtectMax','666-777-8888','support@protectmax.com','1400 Palm St','Charlotte','NC','28201',1993,4.60,'Home Insurance',1),(15,'LifeSecure','777-888-9999','info@lifesecure.com','1500 Oakwood St','Columbus','OH','43001',1989,4.50,'Life Insurance',1),(16,'SafeLife','888-999-1111','contact@safelife.com','1600 Redwood St','Indianapolis','IN','46201',2003,4.30,'Life Insurance',1),(17,'MediCarePlus','999-111-2222','support@medicareplus.com','1700 Beech St','San Francisco','CA','94101',1996,4.80,'Health Insurance',1),(18,'AutoSure','222-333-4444','hello@autosure.com','1800 Willow St','Seattle','WA','98101',1984,4.10,'Auto Insurance',1),(19,'HomeSure','111-444-5555','contact@homesure.com','1900 Sycamore St','Denver','CO','80201',1991,4.70,'Home Insurance',1),(20,'GuardianPlus','333-555-6666','info@guardianplus.com','2000 Magnolia St','Boston','MA','02101',1986,4.90,'Health Insurance',1);
INSERT INTO patients (
    patient_name,
    patient_date_of_birth,
    patient_ssn,
    patient_address_street,
    patient_address_city,
    patient_address_state,
    patient_address_zip,
    insurance_company_id
) VALUES
('John Doe', '1967-03-22', '123-45-6789', '123 Elm St', 'Springfield', 'IL', '62701', 1),
('Jane Smith', '1990-07-22', '987-65-4321', '456 Pine St', 'Chicago', 'IL', '60614', 2),
('Michael Brown', '1982-11-05', '555-66-7777', '789 Maple Ave', 'Houston', 'TX', '77001', 3),
('Emily Davis', '1995-01-10', '111-22-3333', '101 Oak Dr', 'Phoenix', 'AZ', '85001', 4),
('Robert Wilson', '1978-06-17', '444-33-2222', '202 Birch Ln', 'Los Angeles', 'CA', '90001', 5),
('Jessica Taylor', '1992-09-24', '333-22-4444', '303 Cedar Blvd', 'San Antonio', 'TX', '78201', 6),
('David Martinez', '1987-04-12', '222-11-5555', '404 Spruce St', 'Philadelphia', 'PA', '19101', 7),
('Sarah Lee', '1975-12-30', '666-77-8888', '505 Redwood Rd', 'Dallas', 'TX', '75201', 8),
('Laura Walker', '1980-02-20', '777-88-9999', '606 Beech Ct', 'San Diego', 'CA', '92101', 9),
('Paul White', '1983-08-08', '888-99-1111', '707 Palm Ave', 'San Jose', 'CA', '95101', 10),
('Karen Hall', '1989-05-05', '999-00-2222', '808 Willow Ln', 'Seattle', 'WA', '98101', 11),
('Chris Adams', '1973-03-15', '000-11-3333', '909 Cherry St', 'Denver', 'CO', '80201', 12),
('Lisa Young', '1997-07-27', '111-22-4444', '1000 Magnolia Blvd', 'Boston', 'MA', '02101', 13),
('Mark Harris', '1984-10-11', '222-33-5555', '1111 Aspen Ct', 'Austin', 'TX', '73301', 14),
('Susan Clark', '1993-12-05', '333-44-6666', '1212 Sycamore Rd', 'Jacksonville', 'FL', '32201', 15),
('Steven Wright', '1981-09-19', '444-55-7777', '1313 Walnut Blvd', 'Fort Worth', 'TX', '76101', 16),
('Anna King', '1976-06-14', '555-66-8888', '1414 Oakwood St', 'Charlotte', 'NC', '28201', 17),
('Ryan Evans', '1990-01-23', '666-77-9999', '1515 Beech Way', 'Columbus', 'OH', '43001', 18),
('Rachel Hernandez', '1988-04-02', '777-88-1111', '1616 Elm Ave', 'Indianapolis', 'IN', '46201', 19),
('Brian Thomas', '1996-11-17', '888-99-2222', '1717 Cedar Dr', 'San Francisco', 'CA', '94101', 20);
