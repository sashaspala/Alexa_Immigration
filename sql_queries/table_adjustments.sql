/*
alter table
	backendDB.UserInfo 
	drop column id;

alter table 
	backendDB.UserInfo 
	add uid INT primary key auto_increment;

insert into backendDB.UserInfo 
	(age,sex,education,language)
	values (25, 'male', 'grad student', 'English');
*/
/*
insert into backendDB.UserInfo 
	(age,sex,education,language)
	values (29, 'male', 'grad student', 'Spanish');
insert into backendDB.UserInfo 
	(age,sex,education,language)
	values (22, 'female', 'grad student', 'English');
insert into backendDB.UserInfo 
	(age,sex,education,language)
	values (25, 'male', 'grad student', 'Mandarin');
*/
/*
delete from backendDB.UserInfo
	where uid<3;
*/
/*
alter table 
	backendDB.UserInfo 
	add name varchar(45);
update 
	backendDB.UserInfo
	set name='Person1'
	where uid=6;
update 
	backendDB.UserInfo
	set name='Person2'
	where uid=5;
update 
	backendDB.UserInfo
	set name='Person3'
	where uid=4;
update 
	backendDB.UserInfo
	set name='Person4'
	where uid=3;
drop table backendDB.UsersList;
*/
/*
alter table
	backendDB.UserContext 
	drop column id;
alter table 
	backendDB.UserContext 
	add context_id INT primary key auto_increment;
*/
/*
set foreign_key_checks=0;
alter table backendDB.CountryList 
	modify id int auto_increment;
set foreign_key_checks=1;
alter table backendDB.FactsList 
	modify idFactsList int auto_increment;
*/
/*
delete from backendDB.FactsList
	where idFactsList < 15;
alter table backendDB.FactsList 
	modify fact varchar(140);
*/
/*
create table backendDB.CityList (
	id int not null auto_increment,
	countryId int,
	name varchar(45),
	primary key (id),
	foreign key (countryID) references backendDB.CountryList (id)
	);
*/
/*
update 
	backendDB.FactsList
	set intent='INFORM'
	where idFactsList>13;
update 
	backendDB.FactsList
	set intent='MOVE'
	where idFactsList=15;
*/
/*
update 
	backendDB.UserInfo
	set industry='NLP'
	where uid>0;
*/
/*
alter table backendDB.FactsList
	add topic varchar(45);
*/
/*
# the economy | government | weather | human rights | politics
update backendDB.FactsList
	set topic = 'economy'
	where idFactsList=14;
*/
/*
insert into backendDB.FactsList
	(countryid, fact, intent, city, industry, topic)
	values (1, 'Canadian winters can get cold', 'INFORM', null, null, 'weather');
insert into backendDB.FactsList
	(countryid, fact, intent, city, industry, topic)
	values (1, 'The province of Nunavut is very, very cold', 'INFORM', 35, null, 'weather');
insert into backendDB.FactsList
	(countryid, fact, intent, city, industry, topic)
	values (3, 'The summer solstice takes place in December in the Southern Hemisphere', 'INFORM', null, null, 'weather');
insert into backendDB.FactsList
	(countryid, fact, intent, city, industry, topic)
	values (1, 'Toronto has a rich history of colorful local politicians', 'INFORM', 28, null, 'politics');
insert into backendDB.FactsList
	(countryid, fact, intent, city, industry, topic)
	values (2, 'Winter in the UK is mild', 'INFORM', null, null, 'weather');
insert into backendDB.FactsList
	(countryid, fact, intent, city, industry, topic)
	values (1, 'Manchester has an average of 140 rainy days per year', 'INFORM', 42, null, 'weather');
insert into backendDB.FactsList
	(countryid, fact, intent, city, industry, topic)
	values (1, 'You know, Nuance has an office in Montreal', 'JOB', null, 'NLP', null);
*/


select
	* 
	from backendDB.FactsList
	limit 100;
