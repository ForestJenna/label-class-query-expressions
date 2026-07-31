import csv
import os

import arcpy


def _is_data_layer(layer):
    if getattr(layer, "isGroupLayer", False):
        return False
    try:
        return layer.supports("DEFINITIONQUERY")
    except Exception:
        return False


def _list_layer_definition_queries(layer):
    queries = []
    try:
        query_items = layer.listDefinitionQueries() or []
    except Exception:
        query_items = []

    for item in query_items:
        title = item.get("name", "")
        sql = item.get("sql", "")
        is_active = bool(item.get("isActive", False))
        queries.append((title, sql, is_active))

    if queries:
        return queries

    fallback_sql = getattr(layer, "definitionQuery", "") or ""
    if fallback_sql:
        return [("", fallback_sql, True)]
    return [("", "", False)]


def _list_layer_label_expressions(layer):
    if not layer.supports("SHOWLABELS"):
        return [("", "", "", False)]

    try:
        label_classes = list(layer.listLabelClasses() or [])
    except Exception:
        label_classes = []

    expressions = []
    for label_class in label_classes:
        expression_title = getattr(label_class, "className", "")
        label_class_query = getattr(label_class, "SQLQuery", "")
        label_expression = getattr(label_class, "expression", "")
        expression_is_active = bool(getattr(label_class, "visible", False))
        expressions.append(
            (
                expression_title,
                label_class_query,
                label_expression,
                expression_is_active,
            )
        )

    if expressions:
        return expressions
    return [("", "", "", False)]


def export_label_classes_and_queries(aprx_path, map_name, output_csv):
    aprx = arcpy.mp.ArcGISProject(aprx_path)
    maps = aprx.listMaps(map_name)
    if not maps:
        raise ValueError("Map '{}' was not found in '{}'.".format(map_name, aprx_path))
    map_obj = maps[0]
    os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)

    with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            [
                "map_name",
                "layer_name",
                "query_title",
                "definition_query",
                "is_active",
                "expression_title",
                "label_class_query",
                "label_expression",
                "expression_is_active",
            ]
        )

        row_count = 0
        for layer in map_obj.listLayers():
            if not _is_data_layer(layer):
                continue

            for query_title, definition_query, is_active in _list_layer_definition_queries(layer):
                for (
                    expression_title,
                    label_class_query,
                    label_expression,
                    expression_is_active,
                ) in _list_layer_label_expressions(layer):
                    writer.writerow(
                        [
                            map_obj.name,
                            layer.name,
                            query_title,
                            definition_query,
                            is_active,
                            expression_title,
                            label_class_query,
                            label_expression,
                            expression_is_active,
                        ]
                    )
                    row_count += 1

    arcpy.AddMessage("Label class/query report written to: {}".format(output_csv))
    return row_count


def main():
    aprx_path = arcpy.GetParameterAsText(0)
    map_name = arcpy.GetParameterAsText(1)
    output_csv = arcpy.GetParameterAsText(2)

    row_count = export_label_classes_and_queries(aprx_path, map_name, output_csv)

    arcpy.AddMessage("Export complete.")
    arcpy.AddMessage("Rows written: {}".format(row_count))


if __name__ == "__main__":
    main()
