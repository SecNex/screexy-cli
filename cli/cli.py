from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.prompt import Prompt, Confirm

from config import Configuration, Items

console = Console()

flags = {
    "de": "🇩🇪",
    "en": "🇬🇧"
}

class CLI:
    def __init__(self, config: Configuration) -> None:
        self.config = config
    
    def list_section(self) -> None:
        for section in self.config.list_sections():
            console.print(f"💎 {section}")
            for key, value in self.config.get_section(section).items():
                console.print(f"🛠️ {key}: {value}")
            print()

    def list_config(self, section: str) -> None:
        __section = self.config.get_section(section)
        console.print(f"💎 {section}")
        for key, value in __section.items():
            console.print(f"🛠️ {key}: {value}")

    def add_item(self, language: str, title: str, link: str, type: str, position: int = 0) -> None:
        __language = [language]
        __path = self.config.get("kiosk", "items_config_file")
        if language == "all":
            __language = ["de", "en"]
        __result = []
        __de_length = len(Items(__path).get("de"))
        __en_length = len(Items(__path).get("en"))
        if position > 1:
            if position > __de_length or position > __en_length:
                console.print("❌ Position is out of range.", style="red")
                return
        for lang in __language:
            items = Items(__path)
            __add_result = items.add(lang, title, link, type, position)
            if __add_result is not None:
                __result.append(__add_result)
            else:
                return
        if len(__result) == 0:
            console.print("❌ No items added.", style="red")
            return
        table = Table()
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Link", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Language", style="blue")

        for idx, item in enumerate(__result, 1):
            table.add_row(str(idx), item["title"], item["link"], item["type"], item["language"])
        
        console.print(table)
        print()

    def remove_item(self, language: str, id: int, output: bool = True) -> bool:
        __language = [language]
        __path = self.config.get("kiosk", "items_config_file")
        if language == "all":
            __language = ["de", "en"]
        for lang in __language:
            items = Items(__path)
            try:
                items.remove(lang, id)
            except Exception as e:
                return False
            if output:
                console.print(f"✅ Item removed: {id}")
        return True

    def list_items(self) -> None:
        __path = self.config.get("kiosk", "items_config_file")
        items = Items(__path)
        for lang in ["de", "en"]:
            table = Table(title=f"{flags.get(lang)} {lang.upper()}: Tiles")
            table.add_column("ID", justify="right", style="cyan")
            table.add_column("Title", style="magenta")
            table.add_column("Link", style="green")
            table.add_column("Type", style="yellow")

            for idx, item in enumerate(items.get(lang), 1):
                table.add_row(str(idx), item["title"], item["link"], item["type"])

            console.print(table)
            print()
    
    def edit_item(self, id: int, language: str, title: str, link: str, type: str) -> None:
        __path = self.config.get("kiosk", "items_config_file")
        items = Items(__path)
        items.edit(id, language, title, link, type)
        console.print(f"✅ Item edited: {id}")
        
    def bulk_remove(self, ids: list) -> None:
        __path = self.config.get("kiosk", "items_config_file")
        items = Items(__path)
        for lang in ["de", "en"]:
            for id in ids:
                items.remove(lang, id)
        console.print("✅ Items removed successfully.", style="green")

    def clear(self) -> None:
        __path = self.config.get("kiosk", "items_config_file")
        items = Items(__path)
        items.clear()
        console.print("✅ All items removed.")

    def wizard(self) -> None:
        __items_path = self.config.get("kiosk", "items_config_file")
        __media_path = self.config.get("kiosk", "media_config_file")

        while True:
            menu = Tree("🧙 Kiosk Wizard")
            menu.add("[1] Add a new tile")
            menu.add("[2] Remove a tile")
            menu.add("[3] List all tiles")
            menu.add("[4] Edit a tile")
            menu.add("[5] Bulk remove tiles")
            menu.add("[6] Clear all tiles")
            menu.add("[7] Exit")

            console.print(menu)
            print()

            menu_choice = int(Prompt.ask("🧙 Choose an option: ", choices=["1", "2", "3", "4", "5", "6", "7"]))
            print()

            match menu_choice:
                case 1:
                    console.print("🧱 Add a new tile\n")
                    console.print("If you want to add a tile in both languages, please run this command twice or use the choice 'all' for the language.\n", style="italic dim")
                    language = Prompt.ask("🌐 Choose a language", choices=["de", "en", "all"], default="all")
                    title = Prompt.ask("📝 Enter the title")
                    link = Prompt.ask("🔗 Enter the link")
                    type = Prompt.ask("🔖 Choose the type", choices=["website", "external", "pdf"], default="website")
                    position = int(Prompt.ask("🔢 Enter the position", default=0))

                    confirm = Confirm.ask("🚀 Do you want to add this item?")
                    if confirm:
                        print()
                        self.add_item(language, title, link, type, position)
                    else:
                        console.print("🚧 Aborted.", style="bold red")
                case 2:
                    console.print("🗑  Remove a tile\n")
                    language = Prompt.ask("🌐 Choose a language", choices=["de", "en", "all"], default="all")
                    id = int(Prompt.ask("🆔 Enter the ID"))
                    confirm = Confirm.ask("🚀 Do you want to remove this item?")
                    if confirm:
                        print()
                        if self.remove_item(language, id, False):
                            console.print(f"✅ Item removed: {id}")
                    else:
                        console.print("🚧 Aborted.", style="bold red")

                case 3:
                    self.list_items()
                
                case 4:
                    console.print("📝 Edit a tile\n")
                    id = int(Prompt.ask("🆔 Enter the ID: "))
                    language = Prompt.ask("🌐 Choose a language: ", choices=["de", "en"])
                    title = Prompt.ask("📝 Enter the title")   
                    link = Prompt.ask("🔗 Enter the link")
                    type = Prompt.ask("🔖 Choose the type", choices=["website", "external", "pdf"], default="website")

                    confirm = Confirm.ask("🚀 Do you want to edit this item?")
                    if confirm:
                        print()
                        self.edit_item(id, language, title, link, type)
                    else:
                        console.print("🚧 Aborted.", style="bold red")
                case 5:
                    console.print("🗑  Bulk remove tiles\n")
                    console.print("ℹ️ If you want to remove multiple items, please provide the IDs separated by a comma.\n", style="italic dim")
                    ids = Prompt.ask("🆔 Enter the IDs to remove").replace(" ", "")
                    confirm = Confirm.ask("🚀 Do you want to remove these items?")
                    if confirm:
                        print()
                        ids_list = [int(id) for id in ids.split(",")]
                        self.bulk_remove(ids_list)
                    else:
                        console.print("🚧 Aborted.", style="bold red")
                case _:
                    console.print("🚀 Goodbye!")
                    break