from fastapi import APIRouter, Depends, HTTPException

from src.auth.service import get_current_user
from src.config.database.connection import SessionDB
from src.domain.shared.tenant.schemas import TenantIn, TenantOut

from . import service

router = APIRouter()


@router.post("/", response_model=TenantOut)
async def create_tenant(tenant_in: TenantIn, session: SessionDB):
    tenant = await service.create_tenant(tenant_in, session)

    return tenant


@router.get("/", dependencies=[Depends(get_current_user)])
async def get_tenants(session: SessionDB,):
    tenants = await service.get_all_tenants(session)

    return tenants


@router.get("/{tenant_id}")
async def get_tenant_by_id(tenant_id: int, session: SessionDB):
    tenant = await service.get_tenant_by_id(tenant_id, session)

    if tenant is None:
        raise HTTPException(404, 'Tenant not found')

    return tenant


@router.post("/{tenant_id}/create_schema",
             response_model=None,
             status_code=204)
async def create_schema(tenant_id: int, session: SessionDB):
    tenant = await service.get_tenant_by_id(tenant_id, session)
    if tenant is None:
        raise HTTPException(404, 'Tenant not found')
    await service.create_schema(tenant.schema_name)
    return None


@router.post("/{tenant_id}/migrate",)
async def migrate(tenant_id: int, session: SessionDB):
    tentant = await service.get_tenant_by_id(tenant_id, session)

    if tentant is None:
        raise HTTPException(404, 'Tenant not found')

    await service.migrate_tables_for_schema(tentant.schema_name)

    return None
