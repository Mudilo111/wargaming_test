CREATE_TABLE_WEAPONS = 'CREATE TABLE weapons(' \
                       '"weapon" text NOT NULL unique,' \
                       '"reload speed" integer NOT NULL,' \
                       '"rotational speed" integer NOT NULL,' \
                       '"diameter" integer NOT NULL,' \
                       '"power volley" integer NOT NULL,' \
                       '"count" integer NOT NULL,' \
                       'PRIMARY KEY("weapon")' \
                       ');'

CREATE_TABLE_HULLS = 'CREATE TABLE hulls(' \
                     '"hull" text NOT NULL unique,' \
                     '"armor" integer NOT NULL,' \
                     '"type" integer NOT NULL,' \
                     '"capacity" integer NOT NULL, ' \
                     'PRIMARY KEY("hull")' \
                     ');'

CREATE_TABLE_ENGINES = 'CREATE TABLE engines(' \
                       '"engine" text NOT NULL unique,' \
                       '"power" integer NOT NULL,' \
                       '"type" integer NOT NULL,' \
                       'PRIMARY KEY("engine")' \
                       ');'

CREATE_TABLE_SHIPS = 'CREATE TABLE Ships(' \
                     '"ship" text NOT NULL unique,' \
                     '"weapon" text NOT NULL,' \
                     '"hull" text NOT NULL,' \
                     '"engine" text NOT NULL,' \
                     'PRIMARY KEY("ship"),' \
                     'FOREIGN KEY("weapon") REFERENCES weapons("weapon"),' \
                     'FOREIGN KEY("hull") REFERENCES hulls("hull"),' \
                     'FOREIGN KEY("engine") REFERENCES engines("engine")' \
                     ');'

INSERT_QUERY = 'INSERT INTO {table_name} {table_rows} values ' \
               '{rows_values}'

UPDATE_QUERY = 'UPDATE {table_name} ' \
               'SET "{row_name}" = "{row_value}" ' \
               'WHERE "{primary_key_name}" = "{primary_key_value}"'

SELECT_ALL_QUERY = 'SELECT * FROM {table_name}'

SELECT_ROW_QUERY = 'SELECT * FROM {table_name} ' \
               'WHERE "{primary_key_name}" = "{primary_key_value}"'

