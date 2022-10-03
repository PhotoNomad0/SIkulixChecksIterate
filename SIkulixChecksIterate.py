from sikuli.Sikuli import *
import checkIterateMain

# run with:
#java -jar %HOMEPATH%\Development\SikulixIDE\sikulixide-2.0.5.jar -c -r %HOMEPATH%\Development\SikulixTesting\SIkulixChecksIterate.sikuli


tn = "images/tnLabel.png"
toolName = Region(648,29,115,22)

scrollUp = Location(1241, 188)
scrollDown = Location(1242, 659)

launchButton = "images/launchButton.png"

glBox = Region(834,489,217,24)

toolsArea = Region(686,166,545,533)

# downArrow = "downArrow.png"
# downArrowOffs = Pattern("downArrow.png").targetOffset(41,-1)

glFirstPopup = Region(854,343,215,27)

def getLaunchButtons():
    launches = checkIterateMain.findAllImagesBase(toolsArea, [], launchButton)
    print ("launch buttons found ", len(launches))
    return launches

def getGlTextAreaFromLaunchButton(launchButton):
    glBoxActual = Region(launchButton.x + launchButton.w/2 - 337, launchButton.y + launchButton.h/2 - 2, glBox.w, glBox.h)
    return glBoxActual

def getGlPopupAreaFromLaunchButton(launchButton, pos):
    glBoxActual = Region(launchButton.x + launchButton.w/2 - 337, launchButton.y + launchButton.h/2 + 18*pos - 4, glBox.w + 40, glBox.h)
    return glBoxActual

def getGlPopupText(launchButton, pos):
    region = getGlPopupAreaFromLaunchButton(launchButton, pos)
    region.highlight()
    sleep(2)
    region.highlightOff()
    text = region.text().strip()
    print "At y=", region.y, " found text: '", text, "'"
    return {
        "region": region,
        "text": text,
    }
        
def getFirstLaunchButton():
    launches = getLaunchButtons()
    if (len(launches)):
        button = launches[0]
        return button
    else:
        print ("No launch buttons found")
        return None

def getFirstLaunchButtonInfo():
    launchButton_ = getFirstLaunchButton()
    if launchButton_:
        region = getGlTextAreaFromLaunchButton(launchButton_)
        region.highlight()
        sleep(2)
        region.highlightOff()
        text = region.text().strip()
        print "At y=", region.y, " found text: '", text, "'"
        # click(launchButton_)
        return {
            "launchButton": launchButton_,
            "glTextArea": region,
            "glText": text
        }
    else:
        print "No Launch button found"
        return None

# getFirstLaunchButton()
# exit()

checkTNotesArray = [True, False]
finshed = False
runSIngleCheck = False
print "Startup!"
choice = popAsk ("Are you ready to start?")
if choice:
    for checkTNotes in checkTNotesArray:
        if checkTNotes:
            click(scrollUp)
        else:
            click(scrollDown)
        sleep(2)
        
        results = getFirstLaunchButtonInfo()
        if not results:
            print "Launch button not found, try starting checking"
            runSIngleCheck = True
        else:
            if results["glText"] == 'Select Gateway Language':
                print "No Gl Selected"
                click(results["glTextArea"])
                sleep(1)
                popup = getGlPopupText(results["launchButton"], 0)
                click(popup["region"])
                results = getFirstLaunchButtonInfo()
                
            click(results["launchButton"])
            
        toolNameStr = toolName.text().strip()
        print "Running tool '", toolNameStr, "'"
        
        finshed = checkIterateMain.doChecks()
        if not finshed:
            break
        
        if runSIngleCheck:
            print "Just ran a single check"
            break
        else:
            print "Return to tools card"
            click(toolName)
            sleep(2)

    final = "doChecks finished with " + str(finshed)
    print(final)
    choice = popAsk (final)
else:
    print "Cancelled"