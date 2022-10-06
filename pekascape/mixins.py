from typing import List


class ItemsAccessMixin:
    items: list

    @property
    def items_by_name(self) -> List[str]:
        return [item.name for item in self.items]

    def get_item_by_name(self, item_name: str):
        return [item for item in self.items if item.name == item_name][0]
