from __future__ import annotations

import textwrap

class TextUtils:
    @classmethod
    def dedent(cls, text: str | None) -> str:
        if text is None:
            return ""

        return textwrap.dedent(text)[1:-1]
