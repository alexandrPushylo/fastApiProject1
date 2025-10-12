from sqlalchemy import select, insert


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        results = await self.session.execute(query)
        return results.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        results = await self.session.execute(query)
        return results.scalars().one_or_none()

    async def add(self, values):
        # stmt = insert(self.model).values(values)
        # result = await self.session.execute(stmt)
        new_model = self.model(**values)
        self.session.add(new_model)
        await self.session.flush()
        return new_model
