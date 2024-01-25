from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.config.database.connection import SessionDB
from src.domain.shared.company import service
from src.domain.shared.company.schemas import (CompanyFilter, CompanyIn,
                                               CompanyOut)

router = APIRouter()


@router.post("/", status_code=201, response_model=CompanyOut)
async def create_company(company_in: CompanyIn, session: SessionDB):
    company = await service.create_company(company_in, session)
    return company


@router.get("/", response_model=List[CompanyOut])
async def get_all_companies(
        session: SessionDB,
        filters: Annotated[CompanyFilter, Depends()]):
    companies = await service.get_all_companies(session, filters=filters)

    return companies
