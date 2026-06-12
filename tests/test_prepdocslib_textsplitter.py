from prepdocslib.textsplitter import split_text


def test_short_text_returns_one_chunk():
    chunks = list(split_text("Hello world. This is a test."))
    assert chunks == ["Hello world. This is a test."]


def test_chunks_respect_max_chars():
    text = " ".join(["Sentence number %d." % i for i in range(50)])
    chunks = list(split_text(text, max_chars=200, overlap_pct=0.1))
    assert all(len(c) <= 220 for c in chunks)
    assert len(chunks) > 1


def test_overlap_includes_tail_sentence():
    text = " ".join(["First sentence.", "Second sentence.", "Third sentence.", "Fourth sentence."])
    chunks = list(split_text(text, max_chars=30, overlap_pct=0.5))
    # consecutive chunks should share at least one sentence
    for a, b in zip(chunks, chunks[1:]):
        assert any(s in b for s in a.split(". ") if s)
