from fastapi import APIRouter

from src.domain.shared.tenant.route import router as tenant_router

router = APIRouter()

router.include_router(tenant_router, prefix="/tenant", tags=["tenant"])
