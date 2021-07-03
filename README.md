# DBS Projekt Auswirkungen der Wirtschaftssektoren

## Relationen:

COUNTRY(
    id: VARCHAR(255), <br>
    name: VARCHAR(255), <br>
    income_group: VARCHAR(255) <br>
    percentage_snapshot_agriculture: NUMERIC, <br>
    percentage_snapshot_industry: NUMERIC, <br>
    percentage_snapshot_service: NUMERIC
    )

YEAR(
    date: INT, is_snapshot: BOOLEAN
)

COUNTRY_IN_YEAR(
    country_id: VARCHAR(255), <br>
    year: INT, <br>
    industry_share: NUMERIC, <br>
    gdp: NUMERIC, <br>
    population: INT, <br>
    emission: NUMERIC
)