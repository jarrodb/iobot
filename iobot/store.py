
# this needs formal tests...

class Store(object):
    """ Memory Storage (for now)

    Public Methods:
    create
    upsert
    delete
    find
    find_one
    ensure_index
    """
    _ID_KEY = '_id'
    _ID_BITS = 64

    def __init__(self):
        self._queue = []
        self._indexes = {}

        self.ensure_index(self._ID_KEY) # create an index for _ID_KEY

    # public:

    def create(self, item):
        assert isinstance(item, dict), "Query must be a dict"

        if item.has_key(self._ID_KEY):
            if self.find_one({self._ID_KEY:item[self._ID_KEY]}):
                raise ValueError('Cannot create a document with existing id')
        else:
            self._assign_id(item)

        self._queue.append(item)
        self._create_index_for(item)

    def upsert(self, item):
        """ repair this """
        if item.has_key(self._ID_KEY):
            doc = self.find_one({self._ID_KEY:item[self._ID_KEY]})
            if doc:
                # basically delete it to be replaced... ughh
                self.delete({self._ID_KEY:item[self._ID_KEY]})
        else:
            # document has no id, so we're not updating
            # assign one to insert
            self._assign_id(item)

        self.create(item)

    def delete(self, query):
        # take advantages of indexes
        matches = self.find(query)
        deleted = len(matches)

        for doc in matches:
            self._remove_index_for(doc)
            self._queue.pop(self._queue.index(doc))

        return deleted

    def find(self, query):
        #needs so much more optimization
        assert isinstance(query, dict), "Query must be a dict"

        if not query:
            # this should return an iterator or a cursor obj
            return self._queue

        indexed = []

        compare_keys = zip(self._indexes.keys(), query.keys())
        key_matches = [qk for ik, qk in compare_keys if ik == qk]

        if key_matches:
            for key in key_matches:
                if key in self._indexes:
                    doc = self._indexes[key].get(query[key], None)
                    if doc and doc not in indexed:
                        indexed.append(doc)

        return self._search_queue_or_indexed(query, indexed)

    def find_one(self, query):
        results = self.find(query)
        return results[0] if results else None

    def ensure_index(self, key):
        if key not in self._indexes:
            self._create_index_for_key(key)

        return True if self._indexes.has_key(key) else False

    # private:

    def _assign_id(self, item):
        item[self._ID_KEY] = self._generate_id()

    def _generate_id(self):
        """ simple for now """
        import random
        return unicode(random.getrandbits(self._ID_BITS))

    def _search_queue_or_indexed(self, query, indexed=False):
        search = indexed if indexed else self._queue
        found = [doc for doc in self._queue if self._kv_compare(query, doc)]
        return found

    def _kv_compare(self, query, doc):
        match = 1
        for key in query.keys():
            if not doc.has_key(key):
                match = 0
                break
            elif query[key] != doc[key]:
                match = 0
                break

        return True if match else False

    def _remove_index_for(self, item):
        for key in item:
            if key in self._indexes:
                self._indexes[key].pop(item.get(key))

    def _create_index_for(self, item):
        # unique indexes only for now
        for key in self._indexes:
            if item.has_key(key):
                self._indexes[key][item.get(key)] = item

    def _create_index_for_key(self, key):
        # unique indexes only for now
        if not self._indexes.has_key(key):
            self._indexes[key] = {}

            for item in self._queue:
                if item.has_key(key):
                    self._indexes[key][item.get(key)] = item

