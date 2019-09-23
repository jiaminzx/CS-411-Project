Hello!

This is a project for cs 411 Database Structures: we attempted to make a backend that helps use past kaggle speed dating data to predict the likelihood of a match being made on a hypothetical match website based on the factors listed in our SQL databse

* we made a key constaint on userID in the database: below is the command to create the users table we populated in cpanel:create table users(userID INT(11) NOT NULL AUTO_INCREMENT, age INT(11),body_type VARCHAR(40), diet VARCHAR(40), drinks VARCHAR(40), education VARCHAR(40) NOT NULL, ethnicity VARCHAR(40) NOT NULL, height INT(11) NOT NULL, income INT(11), job VARCHAR(40), location VARCHAR(40), offspring VARCHAR(40), orientation VARCHAR(30), pets VARCHAR(40), religion VARCHAR(40), sex VARCHAR(40) NOT NULL, speaks VARCHAR(40), password VARCHAR(40) NOT NULL, name VARCHAR(40) NOT NULL,  email VARCHAR(50),CONSTRAINT user_pk PRIMARY KEY (userID));

