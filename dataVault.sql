/* Create a database named smdvault */
CREATE DATABASE smdvault;

/* Connect to the database named smdvault */
\connect smdvault

/* Create a schema named smdvaultschema */
CREATE SCHEMA smdvaultschema;

/* Create a table named 'HubExperiment' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.HubExperiment
(
	sequence VARCHAR(100) NOT NULL UNIQUE,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source)
);

/* Create a table named 'SatExperimentTitle' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SatExperimentTitle
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	title varchar(255) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (sequence) REFERENCES smdvaultschema.HubExperiment(sequence)
);

/* Create a table named 'SatExperimentAcronym' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SatExperimentAcronym
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	acronym varchar(15) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (sequence) REFERENCES smdvaultschema.HubExperiment(sequence)
);

/* Create a table named 'HubExperimentalUnit' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.HubExperimentalUnit
(
	sequence VARCHAR(100) NOT NULL UNIQUE,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source)
);

/* Create a table named 'ParticipatesIn' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.ParticipatesIn
(
	sequence VARCHAR(100) NOT NULL UNIQUE,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	experimentalUnit VARCHAR(100) NOT NULL,
	experiment VARCHAR(100) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (experimentalUnit) REFERENCES smdvaultschema.HubExperimentalUnit(sequence),
	FOREIGN KEY (experiment) REFERENCES smdvaultschema.HubExperiment(sequence)
);

/* Create a table named 'SatExperimentlUnitIdentifier' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SatExperimentlUnitIdentifier
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	ID VARCHAR(15) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (sequence) REFERENCES smdvaultschema.ParticipatesIn(sequence)
);

/* Create a table named 'HubFactor' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.HubFactor
(
	sequence VARCHAR(100) NOT NULL UNIQUE,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	experiment VARCHAR(100) NOT NULL,
	isCofactor BOOLEAN NOT NULL DEFAULT FALSE,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (experiment) REFERENCES smdvaultschema.HubExperiment(sequence)
);

/* Create a table named 'SatFactorName' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SatFactorName
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	name VARCHAR(40) NOT NULL,
	PRIMARY KEY (sequence),
	FOREIGN KEY (sequence) REFERENCES smdvaultschema.HubFactor(sequence)
);

/* Create a table named 'SatFactorLevel' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SatFactorLevel
(
	sequence VARCHAR(100) NOT NULL UNIQUE,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	levelValue VARCHAR(40) NOT NULL,
	PRIMARY KEY (sequence),
	FOREIGN KEY (sequence) REFERENCES smdvaultschema.HubFactor(sequence)
);

/* Create a table named 'HubTreatment' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.HubTreatment
(
	sequence VARCHAR(100) NOT NULL UNIQUE,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	experiment VARCHAR(100) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (experiment) REFERENCES smdvaultschema.HubExperiment(sequence)
);

/* Create a table named 'SatTreatmentFactorLevel' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SatTreatmentFactorLevel
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	factorLevel VARCHAR(100) NOT NULL,
	PRIMARY KEY (sequence),
	FOREIGN KEY (sequence) REFERENCES smdvaultschema.HubTreatment(sequence),
	FOREIGN KEY (factorLevel) REFERENCES smdvaultschema.SatFactorLevel(sequence)
);

/* Create a table named 'HubGroup' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.HubGroup
(
	sequence VARCHAR(100) NOT NULL UNIQUE,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	treatment VARCHAR(100) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (treatment) REFERENCES smdvaultschema.HubTreatment(sequence)
);

/* Create a table named 'SatGroupName' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SatGroupName
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	name VARCHAR(40) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (sequence) REFERENCES smdvaultschema.HubGroup(sequence)
);

/* Create a table named 'AssignedTo' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.AssignedTo
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	experimentalUnit VARCHAR(100) NOT NULL,
	groupp VARCHAR(100) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (experimentalUnit) REFERENCES smdvaultschema.HubExperimentalUnit(sequence),
	FOREIGN KEY (groupp) REFERENCES smdvaultschema.HubGroup(sequence)
);

/* Create a table named 'HubSession' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.HubSession
(
	sequence VARCHAR(100) NOT NULL UNIQUE,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source)
);

/* Create a table named 'SatSessionName' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SatSessionName
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	name VARCHAR(40) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (sequence) REFERENCES smdvaultschema.HubSession(sequence)
);

/* Create a table named 'AttendsSession' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.AttendsSession
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	experimentalUnit VARCHAR(100) NOT NULL,
	groupp VARCHAR(100) NOT NULL,
	session VARCHAR(100) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (experimentalUnit) REFERENCES smdvaultschema.HubExperimentalUnit(sequence),
	FOREIGN KEY (groupp) REFERENCES smdvaultschema.HubGroup(sequence),
	FOREIGN KEY (session) REFERENCES smdvaultschema.HubSession(sequence)
);

/* Create a table named 'HubObservation' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.HubObservation
(
	sequence VARCHAR(100) NOT NULL UNIQUE,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	collectedAtsession VARCHAR(100) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (collectedAtSession) REFERENCES smdvaultschema.HubSession(sequence)
);

/* Create a table named 'SatObservationName' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SatObservationName
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	name VARCHAR(40) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (sequence) REFERENCES smdvaultschema.HubObservation(sequence)
);

/* Create a table named 'SatObservationValue' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SatObservationValue
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	value  integer ARRAY,
	timestamps timestamp ARRAY,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (sequence) REFERENCES smdvaultschema.HubObservation(sequence)
);

/* Create a table named 'HubMetaData' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.HubMetaData
(
	sequence VARCHAR(100) NOT NULL UNIQUE,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source)
);

/* Create a table named 'SatMetaDataKeyValuePair' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SatMetaDataKeyValuePair
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	key VARCHAR(40) NOT NULL,
	value OID,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (sequence) REFERENCES smdvaultschema.HubMetaData(sequence)
);

/* Create a table named 'SessionMetaData' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SessionMetaData
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	session VARCHAR(100) NOT NULL,
	metadata VARCHAR(100) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (session) REFERENCES smdvaultschema.HubSession(sequence),
	FOREIGN KEY (metadata) REFERENCES smdvaultschema.HubMetaData(sequence)
);

/* Create a table named 'ObservationMetaData' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.ObservationMetaData
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	observation VARCHAR(100) NOT NULL,
	metadata VARCHAR(100) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (observation) REFERENCES smdvaultschema.HubObservation(sequence),
	FOREIGN KEY (metadata) REFERENCES smdvaultschema.HubMetaData(sequence)
);

/* Create a table named 'HubSubject' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.HubSubject
(
	sequence VARCHAR(100) NOT NULL UNIQUE,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	name VARCHAR(40) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source)
);

/* Create a table named 'SatSubjectAge' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SatSubjectAge
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	age integer NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (sequence) REFERENCES smdvaultschema.HubSubject(sequence)
);

/* Create a table named 'SatSubjectName' under schema named 'smdvaultschema' */
CREATE TABLE smdvaultschema.SatSubjectName
(
	sequence VARCHAR(100) NOT NULL,
	timestamp TIME NOT NULL,
	source VARCHAR(200) NOT NULL,
	name VARCHAR(40) NOT NULL,
	PRIMARY KEY (sequence,timestamp,source),
	FOREIGN KEY (sequence) REFERENCES smdvaultschema.HubSubject(sequence)
);
