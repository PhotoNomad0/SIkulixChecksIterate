from sikuli.Sikuli import *
import checkIterateMain as CHK
import time
import sys
import java.awt.Robot as JRobot
from java.awt import Color
myRobot = JRobot()
start = time.time()

# run with:
#java -jar %HOMEPATH%\Development\SikulixIDE\sikulixide-2.0.5.jar -c -r %HOMEPATH%\Development\SikulixTesting\SIkulixChecksIterate.sikuli

# Region(370,205,798,430)

tn = "images/tnLabel.png"
region = Region(939,566,202,45)

#launchButton = Pattern("launchButton.png").targetOffset(-465,-267)
#partialChecked = Pattern("partialChecked.png").similar(0.92)

blueButton = Region(950,585,1,1)
whiteButton = Region(750,579,33,14)

color = CHK.getColorRGB(blueButton)
print "Blue color ", color, "at", blueButton
print(format(color, '#x'))

blue = CHK.blueColor 
print "blue= ", blue
print "equals ", color == blue
#print type(color)

#print "RGB ", color.getRGB()

color = CHK.getColorRGB(whiteButton)
print "White color ", color, "at", whiteButton
print(format(color, '#x'))
print "white equals ", color == CHK.whiteColor

print("Using Jython version ", sys.version)
# 2.7.2 (v2.7.2:925a3cc3b49d, Mar 21 2020, 10:12:24)
# [OpenJDK 64-Bit Server VM (Microsoft)]

opts = OCR.Options()
print opts
#OCR.Options:
#data = null
#language(eng) oem(3) psm(3) height(15.1) factor(1.99) dpi(120) 
#variables: user_defined_dpi:300

# exit()

#launchButton = checkIterateMain.getFirstLaunchButton()

results = CHK.checkOpenProject('en')
print "results = ", results
print "Total run time= ", checkIterateMain.elapsedTime(start)
