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
            
# exit()

tn = "images/tnLabel.png"

projectsButton = Region(694,47,159,33)
toolButton = Region(1093,46,77,38)

matchProject = '_ult_'
langID = 'en'
def doProjects(matchProject, langID):
    langID = input ("Enter Language (empty for no preference).\nTo begin, Open Project to tools page or launch tNotes or tWords.\nDo CTRL-F12 to abort or CTRL-F11 for options.\nAre you ready to start?", langID)

    title = CHK.getPopupText(CHK.projectsTitleArea, 0.5)["text"]
    results = None

    if len(title):
        results = {}
        print "On Projects page"
        matches = CHK.findProjects(matchProject)
        print "matches ", matches

        for project in matches:
            # choice = popAsk ("Do you want to search for "+project+"?")
            # if not choice:
            #     break

            menuIcon = CHK.findProject(project)
            print project, ", menuIcon=", menuIcon

            if menuIcon:
                print "Found Project ", project
                selectButtonSearchRange = CHK.getSearchRangeForSelectButton(menuIcon)
                foundButton = CHK.findFirstImage(selectButtonSearchRange, CHK.selectButton)
                if foundButton:

                    colorArea = Region(foundButton.x + 15, foundButton.y + 15, 1, 1)
                    colorArea.highlight()
                    sleep(1)
                    colorArea.highlightOff()
                    color, colorStr = CHK.getColorAt(colorArea)
                    print "Color found:", colorStr, color

                    # choice = popAsk ("button has color " + str(color) + colorStr + ", continue?")
                    # if not choice:
                    #     return None

                    if colorStr == "disabledButtonColor":
                        click(toolButton) # already selected, so just click on tools
                    else:
                        click(foundButton)

                    toolsOpen = False

                    while not toolsOpen:
                        title_ = CHK.getPopupText(CHK.projectsTitleArea, 0.5)["text"]
                        print "Found title: ", title_
                        if title_ == "Tools":
                            print "On Tools Page"
                            toolsOpen = True

                    # choice = popAsk ("on tools page, continue?")
                    # if not choice:
                    #     return None

                    projectResults = CHK.checkOpenProject(langID, True)
                    results[project] = projectResults

                    click(projectsButton) # go back to projects
                    sleep(1)

                else:
                    print "Could not find select Button"
    
    else:
        print "Not on Projects page"
        results = CHK.checkOpenProject(langID)
    
    choice = popAsk (results)
    return results

results = doProjects(matchProject, langID)
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

