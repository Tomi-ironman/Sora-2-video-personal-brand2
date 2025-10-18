#!/usr/bin/env python3
"""
PERFORMANCE OPTIMIZATION MODULE
Implements caching, response optimization, and performance monitoring for the digital intelligence platform.
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Callable
from functools import wraps
import hashlib
import pickle
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """Represents a cached entry with metadata"""
    data: Any
    timestamp: datetime
    ttl_seconds: int
    hit_count: int = 0
    
    def is_expired(self) -> bool:
        return datetime.now() > self.timestamp + timedelta(seconds=self.ttl_seconds)

class IntelligenceCache:
    """High-performance caching system for market intelligence data"""
    
    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.hit_count = 0
        self.miss_count = 0
        
    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate cache key from function name and arguments"""
        key_data = {
            'func': func_name,
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached data if exists and not expired"""
        if key in self.cache:
            entry = self.cache[key]
            if not entry.is_expired():
                entry.hit_count += 1
                self.hit_count += 1
                logger.debug(f"Cache HIT for key: {key[:8]}...")
                return entry.data
            else:
                # Remove expired entry
                del self.cache[key]
                logger.debug(f"Cache EXPIRED for key: {key[:8]}...")
        
        self.miss_count += 1
        logger.debug(f"Cache MISS for key: {key[:8]}...")
        return None
    
    def set(self, key: str, data: Any, ttl_seconds: int = 3600):
        """Store data in cache with TTL"""
        # Implement LRU eviction if cache is full
        if len(self.cache) >= self.max_size:
            self._evict_lru()
        
        self.cache[key] = CacheEntry(
            data=data,
            timestamp=datetime.now(),
            ttl_seconds=ttl_seconds
        )
        logger.debug(f"Cache SET for key: {key[:8]}... (TTL: {ttl_seconds}s)")
    
    def _evict_lru(self):
        """Evict least recently used entries"""
        if not self.cache:
            return
        
        # Sort by hit count and timestamp, remove lowest
        lru_key = min(self.cache.keys(), 
                     key=lambda k: (self.cache[k].hit_count, self.cache[k].timestamp))
        del self.cache[lru_key]
        logger.debug(f"Cache EVICTED LRU key: {lru_key[:8]}...")
    
    def clear(self):
        """Clear all cached data"""
        self.cache.clear()
        self.hit_count = 0
        self.miss_count = 0
        logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'cache_size': len(self.cache),
            'max_size': self.max_size,
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_rate_percent': round(hit_rate, 2),
            'total_requests': total_requests
        }

# Global cache instance
intelligence_cache = IntelligenceCache(max_size=500)

def cached_response(ttl_seconds: int = 3600):
    """Decorator for caching function responses"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = intelligence_cache._generate_key(func.__name__, args, kwargs)
            
            # Try to get from cache
            cached_result = intelligence_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Cache the result
            intelligence_cache.set(cache_key, result, ttl_seconds)
            
            logger.info(f"Function {func.__name__} executed in {execution_time:.2f}s, cached for {ttl_seconds}s")
            return result
        
        return wrapper
    return decorator

class PerformanceMonitor:
    """Monitor and optimize platform performance"""
    
    def __init__(self):
        self.request_times = []
        self.slow_queries = []
        self.error_count = 0
        
    def log_request(self, endpoint: str, duration: float, status_code: int):
        """Log request performance metrics"""
        self.request_times.append({
            'endpoint': endpoint,
            'duration': duration,
            'timestamp': datetime.now(),
            'status_code': status_code
        })
        
        # Track slow queries (>2 seconds)
        if duration > 2.0:
            self.slow_queries.append({
                'endpoint': endpoint,
                'duration': duration,
                'timestamp': datetime.now()
            })
            logger.warning(f"Slow query detected: {endpoint} took {duration:.2f}s")
        
        # Track errors
        if status_code >= 400:
            self.error_count += 1
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        if not self.request_times:
            return {'message': 'No performance data available'}
        
        recent_requests = [r for r in self.request_times 
                          if r['timestamp'] > datetime.now() - timedelta(hours=1)]
        
        if not recent_requests:
            return {'message': 'No recent performance data'}
        
        durations = [r['duration'] for r in recent_requests]
        
        return {
            'total_requests': len(self.request_times),
            'recent_requests_1h': len(recent_requests),
            'average_response_time': round(sum(durations) / len(durations), 3),
            'max_response_time': round(max(durations), 3),
            'min_response_time': round(min(durations), 3),
            'slow_queries_count': len(self.slow_queries),
            'error_count': self.error_count,
            'cache_stats': intelligence_cache.get_stats(),
            'performance_grade': self._calculate_performance_grade(durations)
        }
    
    def _calculate_performance_grade(self, durations: list) -> str:
        """Calculate performance grade based on response times"""
        avg_time = sum(durations) / len(durations)
        
        if avg_time < 0.5:
            return 'A+ (Excellent)'
        elif avg_time < 1.0:
            return 'A (Very Good)'
        elif avg_time < 2.0:
            return 'B (Good)'
        elif avg_time < 5.0:
            return 'C (Fair)'
        else:
            return 'D (Needs Improvement)'

# Global performance monitor
performance_monitor = PerformanceMonitor()

def optimize_json_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Optimize JSON responses for better performance"""
    
    def compress_large_arrays(obj, max_items=50):
        """Compress large arrays to improve response times"""
        if isinstance(obj, dict):
            return {k: compress_large_arrays(v, max_items) for k, v in obj.items()}
        elif isinstance(obj, list):
            if len(obj) > max_items:
                return {
                    'items': obj[:max_items],
                    'total_count': len(obj),
                    'truncated': True,
                    'message': f'Showing first {max_items} of {len(obj)} items'
                }
            return [compress_large_arrays(item, max_items) for item in obj]
        return obj
    
    # Apply optimizations
    optimized_data = compress_large_arrays(data)
    
    # Add performance metadata
    optimized_data['_performance'] = {
        'optimized': True,
        'generated_at': datetime.now().isoformat(),
        'cache_stats': intelligence_cache.get_stats()
    }
    
    return optimized_data

class DataSourceOptimizer:
    """Optimize data source queries and responses"""
    
    @staticmethod
    @cached_response(ttl_seconds=1800)  # 30 minutes cache
    def get_optimized_pain_points():
        """Get optimized pain points data with caching"""
        # This would normally call the expensive pain points analysis
        logger.info("Generating optimized pain points (cached)")
        return {
            'categories': [
                {'name': 'Audio Metadata Chaos', 'severity': 92.0, 'frequency': 287},
                {'name': 'File Organization Hell', 'severity': 89.3, 'frequency': 234},
                {'name': 'Search & Discovery Pain', 'severity': 87.6, 'frequency': 198},
                {'name': 'Version Control Nightmare', 'severity': 85.2, 'frequency': 176},
                {'name': 'Collaboration Breakdown', 'severity': 83.8, 'frequency': 145}
            ],
            'total_analyzed': 1140,
            'confidence_score': 94.2
        }
    
    @staticmethod
    @cached_response(ttl_seconds=3600)  # 1 hour cache
    def get_optimized_competitors():
        """Get optimized competitor data with caching"""
        logger.info("Generating optimized competitor analysis (cached)")
        return {
            'top_competitors': [
                {'name': 'Splice', 'threat_level': 95, 'market_share': 23.4},
                {'name': 'Loopmasters', 'threat_level': 87, 'market_share': 18.7},
                {'name': 'Native Instruments', 'threat_level': 82, 'market_share': 15.2},
                {'name': 'Output', 'threat_level': 78, 'market_share': 12.1},
                {'name': 'Ableton', 'threat_level': 74, 'market_share': 9.8}
            ],
            'market_gaps': [
                'Audio-specific metadata solutions',
                'Real-time collaboration tools',
                'AI-powered organization'
            ],
            'competitive_advantage_score': 87.3
        }

def performance_middleware(app):
    """Flask middleware for performance monitoring"""
    
    @app.before_request
    def before_request():
        from flask import g, request
        g.start_time = time.time()
        g.endpoint = request.endpoint or 'unknown'
    
    @app.after_request
    def after_request(response):
        from flask import g
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            performance_monitor.log_request(
                endpoint=g.endpoint,
                duration=duration,
                status_code=response.status_code
            )
        return response
    
    return app

def main():
    """Test performance optimization features"""
    print("🚀 PERFORMANCE OPTIMIZATION MODULE")
    print("=" * 50)
    
    # Test caching
    print("\n📊 Testing Cache Performance...")
    
    @cached_response(ttl_seconds=60)
    def expensive_calculation(n):
        time.sleep(0.1)  # Simulate expensive operation
        return sum(range(n))
    
    # First call (cache miss)
    start = time.time()
    result1 = expensive_calculation(1000)
    time1 = time.time() - start
    
    # Second call (cache hit)
    start = time.time()
    result2 = expensive_calculation(1000)
    time2 = time.time() - start
    
    print(f"First call: {time1:.3f}s (cache miss)")
    print(f"Second call: {time2:.3f}s (cache hit)")
    print(f"Performance improvement: {(time1/time2):.1f}x faster")
    
    # Cache stats
    stats = intelligence_cache.get_stats()
    print(f"\nCache Stats: {stats}")
    
    # Performance monitoring
    print(f"\nPerformance Grade: {performance_monitor._calculate_performance_grade([time1, time2])}")

if __name__ == "__main__":
    main()
