CREATE DATABASE IF NOT EXISTS STGM_RAPPORT_REVIZTO_DB;
USE STGM_RAPPORT_REVIZTO_DB;

CREATE TABLE projets
(
    id VARCHAR(255) PRIMARY KEY,
    noDossier VARCHAR(255),
    noProjet VARCHAR(255),
    maitreOuvragge VARCHAR(255),
    entrepreneur VARCHAR(255),
    noVisite VARCHAR(255),
    visitePar VARCHAR(255),
    dateVisite DATETIME,
    presence VARCHAR(255),
    rapportDate DATETIME,
    description VARCHAR(500),
    distribution VARCHAR(500),
    image VARCHAR(255)
);
