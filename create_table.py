import sys
import importlib

name = sys.argv[1]
module = importlib.import_module('ServerSide.DBClasses.'+name)
class_ = getattr(module, name)
class_.create_table()