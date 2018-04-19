# sign_handler.py

from pyledsign.minisign import MiniSign
from simplefont import sign_font
import os, time
import serialfind

portname = serialfind.serialfind()

# LED DISPLAY 2 LINES AS 8-PIXEL RENDERED FONTS
def WriteFont(lines, effect, speed):
    # prepare the bitmap
    class Array:
        def zero_one(self, data):
            zero_oned = ""
            for row in data:
                joined_row = "".join("{0}".format(n) for n in row)
                zero_oned += joined_row
            return zero_oned

    # font setup
    pwd = os.path.dirname(os.path.realpath(__file__))
    new_glyphs_path = '/'.join([pwd, 'fonts'])
    font = sign_font(new_glyphs_path)

    # sign setup
    portname = serialfind.serialfind()
    sign = MiniSign(devicetype='sign', port=portname, )

    # THIS IS BREAKING WHEN THE TEXT IS TOO LONG
    # render message as bitmap 
    matrix = font.render_multiline(lines, 16 / 2, {"ignore_shift_h": True, "fixed_width": 96})

    if not matrix:
        return False
    text_for_sign = Array().zero_one(matrix)
    typeset = sign.queuepix(height=len(matrix), width=len(matrix[0]), data=text_for_sign);



    # queue and send message
    sign.queuemsg(data="%s" % typeset, effect='hold');
    sign.sendqueue(device=portname)

    # pause and report
    time.sleep(6)

