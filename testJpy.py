import sys
sys.path.append('lib.win32-2.7')
import jpy

File = jpy.get_type('java.io.File')

file = File('test/it')
name = file.getName()