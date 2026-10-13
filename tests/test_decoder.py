"""
Unit tests for bangla-pdf-decoder.
"""

import pytest
from bangla_pdf_decoder import decode_bangla_pdf_text


class TestLocationAndNameLigatures:
    """Tests for critical Bengali location names and conjuncts."""

    def test_coxs_bazar(self):
        """Verify Cox's Bazar decodes to কক্সবাজার, not কব্রবাজার or কভ্রবাজার."""
        raw = "কুতুবিদয়া পাড়া, বদরখালী, চকিরয়া, কÔবাজার"
        decoded = decode_bangla_pdf_text(raw)
        assert "কক্সবাজার" in decoded
        assert "কব্রবাজার" not in decoded
        assert "কভ্রবাজার" not in decoded

    def test_chattogram(self):
        """Verify Chattogram decodes to চট্টগ্রাম, not চযগ্রাম."""
        raw = "অঞ্চল: চÿগ্রাম জেলা: চÿগ্রাম"
        decoded = decode_bangla_pdf_text(raw)
        assert "চট্টগ্রাম" in decoded
        assert "চযগ্রাম" not in decoded

    def test_t_ta_conjuncts(self):
        """Verify ট্ট (ÿ) in names and addresses."""
        assert "ভট্টাচার্য" in decode_bangla_pdf_text("মুি× ভÿাচাযÎ")
        assert "পট্টি" in decode_bangla_pdf_text("চামার পিÿ Ïরাড")
        assert "কুট্টি" in decode_bangla_pdf_text("মাতা: ƣিÿ")

    def test_k_sa_conjuncts(self):
        """Verify ক্স (Ô, Ö) in words like রিক্সা, বক্স, এপেক্স."""
        assert "রিক্সা" in decode_bangla_pdf_text("িরÔা/ভËান চালক")
        assert "বক্স" in decode_bangla_pdf_text("কাজী মজিদ বÔ")
        assert "এপেক্স" in decode_bangla_pdf_text("এেপÔ টËানারী")
        assert "এনেক্স" in decode_bangla_pdf_text("এনেÖর এফ-২০৪")

    def test_k_ka_and_b_ba_conjuncts(self):
        """Verify ক্ক (Ñ) in Akkas and ব্ব (ļ) in Jabbar."""
        assert "আক্কাস" in decode_bangla_pdf_text("আলী আÑাস িময়া")
        assert "আব্দুল জব্বার" in decode_bangla_pdf_text("আĺুল জļার")

    def test_k_ta_conjuncts(self):
        """Verify ক্ট (Ò) in factory, project, sector."""
        assert "গ্যাসফ্যাক্টরী" in decode_bangla_pdf_text("গËাসফËাÒরী")
        assert "সেক্টর" in decode_bangla_pdf_text("ÏসÒর সদর দপ্তর")
        assert "ফ্যাক্টরি" in decode_bangla_pdf_text("ãাস ফËাÒির")

    def test_c_ca_and_c_cha_and_shu(self):
        """Verify চ্চ (î), চ্ছ (ę), and শু (ï)."""
        assert "বাচ্চু" in decode_bangla_pdf_text("বাîু িময়া")
        assert "মোদাচ্ছের" in decode_bangla_pdf_text("Ðসয়দ Ïমাদােęর আলী")
        assert "শুভ" in decode_bangla_pdf_text("ïভ")

    def test_n_tha_conjuncts(self):
        """Verify ন্থ (ģ) in Panthapath."""
        assert "পান্থপথ" in decode_bangla_pdf_text("পাģপথ, åীন Ïরাড")
        assert "পান্থনিবাস" in decode_bangla_pdf_text("পাģিনবাস")

    def test_p_la_conjuncts(self):
        """Verify প্ল (ı) in Plaza, Biplob."""
        assert "প্লাজা" in decode_bangla_pdf_text("ধানমিŒড ıাজা")
        assert "বিপ্লব" in decode_bangla_pdf_text("িবıব")

    def test_s_ma_conjuncts(self):
        """Verify স্ম (ů) in Smriti."""
        assert "স্মৃতি" in decode_bangla_pdf_text("০০৪৬. নাম: ůৃিত Ïবগম")

    def test_r_u_conjuncts(self):
        """Verify রু / রূ (Ƃ) in Faruk, Rupali."""
        assert "ফারুক" in decode_bangla_pdf_text("িপতা: ফাƂক রশীদ")
        assert "রুপালী" in decode_bangla_pdf_text("Ƃপালী আ×ার") or "রূপালী" in decode_bangla_pdf_text("Ƃপালী আ×ার")

    def test_d_da_conjuncts(self):
        """Verify দ্ব (ě) in Deen, Dwijen."""
        assert "দ্বীন" in decode_bangla_pdf_text("ěীন ÏমাহাŇদ")
        assert "দ্বিপু" in decode_bangla_pdf_text("িěপু রাজ বংশী")

    def test_d_ma_conjuncts(self):
        """Verify দ্ম (Ě) in Padmabati."""
        assert "পদ্মাবতী" in decode_bangla_pdf_text("পĚাবতী িবśাস")

    def test_ng_ga_conjuncts(self):
        """Verify ঙ্গ (ê) in Jahangir."""
        assert "জাহাঙ্গীর" in decode_bangla_pdf_text("িপতা: জাহাêীর")

    def test_ph_la_conjuncts(self):
        """Verify ফ্ল (ķ, ĸ) in Flat."""
        assert "ফ্ল্যাট" in decode_bangla_pdf_text("ķËাট নং ই ১০")
        assert "ফ্ল্যাট" in decode_bangla_pdf_text("ĸËাট নং ৮সি")

    def test_b_ra_conjuncts(self):
        """Verify ব্র (Ľ) in Ibrahim."""
        assert "ইব্রাহীম" in decode_bangla_pdf_text("িপতা: ইĽাহীম")

    def test_b_la_conjuncts(self):
        """Verify ব্ল (ľ) in Block."""
        assert "ব্লক" in decode_bangla_pdf_text("টËানারী ľক")

    def test_l_da_conjuncts(self):
        """Verify ল্ড (ŏ) in Building, Holding."""
        assert "বিল্ডিং" in decode_bangla_pdf_text("িবিŏং-এ")
        assert "হোল্ডিং" in decode_bangla_pdf_text("Ïহািŏং নং ১৭")

    def test_badda_and_gulshan(self):
        """Verify বাড্ডা (Ă) and গুলশান (Ž)."""
        assert "বাড্ডা" in decode_bangla_pdf_text("বাĂা নগর")
        assert "গুলশান" in decode_bangla_pdf_text("Žলশান আরা")


