INSERT INTO website_exercice (titre, numero) VALUES ("Exo1",1);
INSERT INTO website_exercice (titre, numero) VALUES ("Exo2",2);

INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (1,1);
INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (1,2);
INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (1,3);

INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (2,1);
INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (2,2);
INSERT INTO website_contient_exercice_table (idExercice,idTable) VALUES (2,3);

INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (1,1);
INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (1,2);
INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (1,3);

INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (2,1); 
INSERT INTO website_contient_exercice_question (idExercice,idQuestion) VALUES (2,3);


INSERT INTO website_table  (nom,attribut,remplissage)  VALUES
(
	"article",
	'(NOART INTEGER PRIMARY KEY AUTOINCREMENT, LIBELLE VARCHAR(50), STOCK INTEGER, PRIXINVENT INTEGER);',
	'(LIBELLE,STOCK,PRIXINVENT) VALUES("Dentifrice",32,2); 
	(LIBELLE,STOCK,PRIXINVENT) VALUES("Tapioca",2,23);  
	(LIBELLE,STOCK,PRIXINVENT) VALUES("Ananas",5,5); 
	(LIBELLE,STOCK,PRIXINVENT) VALUES("Lampion",1,50); 
	(LIBELLE,STOCK,PRIXINVENT) VALUES("Nenuphar",10,156);'
);

INSERT INTO website_table (nom,attribut,remplissage) VALUES
(
	"fournisseurs",
	'(NOFOUR INTEGER PRIMARY KEY AUTOINCREMENT, NOMFOUR VARCHAR(50), ADRFOUR VARCHAR(100), VILLEFOUR VARCHAR(50) );',
	'(NOMFOUR,ADRFOUR,VILLEFOUR) Values("Point P","20 rue paumee","Lyon");  
	(NOMFOUR,ADRFOUR,VILLEFOUR) Values("Karibou","52 avenue uneva","Marseille");  
	(NOMFOUR,ADRFOUR,VILLEFOUR) Values("Asus","5685 rue jeanmarie","Washington"); 
	(NOMFOUR,ADRFOUR,VILLEFOUR) Values("Carrefour","30 rue de la République","Paris"); 
	(NOMFOUR,ADRFOUR,VILLEFOUR) Values("Ikea","6 place des babouches","Brest");' 
);

INSERT INTO website_table  (nom,attribut,remplissage)  VALUES
(
	"acheter",
	'(NOFOUR integer,NOART integer,PRIXACHAT integer,DELAI integer,FOREIGN KEY(NOFOUR) REFERENCES fournisseurs(NOFOUR),FOREIGN KEY(NOART) REFERENCES article(NOART) );',
	'VALUES(1,1,2,5);
	VALUES(1,2,1,46);
	VALUES(5,4,13,2);
	VALUES(3,3,1,250);
	VALUES(4,2,99,2);
	VALUES(2,5,5,5);'
);


INSERT INTO website_question (intitule,requete) VALUES
(
	1,
	"numéros et libellés des articles dont le stock est inférieur à 10 ?",
	"SELECT NOART, LIBELLE FROM ARTICLES WHERE STOCK<10;"
);


INSERT INTO website_question (intitule,requete) VALUES
(
	2,
	"Liste des articles dont le prix d'inventaire est compris entre 100 et 300 ?",
	"SELECT * FROM ARTICLES WHERE PRIXINVENT BETWEEN 100 AND 300;"
);


INSERT INTO website_question (intitule,requete) VALUES
(
	3,
	"Liste des fournisseurs dont on ne connaît pas l'adresse ?",
	"SELECT * FROM FOURNISSEURS WHERE ADRFOUR IS NULL;"
);


