from sikuli.Sikuli import *
import checkIterateMain as CHK
import time
import sys
import json
from datetime import datetime
import java.awt.Robot as JRobot
from java.awt import Color
myRobot = JRobot()
start = time.time()

# run with:
#java -jar %HOMEPATH%\Development\SikulixIDE\sikulixide-2.0.5.jar -c -r %HOMEPATH%\Development\SikulixTesting\SIkulixChecksIterate.sikuli     

partialChecked = Pattern("partialChecked.png").similar(0.92)
fullyChecked = Pattern("fullyChecked.png").similar(0.92)
unchecked = "unchecked.png"

# langID = 'hi'
# launchButton_ = CHK.getFirstLaunchButtonInfo()
# print launchButton_
# CHK.selectGL(langID, launchButton_)
# exit()

bottomScroll = "bottomScroll.png"
menuIcon = Pattern("menuIcon.png").similar(0.80)


# matches  ['en_ult_1co_book', 'en_ult_2co_book', 'en_ult_act_book', 'en_ult_est_book', 'en_ult_exo_book', 'en_ult_heb_book', 'en_ult_jdg_book', 'en_ult_jhn_book', 'en_ult_jos_book', 'en_ult_luk_book', 'en_ult_mat_book', 'en_ult_mrk_book', 'en_ult_php_book', 'en_ult_rom_book', 'en_ult_rut_book']
checkProjects = [ 'en_ult_mrk_book', 'en_ult_php_book', 'en_ult_rom_book', 'en_ult_rut_book']
matchProject = '_ult_'
langID = 'en'
startAtTop = True
results = CHK.doProjects(matchProject, langID, startAtTop, checkProjects)
print "results = ", results
print "Total run time= ", CHK.elapsedTime(start)

exit()

# color0 = Color(110, 110, 110).getRGB()
# color1 = Color(121, 121, 121).getRGB()

# print CHK.colorDiff(color0, color1)
# 1.42352941176

color = 0xFFFFFFFFFF737373
print color

# color = CHK.getColorRGB(blueButton)
# print "Blue color ", color, "at", blueButton
# print(format(color, '#x'))

# blue = CHK.blueColor 
# print "blue= ", blue
# print "equals ", color == blue
# #print type(color)

# #print "RGB ", color.getRGB()

# color = CHK.getColorRGB(whiteButton)
# print "White color ", color, "at", whiteButton
# print(format(color, '#x'))
# print "white equals ", color == CHK.whiteColor

print("Using Jython version ", sys.version)
# 2.7.2 (v2.7.2:925a3cc3b49d, Mar 21 2020, 10:12:24)
# [OpenJDK 64-Bit Server VM (Microsoft)]

opts = OCR.Options()
print opts
#OCR.Options:
#data = null
#language(eng) oem(3) psm(3) height(15.1) factor(1.99) dpi(120) 
#variables: user_defined_dpi:300

# CHK.respondToAlerts()
# exit()

#launchButton = checkIterateMain.getFirstLaunchButton()


results = CHK.checkOpenProject('en')
print "results = ", results
print "Total run time= ", CHK.elapsedTime(start)

