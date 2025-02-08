from django.db.migrations.operations.base import Operation

class MigrationOptimizer:
    def optimize(self, operations: list[Operation], app_label: str | None) -> list[Operation]: ...
    def optimize_inner(self, operations: list[Operation], app_label: str | None) -> list[Operation]: ...
