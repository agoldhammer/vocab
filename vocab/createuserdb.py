# import sys

# from werkzeug.security import generate_password_hash

# from vocab.fileman import db_connect


# def create_db(name):
#     """create user db for use by lexy  app
#     fields: username text, pwhash text, is_active bool

#     Args:
#         name (str): name of db to create, w/o extension
#     """
#     conn = db_connect(name, create=True)
#     curs = conn.cursor()
#     curs.execute(
#         """CREATE TABLE users
#         (username text, pwhash text, is_active int)"""
#     )
#     dummy_hash = generate_password_hash("dummy")
#     curs.execute(
#         f"INSERT INTO users VALUES ('test', '{dummy_hash}', 1)"
#     )
#     conn.commit()
#     conn.close()


# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Must specify db name")
#         sys.exit(1)
#     else:
#         create_db(sys.argv[1])
