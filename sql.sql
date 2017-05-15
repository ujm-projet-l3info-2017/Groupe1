TRUNCATE TABLE website_exercice;
TRUNCATE TABLE website_contient_exercice_table;
TRUNCATE TABLE website_contient_exercice_question;
TRUNCATE TABLE website_table;
TRUNCATE TABLE website_question;




INSERT INTO website_exercice (titre, numero) VALUES ("Exo1",1);
INSERT INTO website_exercice (titre, numero) VALUES ("Exo2",2);
INSERT INTO website_exercice (titre, numero) VALUES ("Exo3",3);

INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (1,1);
INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (1,2);
INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (1,3);

INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (2,7);
INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (2,8);

INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (3,4);
INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (3,5);
INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (3,6);

INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (1,1);
INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (1,2);
INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (1,3);

INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (2,8); 
INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (2,9);

INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (3,4); 
INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (3,5);
INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (3,6);
INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (3,7);



INSERT INTO website_table  (nom,attribut,remplissage)  VALUES
(
	"article",
	'(NOART INTEGER NOT NULL AUTO_INCREMENT, LIBELLE VARCHAR(50), STOCK INTEGER, PRIXINVENT INTEGER, PRIMARY KEY (NOART));',
	'(LIBELLE,STOCK,PRIXINVENT) VALUES("Dentifrice",32,2); 
	(LIBELLE,STOCK,PRIXINVENT) VALUES("Tapioca",2,23);  
	(LIBELLE,STOCK,PRIXINVENT) VALUES("Ananas",5,5); 
	(LIBELLE,STOCK,PRIXINVENT) VALUES("Lampion",1,50); 
	(LIBELLE,STOCK,PRIXINVENT) VALUES("Nenuphar",10,156);'
);

INSERT INTO website_table (nom,attribut,remplissage) VALUES
(
	"fournisseurs",
	'(NOFOUR INTEGER NOT NULL AUTO_INCREMENT, NOMFOUR VARCHAR(50), ADRFOUR VARCHAR(100), VILLEFOUR VARCHAR(50), PRIMARY KEY (NOFOUR));',
	'(NOMFOUR,ADRFOUR,VILLEFOUR) Values("Point P","20 rue paumee","Lyon");  
	(NOMFOUR,ADRFOUR,VILLEFOUR) Values("Karibou","52 avenue uneva","Marseille");  
	(NOMFOUR,ADRFOUR,VILLEFOUR) Values("Asus","5685 rue Jeanne Arc","Washington"); 
	(NOMFOUR,ADRFOUR,VILLEFOUR) Values("Carrefour","30 rue de la République","Paris");
	(NOMFOUR,ADRFOUR,VILLEFOUR) Values("Decathlon ","2 impasse du calvaire","Lyon");
	(NOMFOUR,ADRFOUR,VILLEFOUR) Values("Ikea","6 place des babouches","Brest");' 
);

INSERT INTO website_table  (nom,attribut,remplissage)  VALUES
(
	"acheter",
	'(NOACHAT INTEGER NOT NULL AUTO_INCREMENT, NOFOUR integer,NOART integer,PRIXACHAT integer,DELAI integer, PRIMARY KEY (NOACHAT));',
	'(NOFOUR, NOART, PRIXACHAT, DELAI) VALUES(1,1,2,5);
	 (NOFOUR, NOART, PRIXACHAT, DELAI) VALUES(1,2,1,46);
   (NOFOUR, NOART, PRIXACHAT, DELAI) VALUES(5,4,13,2);
   (NOFOUR, NOART, PRIXACHAT, DELAI) VALUES(3,3,1,250);
	 (NOFOUR, NOART, PRIXACHAT, DELAI) VALUES(4,2,99,2);
	 (NOFOUR, NOART, PRIXACHAT, DELAI) VALUES(2,5,5,5);'
);

