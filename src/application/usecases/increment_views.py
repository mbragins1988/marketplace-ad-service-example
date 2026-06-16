from src.application.ports.uow import UnitOfWork
from src.application.ports.usecases import IncrementViewsPort


class IncrementViews(IncrementViewsPort):
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, ad_id: int) -> None:
        async with self._uow:
            await self._uow.ads.increment_views(ad_id)
            await self._uow.commit()
