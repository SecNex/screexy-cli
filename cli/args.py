import argparse
from config import Configuration
from .cli import CLI

class Arguments:
    def __init__(self, cli: CLI) -> None:
        self.__cli = cli
        self.__parser = argparse.ArgumentParser(prog="screexy", description="Screexy CLI")
        self.__subparsers = self.__parser.add_subparsers(dest="command", title="commands", description="valid commands", help="additional help")
        self.__config = self.__subparsers.add_parser("config", help="manage the configuration file")
        self.__config.add_argument("-f", "--file", help="specify the configuration file", metavar="FILE", default="screexy.conf", dest="config_file")
        self.__config_group = self.__config.add_mutually_exclusive_group()
        self.__config_group.add_argument("-a", "--all", action="store_true", help="list all sections in the configuration file", dest="config_all")
        self.__config_group.add_argument("-s", "--section", help="specify a section to view", metavar="SECTION", dest="config_section")

        self.__kiosk = self.__subparsers.add_parser("kiosk", help="manage the kiosk items")
        self.__kiosk_sub = self.__kiosk.add_subparsers(dest="kiosk_command", title="kiosk commands", description="valid kiosk commands", help="additional help")
        self.__kiosk_add = self.__kiosk_sub.add_parser("add", help="list all kiosk items")
        self.__kiosk_add.add_argument("--title", help="specify the title of the item", metavar="TITLE", required=True, dest="kiosk_add_title", type=str)
        self.__kiosk_add.add_argument("--link", help="specify the link of the item", metavar="LINK", required=True, dest="kiosk_add_link", type=str)
        self.__kiosk_add.add_argument("--type", help="specify the type of the item", metavar="TYPE", required=True, dest="kiosk_add_type", type=str, choices=["website", "external", "pdf"])
        self.__kiosk_add.add_argument("--language", help="specify the language of the item", metavar="LANGUAGE", required=True, dest="kiosk_add_language", type=str, choices=["de", "en", "all"], default="all")
        self.__kiosk_add.add_argument("--position", help="specify the position of the item", metavar="POSITION", dest="kiosk_add_position", type=int, default=None)

        self.__kiosk_remove = self.__kiosk_sub.add_parser("remove", help="remove a kiosk item")
        self.__kiosk_remove.add_argument("--id", help="specify the id of the item", metavar="ID", required=True, dest="kiosk_rm_id", type=int)
        self.__kiosk_remove.add_argument("--language", help="specify the language of the item", metavar="LANGUAGE", required=True, dest="kiosk_rm_language", type=str, choices=["de", "en", "all"], default="all")

        self.__kiosk_list = self.__kiosk_sub.add_parser("list", help="list all kiosk items")

        self.__kiosk_edit = self.__kiosk_sub.add_parser("edit", help="edit a kiosk item")
        self.__kiosk_edit.add_argument("--id", help="specify the id of the item", metavar="ID", required=True, dest="kiosk_edit_id", type=int)
        self.__kiosk_edit.add_argument("--language", help="specify the language of the item", metavar="LANGUAGE", required=True, dest="kiosk_edit_language", type=str, choices=["de", "en", "all"])
        self.__kiosk_edit.add_argument("--title", help="specify the title of the item", metavar="TITLE", dest="kiosk_edit_title", type=str, default=None)
        self.__kiosk_edit.add_argument("--link", help="specify the link of the item", metavar="LINK", dest="kiosk_edit_link", type=str, default=None)
        self.__kiosk_edit.add_argument("--type", help="specify the type of the item", metavar="TYPE", dest="kiosk_edit_type", type=str, choices=["website", "external", "pdf"], default=None)

        self.__kiosk_bulk_remove = self.__kiosk_sub.add_parser("bulk-remove", help="remove all kiosk items")
        self.__kiosk_bulk_remove.add_argument("--ids", help="specify the ids of the items to remove", metavar="IDS", required=True, dest="kiosk_bulk_rm_ids", type=int, nargs="+")

        self.__kiosk_wizard = self.__kiosk_sub.add_parser("wizard", help="run the kiosk wizard")
        self.__kiosk_clear = self.__kiosk_sub.add_parser("clear", help="clear all kiosk items")

        self.__tools = self.__subparsers.add_parser("tools", help="manage the tools")
        self.__tools_sub = self.__tools.add_subparsers(dest="tools_command", title="tools commands", description="valid tools commands", help="additional help")
        self.__tools_thumbnail = self.__tools_sub.add_parser("thumbnail", help="generate thumbnails for videos")
        self.__tools_thumbnail.add_argument("--source", help="specify the path to the videos", metavar="VIDEO_PATH", dest="tools_thumbnail_video_path", type=str, default=None)
        self.__tools_thumbnail.add_argument("--target", help="specify the path to the media", metavar="MEDIA_PATH", dest="tools_thumbnail_media_path", type=str, default=None)

    def __parse(self) -> argparse.Namespace:
        return self.__parser.parse_args()

    def run(self) -> None:
        args = self.__parse()
        if args.command == "config":
            if args.config_all:
                self.__cli.list_section()
                return
            if args.config_section:
                self.__cli.list_config(args.config_section)
                return
            if args.config_section:
                print(f"Viewing section: {args.config_section}")
            else:
                print("No arguments provided.")
        if args.command == "kiosk":
            if args.kiosk_command == "add":
                self.__cli.add_item(args.kiosk_add_language, args.kiosk_add_title, args.kiosk_add_link, args.kiosk_add_type, args.kiosk_add_position)
                return
            if args.kiosk_command == "remove":
                self.__cli.remove_item(args.kiosk_rm_language, args.kiosk_rm_id)
                return
            if args.kiosk_command == "list":
                self.__cli.list_items()
                return
            if args.kiosk_command == "edit":
                self.__cli.edit_item(args.kiosk_edit_id, args.kiosk_edit_language, args.kiosk_edit_title, args.kiosk_edit_link, args.kiosk_edit_type)
                return
            if args.kiosk_command == "bulk-remove":
                self.__cli.bulk_remove(args.kiosk_bulk_rm_ids)
                return
            if args.kiosk_command == "wizard":
                self.__cli.wizard()
                return
            if args.kiosk_command == "clear":
                self.__cli.clear()
                return
            print("No arguments provided.")
        if args.command == "tools":
            if args.tools_command == "thumbnail":
                self.__cli.thumbnail(args.tools_thumbnail_video_path, args.tools_thumbnail_media_path)
                return
            print("No arguments provided.")