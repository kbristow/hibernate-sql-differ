from sqlutils import SqlScriptDiffer, SqlComparisonResult

file_new = "current.sql"
file_old = "master.sql"

with open(file_old, "r") as fh:
    original_sql = fh.read()

with open(file_new, "r") as fh:
    new_sql = fh.read()

differ = SqlScriptDiffer(original_sql, new_sql)

diff = differ.diff()

modified = []
new = []
removed = []
for result in diff:
    if result.result == SqlComparisonResult.MODIFIED:
        modified.append(result)
    elif result.result == SqlComparisonResult.NEW:
        new.append(result)
    elif result.result == SqlComparisonResult.REMOVED:
        removed.append(result)


with open("results.sql", "w") as fh:
    fh.write("/*\n---------------NEW---------------\n*/\n")
    for new_statement in new:
        fh.write(new_statement.statement.sql + "\n\n")

    fh.write("\n\n")
    fh.write("/*\n-------------REMOVED-------------\n*/\n")
    for removed_statement in removed:
        fh.write(removed_statement.statement.sql + "\n\n")

    fh.write("\n\n")
    fh.write("/*\n-------------MODIFIED------------\n*/\n")
    for modified_statement in modified:
        fh.write("-- modifed " + modified_statement.statement.sql_id + "\n")
        fh.write(modified_statement.statement.sql + "\n")
        fh.write("-- original " + modified_statement.original.sql_id + "\n")
        fh.write(modified_statement.original.sql + "\n\n")
