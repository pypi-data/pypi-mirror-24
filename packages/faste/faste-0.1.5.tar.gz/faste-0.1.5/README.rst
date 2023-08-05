dictionary style caches
=======================

Faste is a cache library to allow many different cache algorithms in Python, with the functionality of a regular dict.
Anything you can do to a dict, you can do to these caches.

``$ pip install faste``

All The Caches(tm)
~~~~~~~~~~~~~~~~~~

Every cache has the signature ``CacheNameHere(max_items)``

max_items is the max length of the cache before items start getting evicted.


.. code:: python

    import faste

    # Random Replacement
    # When cache is full, random items are removed to make space for new ones
    RR = faste.caches.RRCache(max_items)

    # First In First Out
    # When cache is full, cache evicts the last key that was set
    FIFO = faste.caches.FIFOCache(max_items)

    # Least Recently Used
    # When cache is full, least recently accessed item is evicted
    LRU = faste.caches.LRUCache(max_items)

    # Most Recently Used
    # When cache is full, most recently accessed item is evicted
    # Useful for caches where old data is more commonly accessed
    MRU = faste.caches.MRUCache(max_items)

    # Least Frequently Used
    # When cache is full, least frequently accessed item is evicted
    LFU = faste.caches.LFUCache(max_items)

