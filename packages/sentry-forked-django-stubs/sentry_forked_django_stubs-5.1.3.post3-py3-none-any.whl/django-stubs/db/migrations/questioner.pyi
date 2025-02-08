from typing import Any

from django.db.migrations.state import ModelState
from django.db.models.fields import Field

class MigrationQuestioner:
    defaults: dict[str, Any]
    specified_apps: set[str]
    dry_run: bool | None
    def __init__(
        self,
        defaults: dict[str, bool] | None = None,
        specified_apps: set[str] | None = None,
        dry_run: bool | None = None,
    ) -> None: ...
    def ask_initial(self, app_label: str) -> bool: ...
    def ask_not_null_addition(self, field_name: str, model_name: str) -> Any: ...
    def ask_not_null_alteration(self, field_name: Any, model_name: Any) -> Any: ...
    def ask_rename(self, model_name: str, old_name: str, new_name: str, field_instance: Field) -> bool: ...
    def ask_rename_model(self, old_model_state: ModelState, new_model_state: ModelState) -> bool: ...
    def ask_merge(self, app_label: str) -> bool: ...
    def ask_auto_now_add_addition(self, field_name: str, model_name: str) -> Any: ...

class InteractiveMigrationQuestioner(MigrationQuestioner): ...
class NonInteractiveMigrationQuestioner(MigrationQuestioner): ...
