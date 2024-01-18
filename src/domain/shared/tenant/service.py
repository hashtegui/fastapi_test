from typing import List, Sequence

from fastapi import HTTPException
from sqlalchemy import MetaData, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.automap import AutomapBase
from sqlalchemy.schema import CreateSchema, CreateTable

from src.config.database.connection import sessionmanager

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

    # criando schema

    # await create_schema(tenant_db.schema_name)

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
        await migrate_tables_for_schema(schema_name)
        if not has_schema:
            # await con.run_sync(sessionmanager._engine.dialect)
            schema = CreateSchema(schema_name)

            # await con.execute(schema)
            # await con.commit()


async def migrate_tables_for_schema(schema_name: str):
    if sessionmanager._engine is None:
        raise
    engine = sessionmanager._engine
    async with sessionmanager._engine.begin() as con:
        table_list = await con.run_sync(engine.dialect.get_table_names)

        metadata = MetaData()
        await con.run_sync(metadata.reflect,)

        excluded_tables = ['migrations', 'alembic_version']

        async with sessionmanager.session() as session:
            tenants = await get_all_tenants(session)

        async with engine.execution_options(schema_translate_map={None: schema_name}).connect() as con:
            for tenant in tenants:
                if tenant.schema_name == schema_name:
                    for table in metadata.sorted_tables:
                        if table.name in excluded_tables:
                            continue

                        await con.execute(CreateTable(table))
                        await con.commit()
