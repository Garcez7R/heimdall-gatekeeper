"""Async webhook delivery queue (PHASE 3)."""
from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any

import httpx

from backend.core.webhooks import format_alert_for_webhook


@dataclass
class WebhookJob:
    """A webhook delivery job in the queue."""

    webhook_id: str
    url: str
    platform: str
    alert_id: int
    alert_data: dict[str, Any]
    created_at: str
    retry_count: int = 0
    max_retries: int = 3


class WebhookQueue:
    """Async queue for webhook deliveries with retry logic.
    
    PHASE 3: Replace with Redis/RabbitMQ for production deployment.
    """

    def __init__(self, max_workers: int = 4):
        self.queue: asyncio.Queue[WebhookJob] = asyncio.Queue()
        self.max_workers = max_workers
        self.worker_tasks: list[asyncio.Task] = []
        self.is_running = False

    async def start(self) -> None:
        """Start the webhook processing workers."""
        self.is_running = True
        for _ in range(self.max_workers):
            task = asyncio.create_task(self._worker())
            self.worker_tasks.append(task)

    async def stop(self) -> None:
        """Stop the webhook processing workers gracefully."""
        self.is_running = False
        # Wait for queue to drain
        await self.queue.join()
        # Cancel worker tasks
        for task in self.worker_tasks:
            task.cancel()
        await asyncio.gather(*self.worker_tasks, return_exceptions=True)

    async def enqueue(self, job: WebhookJob) -> None:
        """Add a webhook job to the queue."""
        await self.queue.put(job)

    async def _worker(self) -> None:
        """Process webhook jobs from the queue."""
        while self.is_running:
            try:
                job = await asyncio.wait_for(self.queue.get(), timeout=1.0)
            except asyncio.TimeoutError:
                continue

            try:
                await self._send_webhook(job)
            except Exception as e:
                print(f"Error processing webhook job {job.webhook_id}: {e}")
            finally:
                self.queue.task_done()

    async def _send_webhook(self, job: WebhookJob) -> None:
        """Send a webhook with retry logic."""
        for attempt in range(job.retry_count, job.max_retries + 1):
            try:
                payload = format_alert_for_webhook(job.alert_data, platform=job.platform)

                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(job.url, json=payload)
                    response.raise_for_status()

                print(
                    f"✓ Webhook {job.webhook_id} -> {job.url[:50]}... ({response.status_code})"
                )
                return

            except Exception as e:
                if attempt < job.max_retries:
                    # Exponential backoff: 1s, 2s, 4s
                    wait_time = 2 ** attempt
                    print(
                        f"⚠ Webhook {job.webhook_id} failed (attempt {attempt + 1}/{job.max_retries + 1}), "
                        f"retrying in {wait_time}s: {e}"
                    )
                    await asyncio.sleep(wait_time)
                    job.retry_count = attempt + 1
                else:
                    print(
                        f"✗ Webhook {job.webhook_id} -> {job.url[:50]}... FAILED after {job.max_retries + 1} attempts"
                    )
                    return


# Global webhook queue instance
# In production, this would be managed by a task scheduler or message broker
_webhook_queue: WebhookQueue | None = None


def get_webhook_queue() -> WebhookQueue:
    """Get or create the global webhook queue."""
    global _webhook_queue
    if _webhook_queue is None:
        _webhook_queue = WebhookQueue(max_workers=4)
    return _webhook_queue


async def enqueue_webhook_delivery(
    webhook_id: str, url: str, platform: str, alert_id: int, alert_data: dict[str, Any]
) -> None:
    """Enqueue a webhook delivery job."""
    job = WebhookJob(
        webhook_id=webhook_id,
        url=url,
        platform=platform,
        alert_id=alert_id,
        alert_data=alert_data,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    queue = get_webhook_queue()
    await queue.enqueue(job)
