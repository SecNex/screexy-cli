from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.prompt import Prompt, Confirm

from config import Configuration, Items, Media

import os

console = Console()

flags = {
    "de": "🇩🇪",
    "en": "🇬🇧"
}

class CLI:
    def __init__(self, config: Configuration) -> None:
        self.config = config
        self.check()
        self.prepare()

    def check(self) -> None:
        files = ["items_config_file", "media_config_file"]
        folders = ["media_directory"]
        for file in files:
            if not os.path.exists(self.config.get("kiosk", file)):
                console.print(f"❌ Configuration file not found: {file}", style="red")
                exit(1)
        for folder in folders:
            if not os.path.exists(self.config.get("kiosk", folder)):
                console.print(f"❌ Directory not found: {folder}", style="red")
                exit(1)
    
    def prepare(self) -> None:
        __media_directory = self.config.get("kiosk", "media_directory")
        __media_directories = ["images", "videos", "thumbnails"]
        count = 0
        for directory in __media_directories:
            if not os.path.exists(os.path.join(__media_directory, directory)):
                try:
                    os.makedirs(os.path.join(__media_directory, directory))
                    count += 1
                except Exception as e:
                    console.print(f"❌ Error creating directory: {directory}", style="red")
                    exit(1)
        if count > 0:
            console.print(f"✅ {count} directories created.", style="green")
            print()

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

    def add_media(self, title: str, file: str, type: str, description: str = None) -> None:
        __path = self.config.get("kiosk", "media_config_file")
        __media_directory = self.config.get("kiosk", "media_directory")
        media = Media(__path, __media_directory)
        console.print(media.add(title, file, type, description))
        print()
        console.print("✅ Media added successfully.", style="green")
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
    
    def remove_media(self, id: int) -> None:
        __path = self.config.get("kiosk", "media_config_file")
        __media_directory = self.config.get("kiosk", "media_directory")
        media = Media(__path, __media_directory)
        media.remove(id)
        console.print("✅ Media removed successfully.", style="green")

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

    def list_media(self) -> None:
        __path = self.config.get("kiosk", "media_config_file")
        __media_directory = self.config.get("kiosk", "media_directory")
        media = Media(__path, __media_directory)
        console.print(media.media)
        table = Table(title="🖼️ Media")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("File", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Description", style="red")

        for idx, item in enumerate(media.get(), 1):
            if "description" not in item:
                item["description"] = ""
            table.add_row(str(idx), item["title"], item["link"], item["type"], item["description"])

        console.print(table)
        print()
    
    def edit_item(self, id: int, language: str, title: str, link: str, type: str) -> None:
        __path = self.config.get("kiosk", "items_config_file")
        items = Items(__path)
        items.edit(id, language, title, link, type)
        console.print(f"✅ Item edited: {id}")

    def edit_media(self, id: int, title: str, file: str, type: str, description: str = None) -> None:
        __path = self.config.get("kiosk", "media_config_file")
        __media_directory = self.config.get("kiosk", "media_directory")
        media = Media(__path, __media_directory)
        media.edit(id, title, file, type, description)
        console.print(f"✅ Media edited: {id}")
        
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

    def clear_media(self) -> None:
        __path = self.config.get("kiosk", "media_config_file")
        __media_directory = self.config.get("kiosk", "media_directory")
        media = Media(__path, __media_directory)
        media.clear()
        console.print("✅ All media removed.")

    def thumbnail(self, source: str = None, target: str = None) -> None:
        __source = source
        __target = target
        if source is None:
            __source = f"{self.config.get('kiosk', 'media_directory')}/videos"
        if target is None:
            __target = f"{self.config.get('kiosk', 'media_directory')}/thumbnails"
        from tools.thumbnail import Thumbnail
        thumbnail = Thumbnail(__source, __target)
        thumbnail.generate()
        console.print("✅ Thumbnails generated successfully.", style="green")

    def wizard(self) -> None:
        __items_path = self.config.get("kiosk", "items_config_file")
        __media_path = self.config.get("kiosk", "media_config_file")

        while True:
            menu = Tree("🧙 Kiosk Wizard")
            menu.add("[1] Add a new tile")
            menu.add("[2] Remove a tile")
            menu.add("[3] List all tiles")
            menu.add("[4] Edit a tile")
            menu.add("[5] Clear all tiles")
            menu.add("[6] Add a new media")
            menu.add("[7] Remove a media")
            menu.add("[8] List all media")
            menu.add("[9] Edit a media")
            menu.add("[10] Clear all media")
            menu.add("[11] Exit")

            console.print(menu)
            print()

            menu_choice = int(Prompt.ask("🧙 Choose an option: ", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]))
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
                    console.print("🗑  Clear all tiles\n")
                    confirm = Confirm.ask("🚀 Do you want to remove all items?")
                    if confirm:
                        print()
                        self.clear()
                    else:
                        console.print("🚧 Aborted.", style="bold red")

                case 6:
                    console.print("🖼️ Add a new media\n")
                    title = Prompt.ask("📝 Enter the title")
                    file = Prompt.ask("📁 Enter the path")
                    type = Prompt.ask("🔖 Choose the type", choices=["image", "video"], default="image")
                    description = Prompt.ask("📝 Enter a description", default=None)

                    confirm = Confirm.ask("🚀 Do you want to add this media?")
                    if confirm:
                        print()
                        self.add_media(title, file, type, description)
                    else:
                        console.print("🚧 Aborted.", style="bold red")

                case 7:
                    console.print("🗑  Remove a media\n")
                    id = int(Prompt.ask("🆔 Enter the ID"))
                    confirm = Confirm.ask("🚀 Do you want to remove this media?")
                    if confirm:
                        print()
                        self.remove_media(id)
                    else:
                        console.print("🚧 Aborted.", style="bold red")
                
                case 8:
                    self.list_media()

                case 9:
                    console.print("📝 Edit a media\n")
                    id = int(Prompt.ask("🆔 Enter the ID: "))
                    title = Prompt.ask("📝 Enter the title")   
                    file = Prompt.ask("📁 Enter the path")
                    type = Prompt.ask("🔖 Choose the type", choices=["image", "video"], default="image")
                    description = Prompt.ask("📝 Enter a description", default=None)

                    confirm = Confirm.ask("🚀 Do you want to edit this media?")
                    if confirm:
                        print()
                        self.edit_media(id, title, file, type, description)
                    else:
                        console.print("🚧 Aborted.", style="bold red")

                case 10:
                    console.print("🗑  Clear all media\n")
                    confirm = Confirm.ask("🚀 Do you want to remove all media?")
                    if confirm:
                        print()
                        self.clear_media()
                    else:
                        console.print("🚧 Aborted.", style="bold red")
                
                case _:
                    console.print("👋 Goodbye!", style="bold")
                    print()
                    exit(0)