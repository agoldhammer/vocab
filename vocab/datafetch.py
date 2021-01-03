from typing import Tuple

from sqlalchemy import func, select, text

from vocab.fileman import get_vocab_engine
from vocab.tables import lexicon


def fetch_slugs(dbname: str, num_to_fetch: int = 25) -> Tuple[int, str, str, str]:
    """[fetch the vocab items from lexicon]

    Args:
        dbname (str): base name of vocabulary database
        num_to_fetch (int, optional): number of vocab items to fetch. Defaults to 25.

    Return:
        Tuple[id: int, src: str, target: str, supp: str]
    """
    qry_nitems = f"SELECT * FROM lexicon ORDER BY RANDOM() LIMIT {num_to_fetch}"
    s = text(qry_nitems)
    engine = get_vocab_engine(dbname)
    with engine.connect() as conn:
        result = conn.execute(s)
        rows = result.fetchall()
    return rows


def count_vocab(dbname: str) -> int:
    """return number of vocab items in lexicon of dbname

    Args:
        dbname (str): base name of vocab db

    Returns:
        int: number of vocab items in db
    """
    s = select([func.count()]).select_from(lexicon)
    engine = get_vocab_engine(dbname)
    with engine.connect() as conn:
        result = conn.execute(s)
        nrows = result.fetchone()[0]
    return nrows


if __name__ == "__main__":
    rows = fetch_slugs("sqagerman", 20)
    for row in rows:
        print(row)
    nrows = count_vocab("sqagerman")
    print(f"nrows: {nrows}")
