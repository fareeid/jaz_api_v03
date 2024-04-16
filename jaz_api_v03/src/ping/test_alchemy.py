from typing import Any

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    insert,
)

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

print(user_table.c.name)
print(user_table.c.keys())


address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)

metadata_obj.create_all(engine)

stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
print(stmt)
compiled = stmt.compile()
compiled.params

with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()


def func() -> Any:
    print("func() in one.py")


print("top-level in one.py")

if __name__ == "__main__":
    print("one.py is being run directly")
    func()
