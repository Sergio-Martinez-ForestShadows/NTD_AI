
from documents.services.cleaning import clean_text

def test_clean_text_normalizes_whitespace():
    raw = "  Hello   World \n\n This   is   a   test  \t\t\n"
    cleaned = clean_text(raw)


    assert cleaned == cleaned.strip()


    assert "  " not in cleaned

    assert "Hello World" in cleaned
    assert "This is a test" in cleaned
