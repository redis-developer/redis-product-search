import subprocess


def load_data():
    subprocess.run(["python", "-m", "productsearch.db.load"], check=True)


def start_app():
    # load data
    subprocess.run(["python", "-m", "productsearch.db.load"], check=True)
    # start app
    subprocess.run(["python", "-m", "productsearch.main"], check=True)


def format():
    subprocess.run(
        ["isort", "./productsearch", "./tests/", "--profile", "black"], check=True
    )
    subprocess.run(["black", "./productsearch"], check=True)


def check_format():
    subprocess.run(["black", "--check", "./productsearch"], check=True)


def sort_imports():
    subprocess.run(
        ["isort", "./productsearch", "./tests/", "--profile", "black"], check=True
    )


def check_sort_imports():
    subprocess.run(
        ["isort", "./productsearch", "--check-only", "--profile", "black"], check=True
    )


def check_lint():
    subprocess.run(["pylint", "--rcfile=.pylintrc", "./productsearch"], check=True)


def mypy():
    subprocess.run(["python", "-m", "mypy", "./productsearch"], check=True)


def test():
    subprocess.run(
        ["python", "-m", "pytest", "productsearch", "--log-level=CRITICAL"], check=True
    )


def test_cov():
    subprocess.run(
        [
            "python",
            "-m",
            "pytest",
            "-vv",
            "--cov=./productsearch",
            "--cov-report=xml",
            "--log-level=CRITICAL",
        ],
        check=True,
    )


def cov():
    subprocess.run(["coverage", "html"], check=True)
    print("If data was present, coverage report is in ./htmlcov/index.html")
