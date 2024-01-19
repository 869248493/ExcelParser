import win32clipboard
import win32con
from io import BytesIO
from PIL import Image, ImageGrab

def getClipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(win32con.CF_HDROP)
    print(data)

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()
    win32.For
def grab():
    im = ImageGrab.grabclipboard()
    print(im)
    im.save('somefile.png', 'PNG')

def getTheClipboardType():
    formats = []
    win32clipboard.OpenClipboard()
    lastFormat = 0
    while True:
        nextFormat = win32clipboard.EnumClipboardFormats(lastFormat)
        if 0 == nextFormat:
             # all done -- get out of the loop
             break
        else:
             formats.append(nextFormat)
             lastFormat = nextFormat
    win32clipboard.CloseClipboard()
    return formats

if __name__ == '__main__':

    # win32clipboard.RegisterClipboardFormat()
    # print(getTheClipboardType())
    send_to_clipboard([1, 50006], ["abcd", r"""<QQRichEditFormat><EditElement type="0" pasteType="2"><![CDATA[this is a test sentence ]]></EditElement><EditElement type="2" shortcut="/:sun" filepath="" /></QQRichEditFormat>"""])
