import os
import logging

import xapian

from pylons import config
from exceptions import IndexException, NotFoundException

log = logging.getLogger(__name__)

READ = 1
WRITE = 2


def index_string(collection, identifier, data, append=False):
    """Indexes the new data in the collection. Use append to add information to
    an object if found. If you omit append, it will always overwrite the whole
    record.

    collection := the collection to use for indexing
    identifier := the unique identifier for the object, like it's record id.
                  Must be an integer
    data := the data belonging to the record
    append := wether or not to append to existing data.
    """

    colpath = _get_path_to_collection(collection)
    if not _dir_exists(colpath):
        _create_path(colpath)

    db = _open_collection(colpath, WRITE)
    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("dutch")
    indexer.set_stemmer(stemmer)

    olddoc = None
    try:
        olddoc = get_object(collection, identifier, True)
    except NotFoundException:
        pass

    doc = xapian.Document()
    if append and olddoc:
        for term in olddoc:
            doc.add_term(term)
    else:
        doc.add_term('ident:%d' % identifier)

    doc.set_data(str(identifier))

    indexer.set_document(doc)
    indexer.index_text(data)

    if olddoc:
        db.delete_document(olddoc.docid)
    db.add_document(doc)
    db.flush()


def get_object(collection, identifier, doc=False):
    id = 'ident:%d' % identifier
    docs = find_objects(collection, id, doc)
    if len(docs) == 0:
        raise NotFoundException("Couldn't find object")
    else:
        if doc:
            return docs[0]
        else:
            return docs[0].document.get_data()


def find_objects(collection, keywords, docs=False):
    colpath = _get_path_to_collection(collection)
    if not _dir_exists(colpath):
        _create_path(colpath)

    # Collection/search initialisation
    db = _open_collection(colpath, READ)
    enq = xapian.Enquire(db)
    stem = xapian.Stem("dutch")
    qp = xapian.QueryParser()

    # Query-parsing
    qp.set_database(db)
    qp.set_stemmer(stem)
    qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
    query = qp.parse_query(keywords)
    log.debug("Searching collection %r with query: %s", collection, str(query))

    enq.set_query(query)
    matches = enq.get_mset(0, 10000)
    log.debug("Found approx %d results", matches.get_matches_estimated())

    # Return documents
    if docs:
        return [m for m in matches]
    else:
        return [m.document.get_data() for m in matches]


# Internal support methods, ignore for finding out what to do with this library
def _create_dir(path):
    try:
        os.mkdir(path)
    except OSError, e:
        if e.errno == 17:       # 17 = "File exists"
            pass


def _create_path(path):
    os.mkdirs(path)


def _dir_exists(path):
    return os.path.exists(path)


def _get_path_to_collection(collection):
    if 'index_dir' not in config:
        raise IndexException("Set index_dir in configuration")
    return os.path.join(config['index_dir'], collection)


def _open_collection(path, rw=READ):
    if rw == READ:
        return xapian.Database(path)
    elif rw == WRITE:
        return xapian.WritableDatabase(path, xapian.DB_CREATE_OR_OPEN)
