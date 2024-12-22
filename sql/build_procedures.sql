-- Testing out the logic to write a future SP

DO $$
DECLARE 
    planet_name TEXT := 'HAT-P-11 b';
    matched_ids INTEGER[];
    rec RECORD;
BEGIN
    SELECT ARRAY(
        SELECT DISTINCT(M.id2) FROM exomast."Matches" AS M
        JOIN exomast."Names" AS N ON M.id1=N.id
        WHERE N.name = planet_name) INTO matched_ids;
    --SELECT matched_ids;
    --RAISE NOTICE 'Matched IDs: %', matched_ids; -- Use RAISE NOTICE to display the value

    --SELECT * FROM exomast."PlanetProperties" AS P WHERE P.id in matched_ids;
    FOR rec IN 
        SELECT s.*, c.ra, c.dec, p.*
        FROM exomast."Sources" AS s
        JOIN exomast."Coords" AS c ON c.id=s.id
        JOIN exomast."PlanetProperties" AS p ON p.id = s.id
        INNER JOIN UNNEST(matched_ids) AS xid ON s.id = xid
    LOOP
        RAISE NOTICE '%', rec;
    END LOOP;
END $$ LANGUAGE plpgsql;