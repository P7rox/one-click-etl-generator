import re
from catalog import catalog

def generate_simple_sql(selected_datasets, nlp_input):
    if not selected_datasets:
        return "-- No datasets selected"

    joins = []
    tables = list(selected_datasets.keys())
    sql = f"SELECT *\nFROM {tables[0]}"

    for i in range(1, len(tables)):
        left = tables[i-1]
        right = tables[i]
        common_keys = set(catalog[left]) & set(catalog[right])
        if common_keys:
            key = list(common_keys)[0]
            sql += f"\nJOIN {right} ON {left}.{key} = {right}.{key}"
        else:
            sql += f"\nCROSS JOIN {right}"

    filter_match = re.search(r"(amount\s*[><=]+\s*\d+)", nlp_input.lower())
    if filter_match:
        sql += f"\nWHERE {filter_match.group(1)}"

    return sql


def generate_pyspark_code(selected_datasets, nlp_input):
    if not selected_datasets:
        return "# No datasets selected"

    tables = list(selected_datasets.keys())
    code = """# Auto-generated PySpark Code
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("GeneratedETL").getOrCreate()

"""
    # Track columns for each variable
    var_columns = {}

    for t in tables:
        code += f"{t} = spark.table('{t}')\n"
        var_columns[t] = catalog[t]

    last_var = tables[0]

    for i in range(1, len(tables)):
        left = last_var
        right = tables[i]
        left_cols = var_columns[left]
        right_cols = catalog[right]

        common_keys = set(left_cols) & set(right_cols)
        new_var = f"step_{i}"

        if common_keys:
            key = list(common_keys)[0]
            code += f"{new_var} = {left}.join({right}, on='{key}', how='inner')\n"
            var_columns[new_var] = list(set(left_cols + right_cols))
        else:
            code += f"{new_var} = {left}.crossJoin({right})\n"
            var_columns[new_var] = list(set(left_cols + right_cols))

        last_var = new_var

    # Simple filter example
    filter_match = re.search(r"(amount\s*[><=]+\s*\d+)", nlp_input.lower())
    if filter_match:
        code += f"{last_var} = {last_var}.filter(\"{filter_match.group(1)}\")\n"

    code += f"\n{last_var}.show()\n"
    return code
