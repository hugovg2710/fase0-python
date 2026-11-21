import asyncio
import random
import time


class ProviderError(Exception):
    """Fallo transitorio del proveedor (Simulado)"""


async def fake_classify(text: str, *, fail_rate: float = 0.3) -> str:
    await asyncio.sleep(random.uniform(0.2, 1.2))
    if random.random() < fail_rate():
        raise ProviderError("proveedor no disponible")
    return "breakdown" if "ruido" in text.lower() else "general"

async def classify_with_retries(text: str, *, timeout_s: float = 1.0, attempts: int = 3) -> str:
    delay = 0.1
    for attempt in range(1, attempts + 1):
        try:
            async with asyncio.timeout(timeout_s):
                return await fake_classify(text)
        except(TimeoutError, ProviderError) as exc: 
            if attempt == attempts:
                raise ProviderError(f"agotados {attempts} intentos: {exc!r}") from exc
            await asyncio.sleep(delay + random.uniform(0, delay))
            delay *= 2
    raise AssertionError("Inalcanzable")

async def classify_all(texts: list[str], *, max_concurrency: int = 3) -> list[str]:
    semaphore = asyncio.Semaphore(max_concurrency)

    async def one(text: str) -> str:
        async with semaphore:
            try:
                return await classify_with_retries(text)
            except ProviderError:
                return "requires_review"  # nunca inventar un resultado

    return await asyncio.gather(*(one(t) for t in texts))


async def main() -> None:
    async def wait(seconds: float) -> float:
        await asyncio.sleep(seconds)
        return seconds

    start = time.perf_counter()
    for s in (0.5, 0.5, 0.5):
        await wait(s)

    print(f"secuencial: {time.perf_counter() - start:.1f} s")  # 1.5 s

    start = time.perf_counter()
    await asyncio.gather(
        wait(0.5),
        wait(0.5),
        wait(0.5),
    )

    print(f"concurrente: {time.perf_counter() - start:.1f} s")  # 0.5 s

    texts = [
        f"incidencia {i}: ruido" if i % 2 else f"incidencia {i}"
        for i in range(8)
    ]

    print(await classify_all(texts))

if __name__ == "__main__":
    asyncio.run(main())