from sikuli.Sikuli import *
import checkIterateMain
import time
import sys
start = time.time()

# run with:
#java -jar %HOMEPATH%\Development\SikulixIDE\sikulixide-2.0.5.jar -c -r %HOMEPATH%\Development\SikulixTesting\SIkulixChecksIterate.sikuli

# Region(370,205,798,430)

tn = "images/tnLabel.png"
#launchButton = Pattern("launchButton.png").targetOffset(-465,-267)
#partialChecked = Pattern("partialChecked.png").similar(0.92)

print(sys.version)

#launchButton = checkIterateMain.getFirstLaunchButton()

results = checkIterateMain.checkOpenProject('hi')
print "results = ", results
print "Total run time= ", checkIterateMain.elapsedTime(start)
