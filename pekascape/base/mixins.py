from pekascape.item.base import ItemBase


class ItemsAccessMixin:
    items: list[ItemBase]

    @property
    def items_by_name(self) -> list[str]:
        return [item.name for item in self.items]

    def get_item_by_name(self, item_name: str) -> ItemBase:
        return [item for item in self.items if item.name == item_name][0]
