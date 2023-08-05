from .core import VectorDictionary, Fittable
from .tokenizers import RegexTokenizer
import numpy as np


class BaseVectorizer(Fittable):
    """
    A base class for building vectorizers with a scikit-learn like API.
    """

    def __init__(self, window=5, tokenizer=RegexTokenizer()):
        """
        :param tokenizer: A BaseTokenizer subclass object to tokenize the text
        """
        Fittable.__init__(self)

        self.tokenizer = tokenizer
        self.window = window

        self.processed_documents = []  # List of tokenized, lowercased documents
        self.unique_words = []  # List of uniques words in all documents.

    def fit(self, documents):
        Fittable.fit(self, documents)

        for doc in self.documents:
            self.processed_documents.append(self.tokenizer.tokenize(doc.lower()))

        documents_corpus = self.tokenizer.tokenize(" ".join(self.documents).lower())
        self.unique_words = list(set(self.unique_words) | set(documents_corpus))

    def transform(self):
        pass

    def fit_transform(self, documents):
        self.fit(documents)
        return self.transform()

    def predict(self, documents):
        pass

    def synchronize(self, from_vectorizer):
        """
        Synchronize two vectorizer to return compatibles vectors
        """
        self.unique_words = from_vectorizer.unique_words


class WordVectorizer(BaseVectorizer):
    """
    A simple distributional vectorizer algorithm.
    """

    def transform(self):
        vector_dict = VectorDictionary(dimension=len(self.unique_words))

        for n_word in self.unique_words:
            n_word_vectors = np.empty([0, len(self.unique_words)], dtype=int)

            for document in self.processed_documents:
                doc_n_word_indexes = [i for i, x in enumerate(document) if x == n_word]  # list of index of `n_word` in document

                if doc_n_word_indexes:
                    # Build a vector for each index...
                    for index in doc_n_word_indexes:
                        text_selection = document[index - self.window:index] +\
                                         document[index + 1:index + self.window + 1]

                        n_word_vectors = np.append(n_word_vectors,
                                                   np.array([[text_selection.count(word) for word in self.unique_words]]),
                                                   axis=0)

                else:
                    np.append(n_word_vectors, np.zeros(len(self.unique_words)))

            # ...And sum them to build the final vector :
            vector_dict[n_word] = np.sum(n_word_vectors, axis=0)

        return vector_dict


class PositionalWordVectorizer(BaseVectorizer):
    """
    A distributional word vectorizer that use proximity with other words.
    """

    def transform(self):
        vector_dict = VectorDictionary(dimension=len(self.unique_words))

        for n_word in self.unique_words:
            n_word_vectors = np.empty([0, len(self.unique_words)], dtype=int)

            for document in self.processed_documents:
                doc_n_word_indexes = [i for i, x in enumerate(document) if x == n_word]

                if doc_n_word_indexes:
                    for index in doc_n_word_indexes:
                        before_n_word_selection = list(reversed(document[index - self.window:index]))
                        after_n_word_selection = document[index + 1:index + self.window + 1]

                        vector = []
                        for word in self.unique_words:
                            if word in before_n_word_selection:
                                vector.append(before_n_word_selection.index(word) + 1)
                            elif word in after_n_word_selection:
                                vector.append(after_n_word_selection.index(word) + 1)
                            else:
                                vector.append(0)

                        n_word_vectors = np.append(n_word_vectors, np.array([vector]), axis=0)

                else:
                    n_word_vectors = np.append(n_word_vectors, np.array([np.zeros(len(self.unique_words))]), axis=0)

            vector_dict[n_word] = np.ma.median(np.ma.masked_where(n_word_vectors == 0, n_word_vectors), axis=0).filled(0)

        return vector_dict


class DocVectorizer(BaseVectorizer):
    """
    A simple count based/bag-of-word vectorizer, to vectorize a whole text.
    """

    def transform(self):
        vector_dict = VectorDictionary(dimension=len(self.unique_words))

        for raw_document, processed_document in zip(self.documents, self.processed_documents):
            vector_dict[raw_document] = np.array([processed_document.count(word) for word in self.unique_words], dtype=int)

        return vector_dict


class SemanticDocVectorizer(BaseVectorizer):
    """
    Use the semantic WordVectorizer to vectorize a whole text.
    """

    def transform(self):
        vector_dict = VectorDictionary(dimension=len(self.unique_words))

        for document in self.documents:
            vectorizer = WordVectorizer(window=self.window, tokenizer=self.tokenizer)
            vectorizer.fit(document)
            vectorizer.synchronize(self)

            document_vocabulary_vectors = vectorizer.transform()
            vector_dict[document] = np.mean(np.array(document_vocabulary_vectors.values()), axis=0)

        return vector_dict
