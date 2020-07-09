from click.testing import CliRunner
from vocab.cli import main
from pyperclip import copy


def startup():
    print("running startup")
    copy("testcli running")
    runner = CliRunner()
    _ = runner.invoke(main, ["practice", "--gui", "--all", "test1"])


if __name__ == "__main__":
    startup()
