
-- Examine results
select COUNT(*) from exomast."Sources";
select max(id) from exomast."Sources";
select count(*) from exomast."Matches";
select * from exomast."Sources" limit 1000;
select * from exomast."PlanetProperties" LIMIT 1000;

-- Join example
select S.primary_name, S.survey, P.orbital_period, P.orbital_period_error 
from exomast."PlanetProperties" as P
join exomast."Sources" as S on S.id = P.id
LIMIT 1000;

-- Check duplicates in Sources
select survey, primary_name, COUNT(*) from exomast."Sources" GROUP BY survey, primary_name HAVING count(*) > 1

-- Single planet search
select * from exomast."Names" as N where N.name in ('Kepler-1498 b');
select * from exomast."Sources" where id in (
    select id from exomast."Names" as N where N.name in ('Kepler-1498 b')
);

-- Exploring matched planets
select id1, COUNT(*) as counts 
from exomast."Matches" 
group by id1 
having COUNT(*) > 1 
order by counts desc
limit 10;

-- Function use
select * from exomast.get_planet_info('HAT-P-11 b');
select * from exomast.get_planet_info('WASP-100 b');
