DROP VIEW "SYSTEM"."DETECTIONS_COUNT";
DROP TABLE "SYSTEM"."DETECTION";
DROP TABLE "SYSTEM"."IMAGE";
DROP TABLE "SYSTEM"."ROLE_ACTIONS";
DROP TABLE "SYSTEM"."ROLE";
DROP TABLE "SYSTEM"."ACTION";

CREATE COLUMN TABLE IF NOT EXISTS "SYSTEM"."IMAGE" ("ID" BIGINT CS_FIXED GENERATED BY DEFAULT AS IDENTITY NOT NULL ,
	 "DATE" LONGDATE CS_LONGDATE NOT NULL ,
	 PRIMARY KEY ("ID")) UNLOAD PRIORITY 5 AUTO MERGE;

CREATE COLUMN TABLE IF NOT EXISTS "SYSTEM"."DETECTION" ("ID" BIGINT CS_FIXED GENERATED BY DEFAULT AS IDENTITY NOT NULL ,
	 "IMAGE_ID" BIGINT CS_FIXED NOT NULL ,
	 "SCORE" DOUBLE CS_DOUBLE,
	 "X_MIN" DOUBLE CS_DOUBLE,
	 "Y_MIN" DOUBLE CS_DOUBLE,
	 "X_MAX" DOUBLE CS_DOUBLE,
	 "Y_MAX" DOUBLE CS_DOUBLE,
	 "X" DOUBLE CS_DOUBLE,
	 "Y" DOUBLE CS_DOUBLE,
	 PRIMARY KEY ("ID")) UNLOAD PRIORITY 5 AUTO MERGE;
ALTER TABLE "SYSTEM"."DETECTION" ADD FOREIGN KEY ( "IMAGE_ID" ) REFERENCES "SYSTEM"."IMAGE" ("ID") ON UPDATE CASCADE ON DELETE CASCADE;


CREATE VIEW IF NOT EXISTS "SYSTEM"."DETECTIONS_COUNT" ( "YEAR",
	 "MONTH",
	 "DAY",
	 "HOUR",
	 "DATE",
	 "X_REGION",
	 "Y_REGION",
	 "X_START",
	 "X_END",
	 "Y_START",
	 "Y_END",
	 "COUNT" ) AS SELECT
	 "YEAR",
	 "MONTH",
	 "DAY",
	 "HOUR",
	 "DATE",
	 "X_REGION",
	 "Y_REGION",
	 "X_REGION" * 0.1 AS "X_START",
	 ("X_REGION" + 1 ) * 0.1 AS "X_END",
	 "Y_REGION" * 0.1 AS "Y_START",
	 ("Y_REGION" + 1 ) * 0.1 AS "Y_END",
	 COUNT(*) AS "COUNT" 
FROM ( SELECT
	 YEAR( I."DATE" ) AS "YEAR",
	 MONTH( I."DATE") AS "MONTH",
	 DAYOFMONTH( I."DATE" ) AS "DAY",
	 HOUR( I."DATE") AS "HOUR",
	 TO_DATE(I."DATE") AS "DATE",
	 FLOOR( D."X" / 0.1 ) AS "X_REGION",
	 FLOOR( D."Y" / 0.1 ) AS "Y_REGION" 
	FROM DETECTION AS D 
	LEFT OUTER JOIN IMAGE AS I ON D."IMAGE_ID" = I."ID" ) 
GROUP BY "YEAR",
	 "MONTH",
	 "DAY",
	 "HOUR",
	 "DATE",
	 "X_REGION",
	 "Y_REGION" WITH READ ONLY;

CREATE ROW TABLE IF NOT EXISTS "SYSTEM"."ROLE" ( "ID" VARCHAR(10) CS_STRING,
	 "DESCRIPTION" VARCHAR(255) CS_STRING,
	 PRIMARY KEY ( "ID" ) ) ;


CREATE ROW TABLE IF NOT EXISTS "SYSTEM"."ACTION" ( "ID" VARCHAR(10) CS_STRING,
	 "DESCRIPTION" VARCHAR(255) CS_STRING,
	 PRIMARY KEY ( "ID" ) );

CREATE ROW TABLE IF NOT EXISTS "SYSTEM"."ROLE_ACTIONS" ( "ROLE_ID" VARCHAR(10) CS_STRING,
	 "ACTION_ID" VARCHAR(10) CS_STRING,
	 PRIMARY KEY ( "ROLE_ID",
	 "ACTION_ID" ),
	 FOREIGN KEY ( "ROLE_ID" ) REFERENCES "SYSTEM"."ROLE" ("ID") ON UPDATE RESTRICT ON DELETE RESTRICT,
	 FOREIGN KEY ( "ACTION_ID" ) REFERENCES "SYSTEM"."ACTION" ("ID") ON UPDATE RESTRICT ON DELETE RESTRICT ) 
;
ALTER TABLE "SYSTEM"."ROLE_ACTIONS" ADD FOREIGN KEY ( "ROLE_ID" ) REFERENCES "SYSTEM"."ROLE" ("ID") ON UPDATE RESTRICT ON DELETE RESTRICT
;
ALTER TABLE "SYSTEM"."ROLE_ACTIONS" ADD FOREIGN KEY ( "ACTION_ID" ) REFERENCES "SYSTEM"."ACTION" ("ID") ON UPDATE RESTRICT ON DELETE RESTRICT
;
