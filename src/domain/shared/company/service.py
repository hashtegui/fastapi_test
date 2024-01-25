from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.shared.company.model import Company
from src.domain.shared.company.schemas import CompanyFilter, CompanyIn


async def create_company(company_in: CompanyIn, session: AsyncSession):
    company = Company(**company_in.model_dump())
    session.add(company)
    await session.commit()
    await session.refresh(company)
    return company


async def get_company_by_id(company_id: int, session: AsyncSession):
    result = await session.scalars(select(Company).where(Company.id == company_id))
    return result.first()


async def get_all_companies(
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0,
        filters: Optional[CompanyFilter] = None):
    statement = select(Company).limit(limit).offset(offset)
    if filters:

        if filters.id:
            statement = statement.where(Company.id == filters.id)

        if filters.name:
            statement = statement.where(Company.name.like(f'%{filters.name}%'))

        if filters.tenant_id:
            statement = statement.where(Company.tenant_id == filters.tenant_id)

    result = await session.scalars(statement)
    return result.all()
