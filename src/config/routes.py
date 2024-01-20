from fastapi import APIRouter

from src.auth.routes import router as auth_router
from src.domain.shared.tenant.route import router as tenant_router

router = APIRouter()

router.include_router(tenant_router, prefix="/tenant", tags=["tenant"])
router.include_router(auth_router, prefix="/auth",)
