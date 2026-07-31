import csv
import os

import arcpy


def _bool_to_text(value):
    if value is None:
        return ""
    return "True" if bool(value) else "False"


def _get_definition_queries(layer):
    queries = []

    if layer.supports("DEFINITIONQUERY"):
        try:
            queries = list(layer.listDefinitionQueries() or [])
        except Exception:
            queries = []

        if not queries:
            sql = getattr(layer, "definitionQuery", "")
            if sql:
                queries = [{"name": "", "sql": sql, "isActive": True}]

    return queries


def _get_label_classes(layer):
    if not layer.supports("SHOWLABELS"):
        return []

    try:
        return list(layer.listLabelClasses() or [])
    except Exception:
        return []


def export_label_classes_and_queries(aprx_path, map_name, output_csv):
    aprx = arcpy.mp.ArcGISProject(aprx_path)
    maps = [m for m in aprx.listMaps() if m.name == map_name]
    if not maps:
        raise ValueError("Map not found: {}".format(map_name))

    map_obj = maps[0]
    rows = []

    for layer in map_obj.listLayers():
        if getattr(layer, "isGroupLayer", False):
            continue

        definition_queries = _get_definition_queries(layer)
        label_classes = _get_label_classes(layer)

        if not definition_queries:
            definition_queries = [None]
        if not label_classes:
            label_classes = [None]

        for definition_query in definition_queries:
            for label_class in label_classes:
                rows.append(
                    {
                        "map_name": map_obj.name,
                        "layer_name": layer.name,
                        "layer_long_name": getattr(layer, "longName", layer.name),
                        "layer_visible": _bool_to_text(getattr(layer, "visible", None)),
                        "labels_enabled": _bool_to_text(getattr(layer, "showLabels", None)),
                        "definition_query_name": "" if definition_query is None else definition_query.get("name", ""),
                        "definition_query_sql": "" if definition_query is None else definition_query.get("sql", ""),
                        "definition_query_is_active": "" if definition_query is None else _bool_to_text(definition_query.get("isActive")),
                        "label_class_name": "" if label_class is None else getattr(label_class, "className", ""),
                        "label_class_sql_query": "" if label_class is None else getattr(label_class, "SQLQuery", ""),
                        "label_expression": "" if label_class is None else getattr(label_class, "expression", ""),
                        "label_class_is_active": "" if label_class is None else _bool_to_text(getattr(label_class, "visible", None)),
                    }
                )

    output_dir = os.path.dirname(output_csv)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fieldnames = [
        "map_name",
        "layer_name",
        "layer_long_name",
        "layer_visible",
        "labels_enabled",
        "definition_query_name",
        "definition_query_sql",
        "definition_query_is_active",
        "label_class_name",
        "label_class_sql_query",
        "label_expression",
        "label_class_is_active",
    ]

    with open(output_csv, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def main():
    aprx_path = arcpy.GetParameterAsText(0)
    map_name = arcpy.GetParameterAsText(1)
    output_csv = arcpy.GetParameterAsText(2)

    row_count = export_label_classes_and_queries(aprx_path, map_name, output_csv)

    arcpy.AddMessage("Export complete.")
    arcpy.AddMessage("Map: {}".format(map_name))
    arcpy.AddMessage("Rows written: {}".format(row_count))
    arcpy.AddMessage("CSV: {}".format(output_csv))


if __name__ == "__main__":
    main()
