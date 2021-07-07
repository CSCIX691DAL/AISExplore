DROP TABLE IF EXISTS AIS_MESSAGE5;
CREATE TABLE IF NOT EXISTS AIS_MESSAGE5
(
    mmsi                   INT       NOT NULL PRIMARY KEY,
    imo_number             INT       NOT NULL,
    vessel_name            VARCHAR   NOT NULL,
    destination            VARCHAR   NOT NULL,
    call_sign              VARCHAR   NOT NULL,
    ship_type              INT       NOT NULL,
    position_fix_type      INT       NOT NULL,
    dimension_to_bow       INT       NOT NULL,
    dimension_to_stern     INT       NOT NULL,
    dimension_to_port      INT       NOT NULL,
    dimension_to_starboard INT       NOT NULL,
    draught                INT       NOT NULL,
    eta_day                INT       NOT NULL,
    eta_hour               INT       NOT NULL,
    eta_minute             INT       NOT NULL,
    eta_month              INT       NOT NULL,
    event_time             TIMESTAMP NOT NULL
);
CREATE INDEX ON AIS_MESSAGE5 (mmsi);
CREATE INDEX ON AIS_MESSAGE5 (vessel_name);
CREATE INDEX ON AIS_MESSAGE5 (imo_number);
SELECT *
from AIS_MESSAGE5;