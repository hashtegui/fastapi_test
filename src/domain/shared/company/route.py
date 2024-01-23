from fastapi import APIRouter

from src.config.database.connection import SessionDB
from src.domain.shared.company import service
from src.domain.shared.company.schemas import CompanyIn

router = APIRouter()


@router.post("/")
async def create_company(company_in: CompanyIn, session: SessionDB):
    company = await service.create_company(company_in, session)
    return company


@router.get("/")
async def get_all_companies(session: SessionDB):
    companies = await service.get_all_companies(session)
    return companies
