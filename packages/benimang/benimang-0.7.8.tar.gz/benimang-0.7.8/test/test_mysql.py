import os
from typing import cast

import pytest
import pytest_asyncio

from beni import bcrypto
from beni.bsql import BModel, Db, MysqlDb

dbInfo = 'vjMwuuVArXJpEjGH6UPzZHwxgzA8AMTWCeEMeA/VoIzNwWwbmcQ3bwyYbVuCYMr0pLEO7j1D7YbOrYFERIWXAwu0FUsosFEINZRPCos666Qo1eOuJ48c07oUxUOQIt9HxwHCXEcmj8HCWzkFG9xvH5y45luZejIPVm4uLIdvw2okVhYyKIXOzYcLyucfj/6lYw=='
DB = cast(Db, MysqlDb(**bcrypto.decryptJson(dbInfo, os.environ['XX_BENI'])))


@pytest_asyncio.fixture(scope='session', autouse=True)  # type: ignore
async def sessionSqlite():
    await initDb()
    yield


class Student(BModel):
    id: int = 0
    name: str = ''
    age: int = 0


async def initDb():
    async with DB.getCursor() as cursor:
        await cursor.execute(f'DROP TABLE IF EXISTS `{Student.tableName()}`')
        await cursor.execute(f'''
            CREATE TABLE `{Student.tableName()}`  (
                `id` int NOT NULL AUTO_INCREMENT,
                `name` varchar(255) NULL,
                `age` int NULL,
                PRIMARY KEY (`id`)
            );
        ''')


@pytest.mark.order()
@pytest.mark.asyncio(scope='session')
async def test_addOne():
    async with DB.getCursor() as cursor:
        await cursor.addOne(Student(name='Tom', age=20))
        await cursor.addOne(Student(name='Jerry', age=16))


@pytest.mark.order()
@pytest.mark.asyncio(scope='session')
async def test_saveOne():
    async with DB.getCursor() as cursor:
        student = Student(id=1, name='Tom', age=21)
        await cursor.saveOne(student)


@pytest.mark.order()
@pytest.mark.asyncio(scope='session')
async def test_saveList():
    async with DB.getCursor() as cursor:
        studentList = [
            Student(id=1, name='Tom', age=22),
            Student(id=2, name='Jerry', age=17),
        ]
        await cursor.saveList(studentList)


@pytest.mark.order()
@pytest.mark.asyncio(scope='session')
async def test_getTupleOne():
    async with DB.getCursor() as cursor:
        result = await cursor.getTupleOne(f'SELECT * FROM {Student.tableName()} WHERE `id` = %s', 1)
        assert result and result == (1, 'Tom', 22)


@pytest.mark.order()
@pytest.mark.asyncio(scope='session')
async def test_getDictOne():
    async with DB.getCursor() as cursor:
        result = await cursor.getDictOne(f'SELECT * FROM {Student.tableName()} WHERE `id` = %s', 1)
        assert result and result == {'id': 1, 'name': 'Tom', 'age': 22}


@pytest.mark.order()
@pytest.mark.asyncio(scope='session')
async def test_getOne():
    async with DB.getCursor() as cursor:
        result = await cursor.getOne(Student, f'SELECT * FROM {Student.tableName()} WHERE `id` = %s', 1)
        assert result and result.id == 1 and result.name == 'Tom' and result.age == 22


@pytest.mark.order()
@pytest.mark.asyncio(scope='session')
async def test_getTupleList():
    async with DB.getCursor() as cursor:
        resultList = await cursor.getTupleList(f'SELECT * FROM {Student.tableName()}')
        assert len(resultList) == 2 and [x[1] for x in resultList] == ['Tom', 'Jerry']


@pytest.mark.order()
@pytest.mark.asyncio(scope='session')
async def test_getDictList():
    async with DB.getCursor() as cursor:
        resultList = await cursor.getDictList(f'SELECT * FROM {Student.tableName()}')
        assert len(resultList) == 2 and [x['name'] for x in resultList] == ['Tom', 'Jerry']


@pytest.mark.order()
@pytest.mark.asyncio(scope='session')
async def test_getList():
    async with DB.getCursor() as cursor:
        resultList = await cursor.getList(Student, f'SELECT * FROM {Student.tableName()}')
        assert len(resultList) == 2 and [x.name for x in resultList] == ['Tom', 'Jerry']


@pytest.mark.order()
@pytest.mark.asyncio(scope='session')
async def test_getValue():
    async with DB.getCursor() as cursor:
        result = await cursor.getValue(int, f'SELECT `age` FROM {Student.tableName()} WHERE `name` LIKE %s', 'Tom')
        assert result and result == 22


@pytest.mark.order()
@pytest.mark.asyncio(scope='session')
async def test_getValueList():
    async with DB.getCursor() as cursor:
        result = await cursor.getValueList(int, f'SELECT `id` FROM {Student.tableName()} WHERE `id` IN ( %x )', 1, 2)
        assert result and result == [1, 2]
