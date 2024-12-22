-- Script to build functions

CREATE OR REPLACE FUNCTION exomast.get_planet_info(planet_name TEXT)
RETURNS TABLE(
    id INTEGER,
    survey TEXT,
    primary_name TEXT,
    ra FLOAT,
    "dec" FLOAT,
    orbital_period FLOAT,
    orbital_period_error FLOAT,
) AS $$
DECLARE
    matched_ids INTEGER[];
    rec RECORD;
BEGIN
    -- Get the IDs of matching planets
    SELECT ARRAY(
        SELECT DISTINCT(M.id2) FROM exomast."Matches" AS M
        JOIN exomast."Names" AS N ON M.id1=N.id
        WHERE N.name = planet_name) INTO matched_ids;

    -- Check if any IDs were found.
    IF matched_ids IS NULL OR array_length(matched_ids, 1) IS NULL THEN
        RETURN QUERY SELECT NULL AS id, NULL AS survey, NULL AS primary_name, 
        NULL AS ra, NULL AS "dec", 
        NULL AS orbital_period, NULL AS orbital_period_error; -- Return dummy row if no matches
    END IF;

    -- Join tables and return data
    RETURN QUERY
    SELECT s.id, s.survey, s.primary_name, c.ra, c.dec, p.orbital_period, p.orbital_period_error
    FROM exomast."Sources" AS s
    JOIN exomast."Coords" AS c ON c.id=s.id
    JOIN exomast."PlanetProperties" AS p ON p.id = s.id
    INNER JOIN UNNEST(matched_ids) AS xid ON s.id = xid;
END $$ LANGUAGE plpgsql;


-- Example usage
SELECT * FROM exomast.get_planet_info('HAT-P-11 b');

