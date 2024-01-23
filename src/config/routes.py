from fastapi import APIRouter

from src.auth.routes import router as auth_router
from src.domain.shared.company.route import router as company_router
from src.domain.shared.tenant.route import router as tenant_router
from src.domain.shared.users.routes import router as user_router

router = APIRouter()

router.include_router(tenant_router, prefix="/tenants", tags=["tenant"])
router.include_router(auth_router, prefix="/auth",)
router.include_router(user_router, prefix="/users", tags=["user"])
router.include_router(company_router, prefix="/companies", tags=["company"])
