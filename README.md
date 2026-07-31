# label-class-query-expressions

ArcGIS Pro script-tool-ready Python script that reads all data layers in a specified map inside an `.aprx` and exports label classes and label expressions to one CSV, including:

- label class title/name values
- whether layer labeling is on for each layer
- label class SQL query values
- whether "Label features in this class" is on for each label class

## Script

- `/home/runner/work/label-class-query-expressions/label-class-query-expressions/export_label_class_query_expressions.py`

## Script tool parameters

1. `aprx_path` (Text) – path to ArcGIS Pro project (`.aprx`) or `CURRENT`
2. `map_name` (Text) – map name inside the project
3. `output_csv` (Text) – destination CSV path

## CSV columns

- `map_name`
- `layer_name`
- `layer_label_is_on`
- `class_title`
- `label_class_query`
- `label_expression`
- `label_is_on`
