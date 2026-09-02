"""
placeholder_spec.py — canonical grammar of NON-TRANSLATABLE tokens.

Every token matched here MUST appear, byte-for-byte and in the same multiset,
in both the source string and its Arabic translation. The QA validator
(40_qa_validate.py) uses extract_tokens() to enforce that.

Covers the token families seen in Unreal Engine games (and named in the brief):
  - printf:        %s %d %i %u %f %x  and positional  %1$s %2$d  and width %.2f %03d
  - ICU/UE args:   {0} {1} {PlayerName} {Count}            (also UE FText format args)
  - UE rich text:  <RichTextStyle>...</>  <color=...>...</>  closing </>  self <img .../>
  - C# style:      {0} already covered; also {{ }} literal-brace escapes
  - shell/UE vars: $name  ${name}
  - escapes:       \n \r \t \\  and literal CR/LF kept verbatim
  - bracket refs:  [item] [PAD_A] style hard tokens used by some HD-2D titles

If you discover an Elliot-specific token during extraction, ADD it here and
re-run QA — do not special-case it in a translation.
"""
import re

# Order matters: longer / more specific patterns first so they win the scan.
TOKEN_PATTERNS = [
    ("rich_close",   r"</>"),                                  # UE rich-text close
    ("rich_open",    r"<[A-Za-z][^<>]*?>"),                    # <Bold> <color=#fff> <img id=x/>
    ("printf_pos",   r"%\d+\$[ -+0#]?\d*(?:\.\d+)?[bcdeEfgGiosuxX]"),  # %1$s
    ("printf",       r"%[ -+0#]?\d*(?:\.\d+)?[bcdeEfgGiosuxX]"),       # %s %d %.2f %03d
    ("printf_pct",   r"%%"),                                   # literal percent
    ("icu_named",    r"\{[A-Za-z_][A-Za-z0-9_]*\}"),           # {PlayerName}
    ("icu_index",    r"\{\d+\}"),                              # {0}
    ("brace_var",    r"\$\{[A-Za-z_][A-Za-z0-9_]*\}"),         # ${name}
    ("dollar_var",   r"\$[A-Za-z_][A-Za-z0-9_]*"),             # $name
    ("bracket_tok",  r"\[[A-Z][A-Z0-9_]*\]"),                  # [ITEM] [PAD_A]  (UPPER only, to avoid prose)
    ("escape",       r"\\[nrt\\]"),                            # \n \r \t \\
]

_COMPILED = [(name, re.compile(pat)) for name, pat in TOKEN_PATTERNS]


def extract_tokens(text: str):
    """Return the list of non-translatable tokens in order of appearance.

    Non-overlapping scan, longest-specific-first. Returns [] for plain prose.
    """
    if text is None:
        return []
    tokens = []
    i, n = 0, len(text)
    while i < n:
        matched = False
        for name, rx in _COMPILED:
            m = rx.match(text, i)
            if m:
                tokens.append(m.group(0))
                i = m.end()
                matched = True
                break
        if not matched:
            i += 1
    return tokens


def token_multiset(text: str):
    from collections import Counter
    return Counter(extract_tokens(text))


def compare(source: str, target: str):
    """Compare token multisets. Returns dict with missing/added/ok."""
    s, t = token_multiset(source), token_multiset(target)
    missing = list((s - t).elements())   # in source, absent/short in target
    added = list((t - s).elements())     # appeared/extra in target
    # literal CR/LF (not escaped) counts too:
    s_nl = source.count("\n") + source.count("\r")
    t_nl = target.count("\n") + target.count("\r")
    return {
        "ok": not missing and not added and s_nl == t_nl,
        "missing": missing,
        "added": added,
        "literal_newline_delta": t_nl - s_nl,
    }


if __name__ == "__main__":
    # tiny self-test
    src = "Hello {PlayerName}, you dealt %d damage!<color=#ff0000>CRIT</>\nPress [PAD_A]."
    print("tokens:", extract_tokens(src))
    bad = "مرحبًا، لقد سببت ضررًا!"  # drops every token
    print("compare:", compare(src, bad))
