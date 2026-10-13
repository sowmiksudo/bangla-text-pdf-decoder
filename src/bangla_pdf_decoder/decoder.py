"""
Core Bengali PDF Font Decoder.

Decodes legacy, hybrid, and subsetted Bengali TrueType font encodings
(such as VOXLMY+Bangla, SQDAUS+Bangla, Sutonny-in-PDF, Election Commission
and BD Govt PDFs) into clean, standard Bengali Unicode UTF-8.
"""

import re
import unicodedata
from typing import Dict, Any, Optional

# Mapping of composite glyph codes (from VOXLMY+Bangla, SQDAUS+Bangla, and similar fonts) to Unicode Bengali
LIGATURE_MAP: Dict[str, str] = {
    # Key location & name conjuncts
    'ÿ': 'ট্ট',   # চট্টগ্রাম, ভট্টাচার্য, পট্টি, কুট্টি
    'Ô': 'ক্স',   # কক্সবাজার, রিক্সা, বক্স, এপেক্স
    'Ö': 'ক্স',   # অ্যানেক্স
    'Ñ': 'ক্ক',   # আব্বাস, বক্কর
    'Ò': 'ক্ট',   # ফ্যাক্টরী, প্রজেক্ট, সেক্টর
    'î': 'চ্চ',   # বাচ্চু
    'ï': 'শু',    # শুভ
    'þ': 'ঞ্চ',   # কাঞ্চন
    'ć': 'ন্ড',   # ধানমন্ডি, মন্ডল
    'ě': 'দ্ব',   # দ্বীন, দ্বিজেন
    'ģ': 'ন্থ',   # পান্থপথ, পান্থনিবাস
    'Ħ': 'ন্ধ',   # সন্ধ্যা, জগবন্ধু
    'Ī': 'ন্ব',   # মেনশ্বর
    'Į': 'ন্ত্র',  # মন্ত্রণালয়, সুমন্ত
    'ı': 'প্ল',   # প্লাজা, কমপ্লেক্স, বিপ্লব
    'ĳ': 'প্ন',   # স্বপ্না, স্বপ্নীল
    'ņ': 'ম্র',   # সম্রাট
    'Ł': 'স্ন',   # জ্যোৎস্না, স্নেহা
    'ū': 'স্ন',   # জ্যোৎস্না
    'Ŭ': 'প্ট',   # কনসেপ্ট, দীপ্তি
    'ů': 'স্ম',   # স্মৃতি
    'Ƃ': 'রু',   # ফারুক, রূপালী
    'Ǝ': 'স্ত',   # রুস্তম, মস্তুরা
    'Ə': 'ন্দু',  # কেন্দুয়া, চান্দু
    'á': 'গ্ন',   # সংলগ্ন
    'ã': 'গ্ল',   # গ্লাস, গ্লোরিয়া
    'ê': 'ঙ্গ',   # জাহাঙ্গীর
    'Đ': 'ত্ন',   # রত্না
    'Ě': 'দ্ম',   # পদ্মাবতী
    'Ŝ': 'ষ্ক',   # পরিষ্কার
    'ş': 'ষ্ঠ',   # ষষ্ঠ, শর্মিষ্ঠা
    'Ŏ': 'ল্গ',   # ফাল্গুনী
    'Ā': 'ট্র',   # সেন্ট্রাল, ট্র্যাকার
    'ķ': 'ফ্ল',   # ফ্ল্যাট, ফ্রি
    'Ÿ': 'ক্ষ্ম', # লক্ষ্মী, মাহমুদ
    '¢': 'ঞ্জ',   # রঞ্জন, মিনহাজ
    'ù': 'জ্ব',   # উজ্জ্বল, আলহাজ্ব
    'ú': 'জ্ব',   # আলহাজ্ব
    'Ľ': 'ব্র',   # ইব্রাহীম
    'ľ': 'ব্ল',   # ব্লক, পিডব্লিউডি
    'Ģ': 'ন্ত',   # চূড়ান্ত, কান্ত
    'Ĵ': 'প্র',   # প্রকাশ, প্রিয়া
    'û': 'ঞ্চ',   # অঞ্চল
    'Œ': 'ন্',   # ধানমন্ডি
    'Ù': 'ক্ষ',   # দক্ষিণ
    'Ë': '্য',   # ব্যবসা, মধ্য
    'ń': 'ম্ব',   # নম্বর
    'Ň': 'ম্ম',   # মোহাম্মদ
    '×': 'ক্ত',   # মুক্তি, আক্তার
    'į': 'ন্য',   # জন্য
    'Ş': 'স্ট',   # পোস্টকোড, স্টাফ
    'ƀ': 'সু',   # সুন্দর, সুকান্ত
    'ĥ': 'ন্ম',   # জন্ম
    'Ō': 'ল্ল',   # মল্লিক, উল্লাহ
    'ĺ': 'ব্দ',   # আব্দুল
    'ƣ': 'কু',   # কুমার, কুষ্টিয়া
    'ė': 'দ্দ',   # উদ্দিন
    'ă': 'ড্র',   # ড্রাইভার
    'Ĩ': 'ন্ন',   # আক্তারুন্নাহার, পান্না
    'š': 'ষ্প',   # পুষ্প
    'Ĕ': 'ত্র',   # ত্রিপুরা
    'ĩ': 'ন্স',   # ফ্রান্স
    'ƃ': 'দু',   # দুলাল, দুগ্ধ
    'õ': 'জ্জ',   # আখতারুজ্জামান
    'ħ': 'ঞ্চ',   # চঞ্চল, কাঞ্চন
    'Ĥ': 'ন্দ',   # আনন্দ, সুন্দর, গোবিন্দ
    'Ř': 'শ্র',   # শ্রী
    'ś': 'শ্ব',   # বিশ্বাস
    'Ũ': 'স্ট',   # স্টাফ
    'ļ': 'ব্ব',   # আব্দুল জব্বার
    'Ƅ': 'ত্র',   # ছাত্র, চিত্র
    'Ø': 'ক্র',   # ক্রিসেন্ট, মাইক্রো
    'ē': 'ত্ত',   # উত্তর, দত্ত
    'ø': 'জ্ঞ',   # প্রজ্ঞা, জ্ঞান
    'Ŕ': 'শ্চ',   # পশ্চিম
    'Ů': 'স্ব',   # স্বাধীন, সরস্বতী
    'ŝ': 'ষ্ণ',   # কৃষ্ণ
    'Ž': 'গু',   # গুলশান, গুলজার
    'Ɓ': 'রু',   # পুরুষ
    'ſ': 'নু',   # ইউনুস
    'Ă': 'ড্ড',   # বাড্ডা
    'ŋ': 'ঙ্ক',   # শংকর
    'ř': 'শ্য',   # শ্যাম, শ্যামল
    'Ɔ': 'হু',   # হুজুর
    'ũ': 'স্ত',   # রাস্তা, ওস্তাদ
    'ĸ': 'ফ্ল',   # ফ্ল্যাট
    'ƅ': 'হৃ',   # হৃদয়
    'ý': 'ঞ্জ',   # রঞ্জন, সঞ্জয়
    'Ŷ': 'ষ্ঠ',   # জ্যেষ্ঠ
    'å': 'গ্র',   # গ্রীনরোড
    'İ': 'প্ত',   # সুপ্ত
    'Ő': 'ল্প',   # কল্পনা, শিল্পী
    'ę': 'চ্ছ',   # ইচ্ছা
    'Ŧ': 'ত্র',   # ছাত্র
    'Ô': 'ক্স',   # কক্সবাজার
    'ŏ': 'ল্ড',   # বিল্ডিং, হোল্ডিং
    'ĉ': 'ন্ন',   # নুরুন্নাহার
    'Ū': 'স্থ',   # কবরস্থান
    '\x8f': 'উ',  # উড়াইকাদি
    '\x8a': 'দ',  # জাবেদ আলী, আহাদ উল্লা, বাঁশদহ (138)
    '\x8b': 'ধ্', # মধ্য পাড়া, মধ্য খনজনমারা (139)
    '\x8c': 'ন্', # ধানমন্ডি
    '\x8e': '',
    '\x91': 'শ্', # পশ্চিম (145)
    '\x92': '্য',  # সূর্য (146)
    '\x95': 'ন্', # মিন্টু (149)
    '°': '',
    'ł': 'ল',
    'ƞ': 'ন্দ',
    'ű': 'স্ট',
    '¨': 'স',   # সামস উদ্দিন, আব্দুস ছামাদ
    'Ţ': 'ন্ত',
    'Ŵ': 'ণ্ড',
    'ž': 'হ্',
    'Ĳ': 'গ্চ',
    'Â': 'য়',   # আনোয়ার, সোলায়মান, হৃদয়, মিয়ার
    'è': 'এ',
    'ż': 'ঝ',
    'Ű': 'স্র',   # ইস্রাফিল, এস্রাব (368)
    'Ƥ': 'ফু',   # ফুলবাসী (420)
    'Ì': '্ল',   # সোনাউল্লাহ (204)
    'Ú': 'ন্ঠ',   # (218)
    'Ý': 'ন্স',   # (221)
    'Þ': 'প্ট',   # (222)
    'à': 'প্প',   # (224)
    'ü': 'ঞ্ছ',   # বাঞ্ছার চর, পঞ্ছু ভানু (252)
    'µ': 'ড়',   # বাড়ি, খানপাড়া, উত্তর পাড়া (181)
    '¤': 'ম্',   # (164)
    '¥': 'ল্',   # রাশিদুল ইসলাম (165)
    '¡': '্ব',   # (161)
    'Û': 'ক্ষ্ম',  # লক্ষ্মীপুর (219)
    'Š': 'ৗ',   # (352)
    'Ĝ': 'দ্ধ',   # বুদ্ধি (284)
    'ŗ': 'ভ্র',   # কাভেরী (343)
    'ź': 'হ্ব',   # মাহবুবুর (378)
    'Ė': 'থ্ব',   # পৃথ্বী (278)
    'ō': 'স্ত্র',  # মিস্ত্রী (333)
    'Ķ': 'প্স',   # অপ্সরা (310)
    '\x87': 'ন্', # উপেন্দ্র (135)
    '\x9b': 'য়',  # জয়নাল (155)
    '\ufffe': '', # separator (65534)
}