class TestVowelReordering:
    """Tests for Bengali pre-base vowel reordering."""

    def test_independent_vowel_followed_by_e_kar(self):
        assert "আমেনা" in decode_bangla_pdf_text("আেমনা খাতুন")
        assert "উম্মে" in decode_bangla_pdf_text("উেম্ম কুলসুম")
        assert "আ\u09dfেশা" in decode_bangla_pdf_text("আেয়শা বিবি")

    def test_medial_e_kar_reordering(self):
        assert "খালেক" in decode_bangla_pdf_text("খােলক")
        assert "সালেম" in decode_bangla_pdf_text("সােলম")
        assert "তাহেরা" in decode_bangla_pdf_text("তােহরা")

    def test_preservation_of_correct_words(self):
        assert decode_bangla_pdf_text("রেহানা") == "রেহানা"
        assert decode_bangla_pdf_text("বেগম") == "বেগম"
        assert decode_bangla_pdf_text("ঢাকা") == "ঢাকা"

    def test_dotted_circle_and_hasant_cleanup(self):
        assert "মোহাম্মদ" in decode_bangla_pdf_text("মো◌্হাম্মদ")
        assert "মোহাম্মদ" in decode_bangla_pdf_text("মো্হাম্মদ")


class TestNewlyMappedGlyphs:
    """Test suite for newly verified embedded font glyph mappings."""

    def test_newly_mapped_glyphs(self):
        assert "জাবেদ আলী" in decode_bangla_pdf_text("জােব\x8a আলী")
        assert "আহাদ উল্লা" in decode_bangla_pdf_text("আহা\x8a উŌা")
        assert "বাঁশদহ" in decode_bangla_pdf_text("বঁাশ\x8aহ")
        assert "মধ্য পাড়া" in decode_bangla_pdf_text("ম\x8bয পাড়া")
        assert "পশ্চিম" in decode_bangla_pdf_text("পি\x91চম")
        assert "সূর্য" in decode_bangla_pdf_text("সূ\x92Î")
        assert "মিন্টু" in decode_bangla_pdf_text("িম\x95টু")
        assert "সামস উদ্দিন" in decode_bangla_pdf_text("সাম¨ উিėন")
        assert "আব্দুস ছামাদ" in decode_bangla_pdf_text("আĺু¨ ছামাদ")
        assert "বাড়ি" in decode_bangla_pdf_text("বািµ")
        assert "খানপাড়া" in decode_bangla_pdf_text("খানপাµা")
        assert "আনোয়ার" in decode_bangla_pdf_text("আেনাÂার")
        assert "সোলায়মান" in decode_bangla_pdf_text("ÏসালাÂমান")
        assert "সোনাউল্লাহ" in decode_bangla_pdf_text("ÏসানাউলÌাহ")
        assert "বাঞ্ছার চর" in decode_bangla_pdf_text("বাüার চর")
        assert "লক্ষ্মীপুর" in decode_bangla_pdf_text("লÛীপুর")
        assert "কেন্দুয়া" in decode_bangla_pdf_text("েকƏয়া")
        assert "চান্দু মিয়া" in decode_bangla_pdf_text("চাƏ িময়া")
        assert "দাঁতভাঙ্গা" in decode_bangla_pdf_text("দঁাতভাঙ্গা")
        assert "তেজগাঁও" in decode_bangla_pdf_text("তেজগঁাও")
        assert "নেত্রকোনা" in decode_bangla_pdf_text("নেত্রকানা")
        assert "গুজরিকোনা" in decode_bangla_pdf_text("গুজিরেকানা")

