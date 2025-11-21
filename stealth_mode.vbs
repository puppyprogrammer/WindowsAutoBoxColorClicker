Set WshShell = CreateObject("WScript.Shell")
' Run pythonw (windowless python) with main.py, hidden (0), don't wait (False)
WshShell.Run "pythonw main.py", 0, False
Set WshShell = Nothing
