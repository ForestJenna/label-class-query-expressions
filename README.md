# label-class-query-expressions

ArcGIS Pro script-tool-ready Python script that reads all data layers in a specified map inside an `.aprx` and exports label classes and label expressions to one CSV, including:

- multiple definition queries per layer
- query and expression title/name values
- active status for each query and each label class expression

## Script

- `/home/runner/work/label-class-query-expressions/label-class-query-expressions/export_label_class_query_expressions.py`

## Script tool parameters

1. `aprx_path` (Text) – path to ArcGIS Pro project (`.aprx`) or `CURRENT`
2. `map_name` (Text) – map name inside the project
3. `output_csv` (Text) – destination CSV path

## CSV columns

- `map_name`
- `layer_name`
- `layer_long_name`
- `layer_visible`
- `labels_enabled`
- `definition_query_name`
- `definition_query_sql`
- `definition_query_is_active`
- `label_class_name`
- `label_class_sql_query`
- `label_expression`
- `label_class_is_active`
