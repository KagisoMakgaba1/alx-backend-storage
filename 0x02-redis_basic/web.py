#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import time
from functools import wraps


# Dictionary to cache responses and their timestamps
cache = {}
# Dictionary to track access counts
access_counts = {}
# Cache expiration time in seconds
CACHE_EXPIRATION = 10


def cache_decorator(func):
    @wraps(func)
    def wrapper(url):
        current_time = time.time()

        # Check if the URL is already cached and if it is still valid
        if url in cache:
            cache_entry, timestamp = cache[url]
            if current_time - timestamp < CACHE_EXPIRATION:
                print(f"Cache hit for URL: {url}")
                return cache_entry

        # If not cached or expired, call the function to fetch the page
        print(f"Cache miss for URL: {url}")
        response = func(url)
        cache[url] = (response, current_time)
        return response

    return wrapper


@cache_decorator
def get_page(url: str) -> str:
    # Track the number of times the URL has been accessed
    if url in access_counts:
        access_counts[url] += 1
    else:
        access_counts[url] = 1

    # Fetch the content using requests
    response = requests.get(url)
    response.raise_for_status()  # Ensure we raise an error for bad responses
    return response.text
