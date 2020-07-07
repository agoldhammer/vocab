from click.testing import CliRunner
from vocab.cli import main


def startup():
    print("running startup")
    runner = CliRunner()
    _ = runner.invoke(main, ["practice", "--gui", "test1"])


if __name__ == "__main__":
    startup()
