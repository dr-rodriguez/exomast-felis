-- Script to build functions

DROP FUNCTION IF EXISTS exomast.get_planet_info(planet_name text);

CREATE OR REPLACE FUNCTION exomast.get_planet_info(planet_name TEXT)
RETURNS TABLE(
    id BIGINT,
    survey VARCHAR(30),
    primary_name VARCHAR(30),
    ra FLOAT,
    decl FLOAT,
    orbital_period FLOAT,
    orbital_period_error FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT s.id, s.survey, s.primary_name, c.ra, c.dec, p.orbital_period, p.orbital_period_error
    FROM exomast."Sources" AS s
    JOIN exomast."Coords" AS c ON c.id = s.id
    JOIN exomast."PlanetProperties" AS p ON p.id = s.id
    WHERE s.id IN (
        SELECT M.id2
        FROM exomast."Matches" AS M
        JOIN exomast."Names" AS N ON M.id1 = N.id
        WHERE N.name = planet_name
    )
    ORDER BY s.id;
END $$ LANGUAGE plpgsql;


-- Example usage
SELECT * FROM exomast.get_planet_info('HAT-P-11 b');

