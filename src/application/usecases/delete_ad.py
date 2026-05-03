from src.application.exceptions import AdNotFoundError, ForbiddenError
from src.application.ports.uow import UnitOfWork
from src.application.ports.usecases import DeleteAdPort
from src.domain.entities import AdStatus


class DeleteAd(DeleteAdPort):
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(
        self,
        ad_id: int,
        user_id: int,
    ) -> None:
        async with self._uow:
            # 1. Получаем объявление
            ad = await self._uow.ads.get_by_id(ad_id)
            if ad is None or ad.status == AdStatus.ARCHIVED:
                raise AdNotFoundError

            # 2. Проверяем права (только владелец)
            if ad.user_id != user_id:
                raise ForbiddenError

            # 3. Архивируем (soft delete)
            ad.archive()

            # 4. Сохраняем
            await self._uow.ads.save(ad)

            # 5. Записываем событие в outbox
            await self._uow.outbox.add(
                event_type="ad.deleted",
                payload={"ad_id": ad.id},
            )

            # 6. Фиксируем транзакцию
            await self._uow.commit()
