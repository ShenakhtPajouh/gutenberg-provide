from paragraph_analyse import analyse
import HP
import API
import numpy as np


def pars_metadata_from_book(book_id):
    with open(HP.BOOKS_DIR + str(book_id) + ".txt", 'r', encoding='utf-8') as f:
        text = f.read()
    paragraphs = text.split('\n\n')
    paragraphs = [par for par in paragraphs if par != '']
    result = []
    keys = HP.pre_keys
    for par in paragraphs:
        res = analyse(par)
        res = [res[key] for key in keys]
        result.append(res)
    metadata = np.array(result, dtype=np.int32)
    local_id = np.arange(1, len(result) + 1, dtype=np.int32)
    local_id = np.expand_dims(local_id, 1)
    metadata = np.concatenate([local_id, metadata], axis=1)
    return metadata


def create_pars_metadata(books_id, Print=False):
    books_id = sorted(books_id)
    metadata = np.zeros(shape=(0, len(HP.pre_keys) + 2), dtype=np.int32)
    lens = len(books_id)
    for ind, i in enumerate(books_id):
        if Print:
            print("Book: " + str(i) + "  " + str(ind + 1) + "/" + str(lens))
        met = pars_metadata_from_book(i)
        book_id = np.zeros(met.shape[0], dtype=np.int32) + i
        book_id = np.expand_dims(book_id, 1)
        met = np.concatenate([book_id, met], 1)
        metadata =np.concatenate([metadata, met], 0)
    global_id = np.arange(np.shape(metadata)[0], dtype=np.int32) + 1
    global_id = np.expand_dims(global_id, 1)
    metadata = np.concatenate([global_id, metadata], 1)
    return metadata


if __name__ == "__main__":
    books = API.get_books()
    metadata = create_pars_metadata(books, Print=True)
    np.save(HP.PARAGRAPH_METADATA, metadata)






