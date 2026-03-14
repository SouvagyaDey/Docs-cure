"""
Reusable Redis caching mixin for DRF ModelViewSets.

Usage:
    class HospitalViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
        cache_prefix = "hospitals"
        cache_ttl = settings.CACHE_TTL_LONG
        ...

The mixin caches `list` and `retrieve` responses and automatically
invalidates the cache when `create`, `update`, `partial_update`, or
`destroy` are called.
"""

from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response

import hashlib
import logging

logger = logging.getLogger(__name__)


def _make_list_key(prefix, query_string):
    """Build a deterministic cache key for a list endpoint."""
    qs_hash = hashlib.md5(query_string.encode()).hexdigest()[:12]
    return f"{prefix}:list:{qs_hash}"


def _make_detail_key(prefix, pk):
    """Build a cache key for a single object."""
    return f"{prefix}:detail:{pk}"


def _make_user_key(prefix, user_id):
    """Build a per-user cache key."""
    return f"{prefix}:user:{user_id}"


class CachedViewSetMixin:
    """
    Mixin that adds Redis caching to list/retrieve and
    auto-invalidation on create/update/destroy.

    Class attributes:
        cache_prefix  (str) : unique namespace, e.g. "hospitals"
        cache_ttl     (int) : TTL in seconds (default: CACHE_TTL_MEDIUM)
    """

    cache_prefix: str = ""
    cache_ttl: int = getattr(settings, "CACHE_TTL_MEDIUM", 300)

    # ── cached reads ──────────────────────────────────────────────

    def list(self, request, *args, **kwargs):
        if not self.cache_prefix:
            return super().list(request, *args, **kwargs)

        key = _make_list_key(self.cache_prefix, request.META.get("QUERY_STRING", ""))
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        if response.status_code == 200:
            cache.set(key, response.data, self.cache_ttl)
        return response

    def retrieve(self, request, *args, **kwargs):
        if not self.cache_prefix:
            return super().retrieve(request, *args, **kwargs)

        pk = kwargs.get(self.lookup_field, kwargs.get("pk"))
        key = _make_detail_key(self.cache_prefix, pk)
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)

        response = super().retrieve(request, *args, **kwargs)
        if response.status_code == 200:
            cache.set(key, response.data, self.cache_ttl)
        return response

    # ── auto-invalidation on writes ──────────────────────────────

    def _invalidate_cache(self, pk=None):
        """Delete all list caches for this prefix and optionally one detail key."""
        cache.delete_pattern(f"*{self.cache_prefix}:list:*")
        if pk:
            cache.delete(_make_detail_key(self.cache_prefix, pk))
        logger.debug("Cache invalidated for %s (pk=%s)", self.cache_prefix, pk)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self._invalidate_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        pk = serializer.instance.pk
        self._invalidate_cache(pk=pk)

    def perform_destroy(self, instance):
        pk = instance.pk
        super().perform_destroy(instance)
        self._invalidate_cache(pk=pk)


# ── standalone helpers for function-based views ──────────────────

def get_or_set_cache(key, callback, ttl=300):
    """
    Try to get `key` from cache; if miss, call `callback()`,
    store the result, and return it.
    """
    data = cache.get(key)
    if data is not None:
        return data
    data = callback()
    cache.set(key, data, ttl)
    return data


def invalidate_prefix(prefix):
    """Wipe all keys matching a prefix (list + detail)."""
    cache.delete_pattern(f"*{prefix}:*")


def invalidate_user_cache(prefix, user_id):
    """Wipe a per-user cache entry."""
    cache.delete(_make_user_key(prefix, user_id))
