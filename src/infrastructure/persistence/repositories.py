from typing import List

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.repositories import AdRepository
from src.domain.entities import Ad, AdStatus
from src.infrastructure.persistence.models import AdModel


class SQLAlchemyAdRepository(AdRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        user_id: int,
        title: str,
        description: str,
        price: int,
        category: str,
        city: str,
    ) -> Ad:
        model = AdModel(
            user_id=user_id,
            title=title,
            description=description,
            price=price,
            category=category,
            city=city,
            status=AdStatus.ACTIVE.value,
        )
        self._session.add(model)
        await self._session.flush()
        return _to_entity(model)

    async def get_by_id(self, ad_id: int) -> Ad | None:
        model = await self._session.get(AdModel, ad_id)
        if model is None:
            return None
        return _to_entity(model)

    async def list(
        self,
        user_id: int | None,
        limit: int,
        offset: int,
    ) -> tuple[List[Ad], int]:
        query = select(AdModel)
        if user_id is not None:
            query = query.where(AdModel.user_id == user_id)
        query = query.where(AdModel.status == AdStatus.ACTIVE.value)

        total_query = select(func.count()).select_from(AdModel).where(AdModel.status == AdStatus.ACTIVE.value)
        if user_id is not None:
            total_query = total_query.where(AdModel.user_id == user_id)

        total = await self._session.scalar(total_query)

        query = query.order_by(AdModel.created_at.desc()).offset(offset).limit(limit)
        result = await self._session.execute(query)
        models = result.scalars().all()

        return [_to_entity(m) for m in models], total or 0

    async def save(self, ad: Ad) -> None:
        await self._session.execute(
            update(AdModel)
            .where(AdModel.id == ad.id)
            .values(
                title=ad.title,
                description=ad.description,
                price=ad.price,
                category=ad.category,
                city=ad.city,
                status=ad.status.value,
                updated_at=ad.updated_at,
            )
        )


def _to_entity(model: AdModel) -> Ad:
    return Ad(
        id=model.id,
        user_id=model.user_id,
        title=model.title,
        description=model.description,
        price=model.price,
        category=model.category,
        city=model.city,
        status=AdStatus(model.status),
        views=model.views,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
