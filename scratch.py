import re

expression = r"\b(?:(?:3[01]|[12][0-9]|0?[1-9])[/.-](?:1[0-2]|0?[1-9])[/.-][0-9]{4}|(?:3[01]|[12][0-9]|0?[1-9])-(?:1[0-2]|0?[1-9])-[0-9]{4}|(?:3[01]|[12][0-9]|0?[1-9])[\t ]+(?:Jan|Januari|Feb|Februari|Mar|Maret|Apr|April|Mei|Mei|Jun|Juni|Jul|Juli|Aug|Agustus|Sep|September|Oct|Oktober|Nov|November|Dec|Desember)|(?:2[0-3]|1?[0-9])[\t ]+(?:Jan|January|Feb|February|Mar|March|Apr|April|May|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December)|(?:1[0-2]|[1-9])[/.-](?:1[0-2]|[1-9]))\b"

raw_date = "Kamis (9/12)"
import pdb; pdb.set_trace()