BEGIN;
CREATE TABLE "ion_channel_experiment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "doi" text NOT NULL);
CREATE TABLE "ion_channel_graph" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "x_axis_type" varchar(50) NOT NULL, "x_axis_unit" varchar(50) NOT NULL, "y_axis_type" varchar(50) NOT NULL, "y_axis_unit" varchar(50) NOT NULL, "figure_ref_address" varchar(500) NOT NULL, "figure_ref_caption" varchar(100) NOT NULL, "file_path" text NOT NULL);
CREATE TABLE "ion_channel_graphdata" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "series_name" varchar(200) NOT NULL, "series_data" text NOT NULL, "graph_id" integer NOT NULL REFERENCES "ion_channel_graph" ("id"));
CREATE TABLE "ion_channel_ionchannelmodel" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "channel_type" text NOT NULL, "ion_type" text NOT NULL, "expressions" text NOT NULL, "experiment_id" integer NOT NULL REFERENCES "ion_channel_experiment" ("id"));
CREATE TABLE "ion_channel_patchclamp" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "type" varchar(200) NOT NULL, "duration" integer NOT NULL, "delta" integer NOT NULL, "start_time" integer NOT NULL, "end_time" integer NOT NULL, "protocol_start" integer NOT NULL, "protocol_end" integer NOT NULL, "protocol_step" integer NOT NULL, "experiment_id" integer NOT NULL REFERENCES "ion_channel_experiment" ("id"));
CREATE TABLE "ion_channel_graph__new" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "x_axis_type" varchar(50) NOT NULL, "x_axis_unit" varchar(50) NOT NULL, "y_axis_type" varchar(50) NOT NULL, "y_axis_unit" varchar(50) NOT NULL, "figure_ref_address" varchar(500) NOT NULL, "figure_ref_caption" varchar(100) NOT NULL, "file_path" text NOT NULL, "experiment_id" integer NOT NULL REFERENCES "ion_channel_patchclamp" ("id"));
INSERT INTO "ion_channel_graph__new" ("figure_ref_address", "file_path", "x_axis_unit", "experiment_id", "figure_ref_caption", "x_axis_type", "y_axis_type", "y_axis_unit", "id") SELECT "figure_ref_address", "file_path", "x_axis_unit", NULL, "figure_ref_caption", "x_axis_type", "y_axis_type", "y_axis_unit", "id" FROM "ion_channel_graph";
DROP TABLE "ion_channel_graph";
ALTER TABLE "ion_channel_graph__new" RENAME TO "ion_channel_graph";
CREATE INDEX "ion_channel_ionchannelmodel_abd1812d" ON "ion_channel_ionchannelmodel" ("experiment_id");
CREATE INDEX "ion_channel_patchclamp_abd1812d" ON "ion_channel_patchclamp" ("experiment_id");
CREATE INDEX "ion_channel_graph_abd1812d" ON "ion_channel_graph" ("experiment_id");

COMMIT;
