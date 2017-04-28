import logging

from playhouse.migrate import MySQLMigrator, migrate

from tracnghiem.database import database


def migrate_since_8e15421():
    logging.info("DB Migration for commit 8e15421")
    logging.info("List of actions: ")
    logging.info("* Remove column facebook_id from table account")
    logging.info("* Remove column session_lock from table exam")
    logging.info("")
    logging.info("Migrating db")

    migrate(
        migrator.drop_column("account", "facebook_id"),
        migrator.drop_column("exam", "session_lock_id")
    )
    logging.info("Migration done!")

def migrate_since_906aff3():
    logging.info("DB Migration for commit 906aff3")
    logging.info("List of actions: ")
    logging.info("* Add index for column exam.secret_key")
    logging.info("")
    logging.info("Migrating db")

    migrate(
        migrator.add_index("exam", ["secret_key"])
    )
    logging.info("Migration done!")

logging.basicConfig(format = "[%(asctime)s][%(funcName)s] %(message)s",
                    datefmt = "%Y-%m-%d %H:%M:%S",
                    level = logging.INFO)

migrator = MySQLMigrator(database)

logging.info("Opening database")
database.connect()

migrate_since_906aff3()
database.close()
