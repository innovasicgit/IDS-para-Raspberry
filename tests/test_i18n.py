from config.i18n import DEFAULT_LANGUAGE, _TRANSLATIONS, translate


def test_translate_formats_selected_language():
    assert translate("connected_as", "en", username="admin") == "Connected as: admin"


def test_translate_applies_format_specs():
    assert translate("next_capture", "es", minutes=4, seconds=7).endswith("04:07 min:s")
    assert "**80/100** (80%)" in translate("capture_progress_packets", "es", current=80, total=100, percent=80.0)
    assert translate("active_threshold", "en", value=0.7) == "Active threshold: 0.70"


def test_translate_falls_back_to_spanish_for_unknown_language():
    assert translate("logout", "fr") == translate("logout", DEFAULT_LANGUAGE)


def test_catalog_has_matching_languages_without_spanish_in_english():
    assert set(_TRANSLATIONS["es"]) == set(_TRANSLATIONS["en"])
    spanish_punctuation = "áéíóúñÁÉÍÓÚ¿¡"
    assert not any(
        any(character in value for character in spanish_punctuation)
        for value in _TRANSLATIONS["en"].values()
    )