INSERT INTO website_table (nom, attribut, remplissage) VALUES
(
	"films",
	'(NOFILM INTEGER NOT NULL AUTO_INCREMENT, TITRE VARCHAR(50), ANNEE INTEGER, RECETTES BIGINT, PRIMARY KEY (NOFILM));',
	'(TITRE,ANNEE,RECETTES) VALUES("Avatar ",2009,2787965087);
	(TITRE,ANNEE,RECETTES) VALUES("Titanic ",1997,2186772302);
	(TITRE,ANNEE,RECETTES) VALUES("Star Wars:The Force Awakens",2015,2068223624);
	(TITRE,ANNEE,RECETTES) VALUES("Jurrassic World ",2015,1671713208);
	(TITRE,ANNEE,RECETTES) VALUES("The Avengers ",2012,1518812988);
	(TITRE,ANNEE,RECETTES) VALUES("Furious 7 ",2015,1516045911);
	(TITRE,ANNEE,RECETTES) VALUES("Avengers: Age of Ultron ",2015,1405403694);
	(TITRE,ANNEE,RECETTES) VALUES("Harry Potter and the Deathly Hallows - Part 2 ",2011,1341511219);
	(TITRE,ANNEE,RECETTES) VALUES("Frozen",2013,1287000000);
	(TITRE,ANNEE,RECETTES) VALUES("Iron Man 3",2013,1214811252);	
	(TITRE,ANNEE,RECETTES) VALUES("Beauty and the Beast",2017,1188581648);
	(TITRE,ANNEE,RECETTES) VALUES("The Fate of the Furious",2017,1168383379);
	(TITRE,ANNEE,RECETTES) VALUES("Minions",2015,1159398397);'
	
);

INSERT INTO website_table(nom, attribut, remplissage) VALUES
(
	"acteurs",
	'(NOACTEUR INTEGER AUTO_INCREMENT, NOM VARCHAR(50), PRENOM VARCHAR(50), ANNEENAISS INTEGER, PRIMARY KEY(NOACTEUR) );',
	'(NOM, PRENOM, ANNEENAISS) VALUES ("Worthington","Sam",1976); 
	(NOM, PRENOM, ANNEENAISS) VALUES ("Lang","Stephen",1952);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Weaver","Sigourney",1949);
	(NOM, PRENOM, ANNEENAISS) VALUES ("DiCaprio","Leonardo",1974);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Winslet","Kate",1975);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Ford","Harrison",1942);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Hamill","Mark",1951);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Fisher","Carrie",1956);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Pratt","Chris",1979);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Dallas Howard","Bryce",1981);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Downey Jr","Robert",1965);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Evans","Chris",1981);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Ruffalo","Mark",1967);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Diesel","Vin",1967);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Walker","Paul",1973);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Johnson","Dwayne",1972);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Hemsworth","Chris",1983);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Radcliffe","Daniel",1989);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Grint","Rupert",1988);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Watson","Emma",1990);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Bonham Carter","Helena",1966);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Bell","Kristen",1980);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Menzel","Idina",1971);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Paltrow","Gwyneth",1972);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Stevens","Dan",1982);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Rodriguez","Michelle",1978);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Bullock","Sandra",1964);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Hamm","Jon",1971);
	(NOM, PRENOM, ANNEENAISS) VALUES ("Keaton","Michael",1951);'
);
	
INSERT INTO website_table (nom, attribut, remplissage) VALUES
(
	"joueDans",
	'(NOJOUEDANS INTEGER AUTO_INCREMENT ,NOFILM INTEGER, NOACTEUR INTEGER, PRIMARY KEY(NOJOUEDANS));',
	'(NOFILM, NOACTEUR) VALUES(1,1);
	(NOFILM, NOACTEUR) VALUES(1,2);
	(NOFILM, NOACTEUR) VALUES(1,3);
	(NOFILM, NOACTEUR) VALUES(2,4);
	(NOFILM, NOACTEUR) VALUES(2,5);
	(NOFILM, NOACTEUR) VALUES(3,6);
	(NOFILM, NOACTEUR) VALUES(3,7);
	(NOFILM, NOACTEUR) VALUES(3,8);
	(NOFILM, NOACTEUR) VALUES(4,9);
	(NOFILM, NOACTEUR) VALUES(4,10);
	(NOFILM, NOACTEUR) VALUES(5,11);
	(NOFILM, NOACTEUR) VALUES(5,12);
	(NOFILM, NOACTEUR) VALUES(5,13);
	(NOFILM, NOACTEUR) VALUES(6,14);
	(NOFILM, NOACTEUR) VALUES(6,15);
	(NOFILM, NOACTEUR) VALUES(6,16);
	(NOFILM, NOACTEUR) VALUES(7,11);
	(NOFILM, NOACTEUR) VALUES(7,12);
	(NOFILM, NOACTEUR) VALUES(7,13);
	(NOFILM, NOACTEUR) VALUES(7,17);
	(NOFILM, NOACTEUR) VALUES(5,17);
	(NOFILM, NOACTEUR) VALUES(8,18);
	(NOFILM, NOACTEUR) VALUES(8,19);
	(NOFILM, NOACTEUR) VALUES(8,20);
	(NOFILM, NOACTEUR) VALUES(8,21);
	(NOFILM, NOACTEUR) VALUES(9,22);
	(NOFILM, NOACTEUR) VALUES(9,23);
	(NOFILM, NOACTEUR) VALUES(10,24);
	(NOFILM, NOACTEUR) VALUES(10,11);
	(NOFILM, NOACTEUR) VALUES(11,20);
	(NOFILM, NOACTEUR) VALUES(11,25);
	(NOFILM, NOACTEUR) VALUES(6,26);
	(NOFILM, NOACTEUR) VALUES(12,26);
	(NOFILM, NOACTEUR) VALUES(12,14);
	(NOFILM, NOACTEUR) VALUES(12,16);
	(NOFILM, NOACTEUR) VALUES(13,27);
	(NOFILM, NOACTEUR) VALUES(13,28);
	(NOFILM, NOACTEUR) VALUES(13,29);'
);	


