from documents.services.cleaning import clean_text

def test_clean_text_strips_and_normalizes():
    t = "  hello \n\n\n world \x0c"
    out = clean_text(t)
    assert "hello" in out
    assert "\n\n" in out
