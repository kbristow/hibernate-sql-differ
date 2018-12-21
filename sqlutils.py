from enum import Enum
from typing import List

import re


class SqlComparisonResult(Enum):
    IDENTICAL = 1
    MODIFIED = 2
    NEW = 3
    REMOVED = 4


class SqlStatement(object):
    def __init__(self, sql: str):
        self.sql = sql.strip() + ";"
        sql_split = re.sub("\n[\s]*", " ", sql).split()
        if self.sql.lower().startswith("alter table"):
            self.sql_id = " ".join(sql_split[0:6])
        else:
            self.sql_id = " ".join(sql.split()[0:3])


class SqlStatementComparison(object):
    def __init__(self, statement: SqlStatement, original_statement: SqlStatement, result: SqlComparisonResult):
        self.statement = statement
        self.original = original_statement
        self.result = result


class SqlScriptDiffer(object):
    def __init__(self, source_script: str, modified_script: str):
        self.source = SqlScript(source_script)
        self.modified = SqlScript(modified_script)

    def diff(self) -> List[SqlStatementComparison]:
        diff_results = []
        for modified_statement in self.modified.statements:
            diff_results.append(self.source.compare(modified_statement))
        for source_statement in self.source.statements:
            comp_result = self.modified.compare(source_statement)
            if comp_result.result == SqlComparisonResult.NEW:
                comp_result.result = SqlComparisonResult.REMOVED
                diff_results.append(comp_result)
        return diff_results


class SqlScript(object):
    def __init__(self, full_script: str):
        self.statements = []
        statements_raw = full_script.split(";\n")
        for statement in statements_raw:
            self.statements.append(SqlStatement(statement))

    def compare(self, statement: SqlStatement):
        comparison_result = SqlComparisonResult.NEW
        matched_statement = None
        for own_statement in self.statements:
            if own_statement.sql_id == statement.sql_id:
                comparison_result = SqlComparisonResult.MODIFIED
                matched_statement = own_statement
                if own_statement.sql == statement.sql:
                    comparison_result = SqlComparisonResult.IDENTICAL
                break
        return SqlStatementComparison(statement, matched_statement, comparison_result)
