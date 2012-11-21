; Match any substring of the title
AutoItSetOption ( "WinTitleMatchMode", 2 )
While 1
   WinWait("copy-me-to-clerk-soft")
   ; Ctrl+c
   Send("^c")
   ; Ctrl+w
   Send("^w")
   ;; Alt+tab
   ;Send("!{TAB}")
   WinActivate("Granicus")
   ; Ctrl+v
   Send("^v")
WEnd