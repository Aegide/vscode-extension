from pydantic import BaseModel


PATH = "src/names.txt"
SCHEMA = "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json"


class Element(BaseModel):
    match: str
    name: str

class Language(BaseModel):
    _schema: str = SCHEMA
    name: str = "JSONT"
    scopeName: str = "source.jsont"
    fileTypes: list[str] = ["jsont"]
    patterns: list[dict[str, str]] = []
    repository: dict[str, Element] = {}


language = Language()


with open(PATH, mode="r", encoding="utf8") as names:
    for line in names.readlines():
        keyword = line[:-1]
        pattern = {"include": f"#{keyword}"}
        language.patterns.append(pattern)
        match_replaced = keyword.replace(".", "_")
        element = Element(
            match=f"{match_replaced}$",
            name=f"{keyword}.jsont"
            )
        language.repository[keyword] = element


printable_json = language.model_dump_json()
print(printable_json.replace("_schema", "$schema"))