# Regex pattern matching any valid Bengali consonant or consonant cluster (with optional nukta and hasant)
BENGALI_CLUSTER_PATTERN = r'[\u0985-\u09B9\u09CE\u09DC-\u09DF]\u09BC?(?:্[\u0985-\u09B9\u09DC-\u09DF]\u09BC?)*'
BENGALI_CLUSTER_RE = re.compile(BENGALI_CLUSTER_PATTERN)

# Common word corrections for legacy PDF font anomalies
WORD_FIXES: Dict[str, str] = {
    'কের্পােরশন': 'কর্পোরেশন',
    'কের্পোরেশন': 'কর্পোরেশন',
    'কের্পারেশন': 'কর্পোরেশন',
    'পোস্টেকাড': 'পোস্টকোড',
    'উপেজলা': 'উপজেলা',
    'পরিসেদর': 'পরিষদের',
    'ফেরেদৗস': 'ফেরদৌস',
    'ফেরেদৌস': 'ফেরদৌস',
    'হোেসন': 'হোসেন',
    'বাদ্ধা': 'বাড্ডা',
    'বাধ্বা': 'বাড্ডা',
    'ফ্ফলশান': 'গুলশান',
    'ফ্গুলশান': 'গুলশান',
    'সেকাল্টারবাগ': 'সেকান্দারবাগ',
    'সেকাল্টার': 'সেকান্দার',
    'ট্যান্টানারী': 'ট্যানারী',
    'ট্যান্টানারি': 'ট্যানারি',
    'ল্ডক': 'ব্লক',
    'ব্যান্টবসা': 'ব্যবসা',
    'খল্টকার': 'খন্দকার',
    'ব্যান্টাংক': 'ব্যাংক',
    'বিক্টিং': 'বিল্ডিং',
    'শ্রিসেন্ট': 'ক্রিসেন্ট',
    'উেম্ম': 'উম্মে',
    'আেমনা': 'আমেনা',
    'আেয়শা': 'আয়েশা',
    'আফেরাজা': 'আফরোজা',
    'মো◌্হাম্মদ': 'মোহাম্মদ',
    'মো্হাম্মদ': 'মোহাম্মদ',
    'সন্ধা': 'সন্ধ্যা',
    'চযগ্রাম': 'চট্টগ্রাম',
    'কব্রবাজার': 'কক্সবাজার',
    'কভ্রবাজার': 'কক্সবাজার',
    'গুজিরেকানা': 'গুজরিকোনা',
    'নেত্রকানা': 'নেত্রকোনা',
    'ক্যান্টনেমন্ট': 'ক্যান্টনমেন্ট',
}