INSERT INTO website_table  (nom,attribut,remplissage)  VALUES
(
	"consommateurs",
	'(NUMU INTEGER NOT NULL AUTO_INCREMENT, PRENOM VARCHAR(50), NOM VARCHAR(50), PRIMARY KEY (NUMU));',
	'(PRENOM,NOM) VALUES("Jean","Jugnot"); 
	(PRENOM,NOM) VALUES("Jeanne","Jugna");  
	(PRENOM,NOM) VALUES("Jannot","Jon"); 
	(PRENOM,NOM) VALUES("Jade","Jedi"); 
	(PRENOM,NOM)  VALUES("Jeannette","Jhin");'
);



INSERT INTO website_table  (nom,attribut,remplissage)  VALUES
(
	"consommationeau",
	'(NUMU INTEGER NOT NULL, CONS INT(50),PRIMARY KEY (NUMU,CONS));',
	'(NUMU,CONS) VALUES(1,50); 
	(NUMU,CONS) VALUES(2,60);  
	(NUMU,CONS) VALUES(3,70); 
	(NUMU,CONS) VALUES(4,56); 
	(NUMU,CONS) VALUES(5,55);'
);


INSERT INTO website_question (numero,intitule,requete) VALUES
(
	1,
	"numéros et libellés des articles dont le stock est inférieur à 10 ?",
	"SELECT NOART, LIBELLE FROM article WHERE STOCK<10;"
);


INSERT INTO website_question (numero,intitule,requete) VALUES
(
	2,
	"Liste des articles dont le prix inventaire est inferieur a 300 ?",
	"SELECT * FROM article WHERE PRIXINVENT<300;"
);


INSERT INTO website_question (numero,intitule,requete) VALUES
(
	3,
	"Liste des fournisseurs qui se situent a Lyon ?",
	"SELECT * FROM fournisseurs WHERE VILLEFOUR='Lyon';"
);





INSERT INTO website_question (numero,intitule,requete) VALUES
(
	1,
	"Liste des films sortis avant 2000 ?",
	"SELECT * FROM films WHERE ANNEE < 2000;"
);

INSERT INTO website_question (numero,intitule,requete) VALUES
(
	2,
	"Liste des films dans lesquels Emma Watson a joué ?",
	"SELECT films.NOFILM, films.TITRE, films.ANNEE, films.RECETTES FROM films, acteurs, joueDans WHERE films.NOFILM=joueDans.NOFILM AND acteurs.NOACTEUR=joueDans.NOACTEUR AND acteurs.NOM = 'Watson' AND acteurs.PRENOM='Emma';"
);

INSERT INTO website_question (numero,intitule,requete) VALUES
(
	3,
	"Liste des films ayant engrangé moins de 15 milliard de dollars de recettes ?",
	"SELECT * FROM films WHERE RECETTES<1500000000;"
);

INSERT INTO website_question (numero,intitule,requete) VALUES
(
	4,
	"Liste des films?",
	"SELECT * FROM films"
);


INSERT INTO website_question (numero,intitule,requete) VALUES
(
	1,
	"Liste des prenoms des consommateurs et de leur consommation d\'eau par ordre croissant?",
	"SELECT PRENOM,CONS FROM consommateurs,consommationeau WHERE consommateurs.NUMU=consommationeau.NUMU order by CONS ASC"
);


INSERT INTO website_question (numero,intitule,requete) VALUES
(
	2,
	"Nom prenom du plus petit consommateur deau",
	"SELECT NOM,PRENOM FROM consommateurs,consommationeau WHERE consommateurs.NUMU=consommationeau.NUMU AND CONS<=(SELECT MIN(CONS) from consommationeau)"
);
