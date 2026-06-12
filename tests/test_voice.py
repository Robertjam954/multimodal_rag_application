from voice.diarizer import merge_by_speaker


def test_merge_collapses_adjacent_same_speaker():
    items = [
        {"speaker": "A", "start": 0.0, "end": 1.0, "text": "hello"},
        {"speaker": "A", "start": 1.1, "end": 2.0, "text": "world"},
        {"speaker": "B", "start": 2.5, "end": 3.0, "text": "hi"},
    ]
    out = merge_by_speaker(items)
    assert len(out) == 2
    assert out[0]["text"] == "hello world"
