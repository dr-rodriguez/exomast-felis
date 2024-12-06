
CREATE TABLE exomast."Sources" (
	id BIGSERIAL, 
	type VARCHAR(30) NOT NULL, 
	survey VARCHAR(30) NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id)
)

;
CREATE INDEX "PK_Sources_id" ON exomast."Sources" (id);
COMMENT ON TABLE exomast."Sources" IS 'Main table for ExoMAST objects (planets, brown dwarfs)';
COMMENT ON COLUMN exomast."Sources".id IS 'Main source identifier';
COMMENT ON COLUMN exomast."Sources".type IS 'Type of source (eg, exoplanet, brown dwarf, etc)';
COMMENT ON COLUMN exomast."Sources".survey IS 'Originating survey (eg, nexsci, TOI, etc)';
COMMENT ON COLUMN exomast."Sources".name IS 'Primary name for this source from survey';

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
COMMENT ON COLUMN exomast."Names".id IS 'Main identfier for an object; links to Sources table';
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
COMMENT ON TABLE exomast."Coords" IS 'Coordinates for ExoMAST objects (planets, brown dwarfs)';
COMMENT ON COLUMN exomast."Coords".id IS 'Main source identifier';
COMMENT ON COLUMN exomast."Coords".ra IS 'ICRS Right Ascension of object';
COMMENT ON COLUMN exomast."Coords".dec IS 'ICRS Declination of object';
COMMENT ON CONSTRAINT "Coords_id_Sources_id" ON exomast."Coords" IS 'Link Coords to Sources table';
COMMENT ON CONSTRAINT check_dec ON exomast."Coords" IS 'Validate Dec range';
COMMENT ON CONSTRAINT check_ra ON exomast."Coords" IS 'Validate RA range';

CREATE TABLE exomast."Properties" (
	id BIGINT, 
	property VARCHAR(30), 
	value DOUBLE PRECISION, 
	PRIMARY KEY (id, property), 
	CONSTRAINT "Properties_id_Sources_id" FOREIGN KEY(id) REFERENCES exomast."Sources" (id)
)

;
COMMENT ON TABLE exomast."Properties" IS 'Properties for ExoMAST objects (planets, brown dwarfs)';
COMMENT ON COLUMN exomast."Properties".id IS 'Main source identifier';
COMMENT ON COLUMN exomast."Properties".property IS 'Name of the property';
COMMENT ON COLUMN exomast."Properties".value IS 'Value of the property';
COMMENT ON CONSTRAINT "Properties_id_Sources_id" ON exomast."Properties" IS 'Link Properties to Sources table';
