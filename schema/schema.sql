
CREATE TABLE exomast."Sources" (
	id BIGSERIAL, 
	source_type VARCHAR(30) NOT NULL, 
	survey VARCHAR(30) NOT NULL, 
	primary_name VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id)
)

;
CREATE INDEX "PK_Sources_id" ON exomast."Sources" (id);
COMMENT ON TABLE exomast."Sources" IS 'Main table for ExoMAST objects (planets, brown dwarfs)';
COMMENT ON COLUMN exomast."Sources".id IS 'Main source identifier';
COMMENT ON COLUMN exomast."Sources".source_type IS 'Type of source (eg, exoplanet, brown dwarf, etc)';
COMMENT ON COLUMN exomast."Sources".survey IS 'Originating survey (eg, nexsci, TOI, etc)';
COMMENT ON COLUMN exomast."Sources".primary_name IS 'Primary name for this source from survey';

CREATE TABLE exomast."Publications" (
	id BIGSERIAL, 
	reference VARCHAR(100) NOT NULL, 
	ref VARCHAR(30), 
	PRIMARY KEY (id)
)

;
COMMENT ON TABLE exomast."Publications" IS 'Publications/references for values in database';
COMMENT ON COLUMN exomast."Publications".id IS 'Publication internal identifier';
COMMENT ON COLUMN exomast."Publications".reference IS 'Publication reference name (eg, Author, et al. 2021)';
COMMENT ON COLUMN exomast."Publications".ref IS 'Publication bibcode';

CREATE TABLE exomast."Matches" (
	id1 BIGINT, 
	id2 BIGINT, 
	PRIMARY KEY (id1, id2), 
	CONSTRAINT "Matches_id1_Sources_id" FOREIGN KEY(id1) REFERENCES exomast."Sources" (id), 
	CONSTRAINT "Matches_id2_Sources_id" FOREIGN KEY(id2) REFERENCES exomast."Sources" (id)
)

;
COMMENT ON TABLE exomast."Matches" IS 'Matching table between exomast sources';
COMMENT ON COLUMN exomast."Matches".id1 IS 'Source identifier';
COMMENT ON COLUMN exomast."Matches".id2 IS 'Source identifier';
COMMENT ON CONSTRAINT "Matches_id2_Sources_id" ON exomast."Matches" IS 'Link Matches to Sources table';
COMMENT ON CONSTRAINT "Matches_id1_Sources_id" ON exomast."Matches" IS 'Link Matches to Sources table';

CREATE TABLE exomast."Names" (
	id BIGINT NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id, name), 
	CONSTRAINT "Names_id_Sources_id" FOREIGN KEY(id) REFERENCES exomast."Sources" (id)
)

;
COMMENT ON TABLE exomast."Names" IS 'Additional identifiers for objects in Sources table';
COMMENT ON COLUMN exomast."Names".id IS 'Main identifier for an object; links to Sources table';
COMMENT ON COLUMN exomast."Names".name IS 'Identifier for source';
COMMENT ON CONSTRAINT "Names_id_Sources_id" ON exomast."Names" IS 'Link Names to Sources table';

CREATE TABLE exomast."Coords" (
	id BIGINT, 
	ra DOUBLE PRECISION, 
	dec DOUBLE PRECISION, 
	PRIMARY KEY (id), 
	CONSTRAINT "Coords_id_Sources_id" FOREIGN KEY(id) REFERENCES exomast."Sources" (id), 
	CONSTRAINT check_ra CHECK (ra >= 0 AND ra <= 360), 
	CONSTRAINT check_dec CHECK (dec >= -90 AND dec <= 90)
)

;
COMMENT ON TABLE exomast."Coords" IS 'Coordinates for ExoMAST objects';
COMMENT ON COLUMN exomast."Coords".id IS 'Main source identifier';
COMMENT ON COLUMN exomast."Coords".ra IS 'ICRS Right Ascension of object';
COMMENT ON COLUMN exomast."Coords".dec IS 'ICRS Declination of object';
COMMENT ON CONSTRAINT "Coords_id_Sources_id" ON exomast."Coords" IS 'Link Coords to Sources table';
COMMENT ON CONSTRAINT check_ra ON exomast."Coords" IS 'Validate RA range';
COMMENT ON CONSTRAINT check_dec ON exomast."Coords" IS 'Validate Dec range';

CREATE TABLE exomast."PlanetProperties" (
	id BIGINT, 
	orbital_period FLOAT, 
	orbital_period_error FLOAT, 
	orbital_period_ref BIGINT, 
	PRIMARY KEY (id), 
	CONSTRAINT "PlanetProperties_id_Sources_id" FOREIGN KEY(id) REFERENCES exomast."Sources" (id), 
	CONSTRAINT "PlanetProperties_id_Publications_id" FOREIGN KEY(orbital_period_ref) REFERENCES exomast."Publications" (id)
)

;
COMMENT ON TABLE exomast."PlanetProperties" IS 'Properties for ExoMAST planets';
COMMENT ON COLUMN exomast."PlanetProperties".id IS 'Main source identifier';
COMMENT ON COLUMN exomast."PlanetProperties".orbital_period IS 'Orbital period in days';
COMMENT ON COLUMN exomast."PlanetProperties".orbital_period_error IS 'Uncertainty of orbital period in days';
COMMENT ON COLUMN exomast."PlanetProperties".orbital_period_ref IS 'Publication identifier for orbital period';
COMMENT ON CONSTRAINT "PlanetProperties_id_Sources_id" ON exomast."PlanetProperties" IS 'Link PlanetProperties to Sources table';
COMMENT ON CONSTRAINT "PlanetProperties_id_Publications_id" ON exomast."PlanetProperties" IS 'Link PlanetProperties to Publications table';

CREATE TABLE exomast."Properties" (
	id BIGINT, 
	property_type VARCHAR(30), 
	property_value FLOAT, 
	property_error FLOAT, 
	property_reference BIGINT, 
	PRIMARY KEY (id, property_type), 
	CONSTRAINT "Properties_id_Sources_id" FOREIGN KEY(id) REFERENCES exomast."Sources" (id), 
	CONSTRAINT "Properties_id_Publications_id" FOREIGN KEY(property_reference) REFERENCES exomast."Publications" (id)
)

;
COMMENT ON TABLE exomast."Properties" IS 'Properties for ExoMAST planets; long-form version';
COMMENT ON COLUMN exomast."Properties".id IS 'Main source identifier';
COMMENT ON COLUMN exomast."Properties".property_type IS 'Property type (eg, the name "orbital period")';
COMMENT ON COLUMN exomast."Properties".property_value IS 'Value of property';
COMMENT ON COLUMN exomast."Properties".property_error IS 'Uncertainty of value';
COMMENT ON COLUMN exomast."Properties".property_reference IS 'Publication reference';
COMMENT ON CONSTRAINT "Properties_id_Sources_id" ON exomast."Properties" IS 'Link Properties to Sources table';
COMMENT ON CONSTRAINT "Properties_id_Publications_id" ON exomast."Properties" IS 'Link Properties to Publications table';
