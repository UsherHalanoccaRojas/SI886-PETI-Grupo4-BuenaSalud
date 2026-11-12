"""Actualiza el indice y exporta a PDF con LibreOffice (UNO). Uso: python3 export_pdf.py archivo.docx"""
import subprocess, time, sys, os, uno
from com.sun.star.beans import PropertyValue
src = os.path.abspath(sys.argv[1]); pdf = src[:-5]+".pdf"
pr = subprocess.Popen(["soffice","--headless","--norestore","--accept=socket,host=localhost,port=2002;urp;"])
ctx=None
for _ in range(40):
    try:
        lc = uno.getComponentContext(); res = lc.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",lc)
        ctx = res.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"); break
    except Exception: time.sleep(1)
desk = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop",ctx)
pv = lambda n,v: PropertyValue(Name=n,Value=v)
doc = desk.loadComponentFromURL(uno.systemPathToFileUrl(src),"_blank",0,(pv("Hidden",True),))
idx = doc.getDocumentIndexes()
for i in range(idx.getCount()): idx.getByIndex(i).update()
doc.storeToURL(uno.systemPathToFileUrl(pdf),(pv("FilterName","writer_pdf_Export"),))
doc.close(True); 
try: desk.terminate()
except Exception: pass
pr.wait(timeout=20); print("pdf:",pdf)
