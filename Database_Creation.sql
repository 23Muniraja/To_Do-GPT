CREATE TABLE To_Do(
	Priority_Id Int NOT NULL,
    Task varchar(255) NOT NULL,
    Completed Int NOT NULL
);

Insert into To_Do (Priority_Id, Task, Completed) 
Values (0 , 'Checking_Database', 1);

SELECT * FROM To_Do;

ALTER TABLE To_Do
ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;