import docx

from vocab.fileman import get_fqdocname, db_connect


def get_doc(fname):
    fqname = get_fqdocname(fname)
    return docx.Document(fqname)


def get_vitems(doc):
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
    conn = db_connect(dbname)
    c = conn.cursor()
    c.executemany("INSERT INTO vocab VALUES (?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()


def execute(store, fname, dbname):
    # FIXME
    doc = get_doc(fname)
    vitems = get_vitems(doc)
    valid_vitems = []
    invalid_vitems = []
    for vitem in vitems:
        status, v = validate_vitem(vitem)
        print(status, v)
        if status:
            valid_vitems.append([v[0].strip(), v[1].strip(), v[2].strip(), 0, 0])
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
    execute()
