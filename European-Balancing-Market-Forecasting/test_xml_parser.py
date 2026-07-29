import sys
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve()

sys.path.append(
    str(BASE_DIR)
)



from src.data_loader.xml_price_parser import XMLPriceParser



# ============================================================
# TEST XML FILE
# ============================================================

xml_file = Path(
    "data/raw/italy/prices/prices_2020.xml"
)



if not xml_file.exists():

    print(
        "XML file not found:"
    )

    print(
        xml_file
    )

    exit()



# ============================================================
# READ XML
# ============================================================

with open(
    xml_file,
    "rb"
) as f:

    xml_content = f.read()



# ============================================================
# PARSE
# ============================================================

parser = XMLPriceParser(
    xml_content
)


df = parser.parse()



print("\n")
print("="*60)
print("XML PARSER TEST")
print("="*60)



print(
    df.head()
)


print()


print(
    df.tail()
)


print()


print(
    df.info()
)


print()


print(
    "Rows:",
    len(df)
)


print(
    "Start:",
    df["timestamp"].min()
)


print(
    "End:",
    df["timestamp"].max()
)