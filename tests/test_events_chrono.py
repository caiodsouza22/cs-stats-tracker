from roundwire.models.events import chronological_events
def test_chrono(cs2_match):
    events = chronological_events(cs2_match.rounds[0])
    assert events == sorted(events, key=lambda e: (e.tick_ms, e.kind.value, e.summary))
