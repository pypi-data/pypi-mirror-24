import sys
from . import install

if sys.argv[1:] == ["install"]:
    install()
else:
    print("""Usage:
python -m raspberryjammod install
""")