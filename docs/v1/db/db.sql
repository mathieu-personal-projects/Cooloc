CREATE TABLE IF NOT EXISTS Colocs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50),
    date_crea TIMESTAMP,
    responsable INT,
);

CREATE TABLE IF NOT EXISTS Utilisateurs (
    id SERIAL PRIMARY KEY,
    mail VARCHAR(50) NOT NULL UNIQUE,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    role VARCHAR(50) NOT NULL,
    mdp VARCHAR(255) NOT NULL,
    date_creation TIMESTAMP,
    num_telephone VARCHAR(15),
    id_coloc INT REFERENCES Colocs(id),
    CONSTRAINT fk_coloc
        FOREIGN KEY(id_coloc)
            REFERENCES Colocs(id)
);

CREATE TABLE IF NOT EXISTS Absences (
    id SERIAL PRIMARY KEY,
    date_crea TIMESTAMP,
    date_debut TIMESTAMP,
    date_fin TIMESTAMP,
    id_utilisateur INT REFERENCES Utilisateurs(id)
);

CREATE TABLE IF NOT EXISTS Depenses (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50),
    montant FLOAT,
    date_paiement TIMESTAMP,
    priorite VARCHAR(50),
    date_fin TIMESTAMP,
    cloture VARCHAR(50),
    id_utilisateur INT REFERENCES Utilisateurs(id)
);

CREATE TABLE IF NOT EXISTS Taches (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50),
    date_debut TIMESTAMP,
    date_fin TIMESTAMP,
    date_crea TIMESTAMP,
    priorite VARCHAR(50),
    cloture VARCHAR(50),
    createur INT REFERENCES Utilisateurs(id),
    atribue_a INT REFERENCES Utilisateurs(id)
);


ALTER TABLE Colocs
ADD CONSTRAINT fk_responsable
FOREIGN KEY (responsable) REFERENCES Utilisateurs(id)