def decode_bangla_pdf_text(text: str) -> str:
    """
    Decodes raw text extracted from Bengali PDFs into clean, well-formed Unicode Bengali.
    Handles visual glyph positioning, pre-base vowels, and legacy ligatures.
    """
    if not text:
        return ""

    # Step 1: Normalize newlines & remove null bytes
    text = text.replace('\r\n', '\n').replace('\r', '\n').replace('\x00', '')

    # Step 2: Replace known font composite ligatures
    for glyph, replacement in LIGATURE_MAP.items():
        if glyph in text:
            text = text.replace(glyph, replacement)

    # Step 3: Reph conversion
    # Consonant cluster followed by Î (reph symbol) -> র্ + cluster
    # e.g., প + Î -> র্প, ড + Î -> র্ড, ট + Î -> র্ট
    text = re.sub(rf'({BENGALI_CLUSTER_PATTERN})Î', r'র্\1', text)
    text = text.replace('Î', 'র্')

    # Step 4: Oi-kar prefix conversion (Ð)
    # Ð followed by consonant cluster -> cluster + ৈ
    # e.g., Ðতয়ব -> তৈয়ব, Ðসয়দ -> সৈয়দ
    text = re.sub(rf'Ð({BENGALI_CLUSTER_PATTERN})', r'\1ৈ', text)
    text = text.replace('Ð', 'ৈ')

    # Step 5: o-kar (Ï + cluster + া -> cluster + ো)
    # e.g., Ïভাটার -> ভোটার, Ïরাড -> রোড, Ïমাঃ -> মোঃ
    text = re.sub(rf'Ï({BENGALI_CLUSTER_PATTERN})া', r'\1ো', text)

    # Step 6: au-kar (Ï + cluster + ৗ -> cluster + ৌ)
    # e.g., Ïপৗরসভা -> পৌরসভা, Ïচৗধুরী -> চৌধুরী, Ïতৗিহদ -> তৌহিদ
    text = re.sub(rf'Ï({BENGALI_CLUSTER_PATTERN})ৗ', r'\1ৌ', text)

    # Step 7: e-kar (Ï + cluster -> cluster + ে)
    # Avoid duplicate if cluster already ends with e-kar
    def _repl_e(m):
        c = m.group(1)
        if 'ে' in c:
            return c
        return c + 'ে'

    text = re.sub(rf'Ï({BENGALI_CLUSTER_PATTERN})', _repl_e, text)
    text = text.replace('Ï', '')

    # Step 8: i-kar visual swap (ি precedes consonant in visual encoding, swap to follow)
    # e.g., িঠকানা -> ঠিকানা, তািলকা -> তালিকা, মিহলা -> মহিলা
    text = re.sub(rf'ি({BENGALI_CLUSTER_PATTERN})', r'\1ি', text)

    # Step 8b: Handle visual bare e-kar + aa-kar -> o-kar, e-kar + au-kar -> ou-kar
    # Only if e-kar is not preceded by a consonant (to avoid turning রেহানা into রহোনা)
    text = re.sub(rf'(^|[^\u0995-\u09B9\u09CE\u09DC-\u09DF\u09CD])ে({BENGALI_CLUSTER_PATTERN})া', r'\1\2ো', text)
    text = re.sub(rf'(^|[^\u0995-\u09B9\u09CE\u09DC-\u09DF\u09CD])ে({BENGALI_CLUSTER_PATTERN})ৗ', r'\1\2ৌ', text)

    # Step 8c: Handle visual bare e-kar typed before consonant
    # e.g., খােলক (খ + া + ে + ল + ক) -> খালেক, আেমনা -> আমেনা, উেম্ম -> উম্মে
    text = re.sub(rf'([^\u0995-\u09B9\u09CE\u09DC-\u09DF\u09CD]|^)ে({BENGALI_CLUSTER_PATTERN})', r'\1\2ে', text)

    # Step 9: Clean up adjacent/duplicate vowel anomalies caused by multi-glyph sequences
    # Fix 'োেস' -> 'োসে' (where e-kar followed an o-kar cluster like হোেসন -> হোসেন)
    text = re.sub(r'োে([ক-হ])', r'ো\1ে', text)
    # Fix double e-kar or double vowels
    text = re.sub(r'ে+', 'ে', text)
    text = re.sub(r'ি+', 'ি', text)
    text = re.sub(r'া+', 'া', text)
    text = re.sub(r'ো+', 'ো', text)
    text = re.sub(r'ু+', 'ু', text)
    text = re.sub(r'ূ+', 'ূ', text)

    # Step 9b: Remove dotted circle placeholders and invalid combining marks
    text = text.replace('\u25cc', '')
    # Remove invalid hasants directly following dependent vowel signs (e.g. ো্হ -> োহ in মো◌্হাম্মদ)
    text = re.sub(r'([\u09BE-\u09CC])্+', r'\1', text)

    # Step 10: Apply word-level dictionary fixes
    for k, v in WORD_FIXES.items():
        text = text.replace(k, v)

    # Step 11: Standard Unicode NFC normalization
    text = unicodedata.normalize('NFC', text)

    # Step 11b: Fix ordering of modifier characters (Chandrabindu, Anusvara, Visarga)
    # If typed before a dependent vowel sign in the raw PDF, swap them to logical order
    # e.g. দঁাত -> দাঁত (দ + া + ঁ)
    text = re.sub(r'([ঁংঃ])([ািীুূৃেৈোৌ])', r'\2\1', text)

    # Step 11c: Canonical Nukta composition to standard precomposed Bengali letters
    # Standard Unicode NFC does NOT compose Bengali letters with Nukta (U+09BC)
    # \u09af + \u09bc -> য় (U+09DF), \u09a1 + \u09bc -> ড় (U+09DC), \u09a2 + \u09bc -> ঢ় (U+09DD)
    text = text.replace('\u09af\u09bc', 'য়').replace('\u09a1\u09bc', 'ড়').replace('\u09a2\u09bc', 'ঢ়')

    # Step 12: Clean multiple consecutive spaces (preserving newlines)
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()


# Backward-compatible alias
decode_bengali_text = decode_bangla_pdf_text


def decode_record_dict(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decodes all textual values in a customer/voter record dictionary.
    Leaves non-string values intact.
    """
    decoded = {}
    for k, v in record.items():
        if isinstance(v, str):
            decoded[k] = decode_bangla_pdf_text(v)
        else:
            decoded[k] = v
    return decoded
