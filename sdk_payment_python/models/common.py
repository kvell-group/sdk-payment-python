from __future__ import annotations

import dataclasses


class KvellModel:
    @classmethod
    def from_dict(cls, data: dict) -> KvellModel:
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})
