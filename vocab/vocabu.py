import docx

from vocab.fileman import (get_fqdocname,
                           db_connect,
                           backup_db,
                           db_exists)
from vocab.createdb import create_db


def get_doc(fname: str) -> docx.Document:
    """given a base file name, find the fully qualified
    filename and make Python readable with docx odule

    Args:
        fname (str): base file name, w/o ext or path

    Returns:
        docx.Document: python readable version of the docx file
    """
    fqname = get_fqdocname(fname)
    return docx.Document(fqname)


def get_vitems(doc):
    """return view items, which are lists of three strings,
       one for each part of the :-separated line in the vocab doc

    Args:
        doc ([docx.Document]): [description]

    Returns:
        [list[Str]]: [3-segment list of strings for each view items]
    """
    return [p.text.split(":") for p in doc.paragraphs]


def validate_vitem(vitem):
    """return status, vitem where status is t/f and vitem is of len 3 with blank
    string added to supp field if nec"""
    lvitem = len(vitem)
    if lvitem == 2:
        vitem.append("")
        return True, vitem
    elif lvitem == 3:
        return True, vitem
    else:
        return False, vitem


def store_data(data, dbname):
    """takes a list of 6-tuples representing vitems
    and stores in db dbname

    Args:
        data (List[6-tuples]): list of 6-tuples representing vitems
        dbname (Str): base dbname without ext or path

        data tuples: src, target, supp, lrd_from, Lrd_to, nseen
    """
    _, dbexists = db_exists(dbname)
    if dbexists:
        backup_db(dbname)  # if storing new data, backup db before continuing
        conn = db_connect(dbname)
    else:
        create_db(dbname)
        conn = db_connect(dbname)
    c = conn.cursor()
    c.executemany("INSERT INTO vocab VALUES (?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()


def execute(store, fname, dbname):
    """if store == True, store vitems from doc fname in db
    named dbname; else just display the vitems on the console

    Args:
        store (Bool): store in db if true, else dry run
        fname (Str): base name of docx vocab file, w/o ext
        dbname (Str): base name of db file, w/o ext
    """
    doc = get_doc(fname)
    vitems = get_vitems(doc)
    valid_vitems = []
    invalid_vitems = []
    for vitem in vitems:
        status, v = validate_vitem(vitem)
        print(status, v)
        if status:
            valid_vitems.append([v[0].strip(), v[1].strip(), v[2].strip(), 0, 0, 0])
        else:
            invalid_vitems.append(v)
    for vitem in valid_vitems:
        print(vitem)
    if store:
        store_data([tuple(vitem) for vitem in valid_vitems], dbname)
    for vitem in invalid_vitems:
        print(f"Bad vitem: {vitem}")
    print(f"Total vitems: {len(vitems)}")


if __name__ == "__main__":
    print("This file should only be called via cli")
