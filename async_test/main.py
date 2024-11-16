import asyncio
import time


async def async_task(name):
    print(f"{name}: 시작")
    await asyncio.sleep(1)  # 비동기 작업
    print(f"{name}: 완료")


async def main():
    print("콜 스택 작업 1 시작")
    task1 = asyncio.create_task(async_task("비동기 작업 3"))
    task1 = asyncio.create_task(async_task("비동기 작업 3"))
    task1 = asyncio.create_task(async_task("비동기 작업 3"))
    await asyncio.sleep(3)
    # 비동기 작업을 이벤트 루프에 등록
    print("모든 작업 완료")


asyncio.run(main())
