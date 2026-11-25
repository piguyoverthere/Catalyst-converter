# [dev]
import os
import tree_sitter_java as tsjava
from tree_sitter import Language, Parser

JAVA_LANGUAGE = Language(tsjava.language())
parser = Parser(JAVA_LANGUAGE)

def read_all_files(root_dir, encoding="utf-8"):
    file_contents = {}

    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            full_path = os.path.join(root, filename)
            try:
                with open(full_path, "r", encoding=encoding) as f:
                    file_contents[full_path] = f.read()
            except (UnicodeDecodeError, OSError) as e:
                print(f"Skipping {full_path}: {e}")

    return file_contents

with open("MyClass.java", "rb") as f:
    code = f.read()

tree = parser.parse(code)

# Query for class declarations and their superclass
query = JAVA_LANGUAGE.query("""
(class_declaration
  name: (identifier) @class_name
  (superclass (type_identifier) @superclass_name))
""")

captures = query.captures(tree.root_node)

# Extract the superclass name
if "superclass_name" in captures:
    for node in captures["superclass_name"]:
        print("Extends:", node.text.decode("utf-8"))
else:
    print("Extends: Object (implicit)")
