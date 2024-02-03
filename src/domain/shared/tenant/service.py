
import alembic
from alembic.migration import MigrationContext
from fastapi import HTTPException
from sqlalchemy import Connection, MetaData, Table, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.automap import AutomapBase
from sqlalchemy.schema import (AddConstraint, CreateColumn, CreateSchema,
                               CreateTable)

from src.config.database.connection import sessionmanager
from src.domain.models import Base
from src.domain.shared import SharedBase

from .model import Tenant
from .schemas import TenantIn


class AutoBase(AutomapBase):
    metadata = MetaData(schema='public')
    pass


async def get_tenant_by_name(tenant_name: str, session: AsyncSession):
    result = await session.scalars(select(Tenant)
                                   .where(Tenant.name == tenant_name))
    return result.first()


async def get_tenant_by_id(tenant_id: int, session: AsyncSession):
    result = await session.scalars(select(Tenant)
                                   .where(Tenant.id == tenant_id))
    return result.first()


async def create_tenant(tenant: TenantIn, session: AsyncSession):

    if tenant.schema_name == 'public':  # validate if tenant is public
        raise HTTPException(400, 'Cannot create public tenant')

    tenant_db = Tenant(**tenant.model_dump())

    session.add(tenant_db)

    await session.commit()
    await session.refresh(tenant_db)

    return tenant_db


async def get_all_tenants(session: AsyncSession):
    result = await session.scalars(select(Tenant))
    return result.all()


async def create_schema(schema_name: str):
    if sessionmanager._engine is None:
        raise
    engine = sessionmanager._engine
    async with sessionmanager._engine.begin() as con:
        has_schema = await con.run_sync(engine.dialect.has_schema, schema_name)
        if not has_schema:
            # await con.run_sync(sessionmanager._engine.dialect)
            schema = CreateSchema(schema_name)

            await con.execute(schema)
            await con.commit()
        await migrate_tables_for_schema(schema_name)


async def create_shared_tables():
    # criar as tabelas publicas
    orm_tables = SharedBase.metadata.sorted_tables

    if sessionmanager._engine is None:
        raise
    engine = sessionmanager._engine

    async with engine.execution_options(schema_translate_map={'shared': 'shared'}).connect() as con:
        for table in orm_tables:
            has_table = await con.run_sync(engine.dialect.has_table, table.name, 'shared')
            if has_table:
                print(f"""Table {table.name} already exists in shared""")
                await verify_table_columns(table, 'shared')
                continue
            await con.execute(CreateTable(table))
            await con.commit()


async def create_public_tables():
    # criar as tabelas publicas
    orm_tables = Base.metadata.sorted_tables

    if sessionmanager._engine is None:
        raise
    engine = sessionmanager._engine

    async with engine.execution_options(schema_translate_map={'public': 'public'}).connect() as con:
        for table in orm_tables:
            has_table = await con.run_sync(engine.dialect.has_table, table.name, 'public')
            if has_table:
                print(f"""Table {table.name} already exists in public""")
                await verify_table_columns(table,)
                continue
            else:
                await con.execute(CreateTable(table))
                await con.commit()


async def verify_table_columns(table: Table, schema_name: str = 'public'):

    if sessionmanager._engine is None:
        raise
    engine = sessionmanager._engine

    async with engine.execution_options(schema_translate_map={None: schema_name}).connect() as con:

        column_list = await con.run_sync(engine.dialect.get_columns, table.name, schema_name)

        for column in table.columns:

            for col in column_list:
                if column.name == col['name']:

                    break
            else:
                print(f"""Column {column.name} not found in table {
                    table.name}""")

                create_column = CreateColumn(column)
                compiled = create_column.compile(dialect=engine.dialect)
                await con.execute(text(f"""ALTER TABLE {schema_name}.{table.name} ADD COLUMN {compiled.string}"""))
                for fk in column.foreign_keys:
                    await con.execute(AddConstraint(fk.constraint))
                await con.commit()


async def migrate_tables_for_schema(schema_name: str):
    if sessionmanager._engine is None:
        raise
    engine = sessionmanager._engine
    async with sessionmanager._engine.begin() as con:

        # table_list = await con.run_sync(engine.dialect.get_table_names)

        metadata = MetaData()
        new_meta = MetaData(schema=schema_name)
        await con.run_sync(metadata.reflect, )

        excluded_tables = ['migrations', 'alembic_version']

        orm_tables = Base.metadata.sorted_tables

        async with sessionmanager.session() as session:
            tenants = await get_all_tenants(session)

        async with engine.execution_options(schema_translate_map={'public': schema_name}).connect() as connection:
            for tenant in tenants:
                if tenant.schema_name == schema_name:
                    for table in orm_tables:
                        if table.name in excluded_tables:
                            continue
                        if await connection.run_sync(engine.dialect.has_table, table.name, schema_name):
                            print(f"""Table {table.name} already exists in {
                                  schema_name}""")
                            await verify_table_columns(table, schema_name)

                            continue

                        table_copy = table.to_metadata(new_meta)
                        await connection.execute(CreateTable(table_copy))
                        # print(CreateTable(table).compile(
                        #     connection.sync_connection))
                        await connection.commit()
