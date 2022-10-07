################################
# iterates through all of checks starting with current location
# Note: Use control-F12 to abort
# Note: Use control-F11 to toggle pausing

from sikuli.Sikuli import *
import java.awt.Robot as JRobot
from java.awt import Color

import time
#import utils
start = time.time()

################################
# images

action = Pattern("images/Running.png")
bottomScroll = "images/bottomScroll.png"
selectedGroupExpanded = Pattern("images/SelectedGroupExpanded.png").similar(0.83)
selectedGroupCollapsed = Pattern("images/SelectedGroupCollapsed.png").similar(0.83)
deselectedGroupCollapsed = Pattern("images/deselectedGroupCollapsed.png").similar(0.83)
unselectedDivider = Pattern("images/unselectedDivider.png").similar(0.74)
beforeSelectedDivider = "images/beforeSelectedDivider.png"
afterSelectedDivider = "images/afterSelectedDivider.png"
alertDialog = Pattern("images/alertDialog.png").similar(0.58)
projectFolder = "images/projectFolder.png"
launchButton = Pattern("images/launchButton.png").similar(0.86)
unchecked = "images/unchecked.png"
partialChecked = Pattern("images/partialChecked.png").similar(0.92)
continueButton = "images/continueButton.png"
okButton = "images/okButton.png"
ignoreButton = "images/ignore.png"

################################
# initial config

Settings.MouseMoveDelay = 0
pauseAtEachIteration = False
bottomScrollWidth = 9
bottomScrollHeight = 9
togglesXOffset = -465
togglesYOffset = -267
scrollBarRegion = Region(241,54,8,758)
bottomScrollRegion = Region(scrollBarRegion.x-1, scrollBarRegion.y+scrollBarRegion.h-bottomScrollHeight+8,bottomScrollWidth+2,bottomScrollHeight+2)
alertDialogRegion = Region(366,193,805,450)
actionsRegion = Region(765,13,769,50)
headerArea = Region(0,28,1536,79)
scrollUp = Location(1241, 188)
scrollDown = Location(1242, 659)
glBox = Region(834,489,217,24)
toolsArea = Region(686,166,545,533)
glFirstPopup = Region(854,343,215,27)
projectNameArea = Region(735,53,186,22)
toolName = Region(648,29,115,22)
mouseOffMenu = Region(800,200,1,1)
blueColor = Color(25, 87, 158).getRGB()
whiteColor = Color(255, 255, 255).getRGB()
checkSelectedColor = Color(33,150,243).getRGB()
checkDeselectedColor = Color(116,116,116).getRGB()
groupDeselectedColor = Color(51,51,51).getRGB()
messageRegion = Region(570,308,499,23)
alertRegion = Region(360,186,437,550)
invalidCheckRegion = Region(517,343,598,161)
highLightTime = 0 # set to zero to disable highlighting, otherwise set to how many seconds you want to wait on a highlight
page = 0
running = True
myRobot = JRobot()

config = {
    "validateRunning": action,
    "checkSize": 40,
    "waitForValidate": 0.01,
    "menuRegion": Region(1,106,240,705),
    "scrollBarRegion": scrollBarRegion,
    "scrollBottomRegion": bottomScrollRegion,
    "bottomScrollRegion": bottomScrollRegion,
}

################################
# program

def runHotkey (event) :
    global running
    print "Hot key abort"
    running = False

Env.addHotkey(Key.F12, KeyModifier.CTRL, runHotkey)

def runTogglePause (event) :
    global pauseAtEachIteration
    pauseAtEachIteration = not pauseAtEachIteration
    print "Pausing toggled to ", pauseAtEachIteration

Env.addHotkey(Key.F11, KeyModifier.CTRL, runTogglePause)

# print "scrollBarRegion=", scrollBarRegion
# print "bottomScroll = ", bottomScroll
# print "bottomScrollRegion=", bottomScrollRegion

# print 'Running'

# test scroll bottom
#while running:
#    bottomScrollRegion.highlight()
#    sleep(5)
#    bottomScrollRegion.highlightOff()
#    atBottom = not bottomScrollRegion.exists(bottomScroll, 1)
#    status = "atBottom: " + str(atBottom)
#    print status
#    ok = popAsk(status + ", continue?")
#
#    if not ok:        
#        print "Cancelled"
#        exit()

def getRGB(color):
    colorRGB = ~color ^ 0x00FFFFFF
    red = (colorRGB >> 16) & 0xFF
    green = (colorRGB >> 8) & 0xFF
    blue = colorRGB & 0xFF
    return {
        "red": red,
        "green": green,
        "blue": blue
    }

def colorDiff(color0, color1):
    color0_ = getRGB(color0)
    color1_ = getRGB(color1)
    colors = ["red","green","blue"]
    sumSQ = 0
    for key in colors:
        colorA = color0_[key]
        colorB = color1_[key]
        sq = (colorA - colorB)**2
        # print key, " sq= ", sq
        sumSQ = sumSQ + sq
    
    return sumSQ/255.0

def by_y(group):
    return group["match"].y

def by_y_item(item):
    return item.y

def getColor(region):
    p = region.getCenter()
    color = myRobot.getPixelColor(p.x, p.y)
    return color

def getColorRGB(region):
    color = getColor(region)
    rgb = color.getRGB()
    return rgb

def lookupColor(rgb):
    colorOptions = {
        "blueColor": blueColor,
        "whiteColor": whiteColor,
        "checkSelectedColor": checkSelectedColor,
        "checkDeselectedColor": checkDeselectedColor,
        "groupDeselectedColor": groupDeselectedColor
    }

    for key in colorOptions:
        color = colorOptions[key]
        if color == rgb:
            return key

    # try again with some tolerance
    tolerance = 1.5
    for key in colorOptions:
        color = colorOptions[key]
        if colorDiff(color, rgb) < tolerance:
            return key

    return "UNKNOWN: " + str(rgb)
    
def findAllImages(region, groups, image, selected, expanded):
    print "searching for expanded: ", expanded, ", selected ", selected
    region.findAll(image)
    found = region.getLastMatches()
    while found and found.hasNext():
        match = found.next()
#        print "found expanded: ", expanded, ", selected ", selected, " : ", match
        groups.append({
                    "expanded": expanded,
                    "selected": selected,
                    "match": match
                    })
    return groups

def findAllImagesBase(region, groups, image):
    region.findAll(image)
    found = region.getLastMatches()
    while found and found.hasNext():
        match = found.next()
        groups.append(match)
    # print "groups=", len(groups), " found"
    if len(groups):
        groups = sorted(groups, key=by_y_item) # sort keys by y order
    return groups

def findFirstImage(region, image):
    found = findAllImagesBase(region, [], image)
    if len(found):
        found = found[0]
        return found
    return None

def getGroupsFromDisplayedMenu(config):
    region = config["menuRegion"]
    print "Searching for Group Headers"
    deselectedGroups = findAllImages(region, [], deselectedGroupCollapsed, selected = False, expanded = False)
    selectedCollapsed = findAllImages(region, [], selectedGroupCollapsed, selected = True, expanded = False)
    selectedExpanded = findAllImages(region, [], selectedGroupExpanded, selected = True, expanded = True)

    groups = deselectedGroups + selectedCollapsed + selectedExpanded
    groups = sorted(groups, key=by_y) # sort keys by y order
    
    print "found groups = ", len(groups)
    
    for i in range(len(groups)):
        item = groups[i]
        print i, " expanded: ", item["expanded"], " selected: ", item["selected"], ", match: ", item["match"]

    selected = None
    collapsed = False

    if selectedCollapsed and len(selectedCollapsed):
        found = selectedCollapsed[0]
        print "Found selected collapsed: ", found
        selected = found
        collapsed = True
        
    elif selectedExpanded and len(selectedExpanded):
        found = selectedExpanded[0]
        print "Found selected expanded: ", found
        selected = found
        collapsed = False

    return {
            "selected": selected,
            "collapsed": collapsed,
            "groups": groups
            }

def getCheckDivisionsFromDisplayedMenu(region):
    print "Searching for check dividers in region ", region

    checks = findAllImages(region, [], unselectedDivider, selected = False, expanded = False)
    checks = findAllImages(region, checks, beforeSelectedDivider, selected = True, expanded = False)
    checks = findAllImages(region, checks, afterSelectedDivider, selected = True, expanded = True)

    checks = sorted(checks, key=by_y) # sort keys by y order
    
    for i in range(len(checks)):
        item = checks[i]["match"]
        print i, "check boundary: ", item

    return checks

def verifyNotCrashed(config):
    global running
    
    if not running:
        print "Detected that user cancelled"
        return False
            
    waitForValidate = config["waitForValidate"]
    success = False
    sleep(waitForValidate)
    try:
        actionsRegion.wait(action)
    except:
        print "App has crashed"
        success = False
    else:
        success = True
        
    return (success)

def getYforDivider(divider):
    div = divider["match"]
    y = div.y + div.h + 5
    return y

def doCheck(config, y):
    success_ = False
    textArea = Region(32, y - 2, 169, 25)
    doHighLight(textArea)
    text = textArea.text().encode('UTF-8')
    print "At y=", y, " found text: ", text

    # # examine color
    # color, colorStr = getColorAt(textArea)
    # # print "backbground color ", color, " - ", colorStr
    # if ("UNKNOWN" in colorStr):
    #     message = "Unknown color " + colorStr + " for " + str(color)
    #     print message
    #     # colorArea.highlight()
    #     # pauseMsg(message)
    #     # colorArea.highlightOff()

    click(textArea)
    success_ = verifyNotCrashed(config)
    return (success_)

def getColorAt(region):
    colorArea = Region(region.x, region.y, 1, 1)
    color = getColor(colorArea)
    colorStr = lookupColor(color.getRGB())
    return color,colorStr

def doHighLight(region):
    if highLightTime:
        region.highlight()
        sleep(highLightTime)
        region.highlightOff()

def doMouseMoveOff():
    # move mouse off of menu to remove issues with hover text
    mouseMove(mouseOffMenu)
    sleep(0.5)

def iterateGroupSegment(config, state):
    scrollBarRegion = config["scrollBarRegion"]
    checkHeight = config["checkSize"]
    autoScrolled = state["autoScrolled"]
    bottomScrollRegion = config["bottomScrollRegion"]
    print " scrollBarRegion = ", scrollBarRegion
    region = config["menuRegion"]
    print " region = ", region
    startY = region.y + checkHeight * 0.3
    print "startY = ", startY
    doMouseMoveOff()
    startScrollBar = scrollBarRegion.getScreen().capture(scrollBarRegion)
    print " startScrollBar = ", startScrollBar
    y = 0

    selectedY = region.y
    overScrolled = False
    print "FInding selected group"
    foundGroups = getGroupsFromDisplayedMenu(config)
    if (foundGroups["selected"]):
        match = foundGroups["selected"]["match"]
        region_ = Region(37, match.y - 10, 169, 35)
        doHighLight(region_)
        text = region_.text().encode('UTF-8')
        print "Starting at group ", text, " at ", region_
        
        if (foundGroups["collapsed"]):
            print "Expanding selection ", match
            click(match)
            success = verifyNotCrashed(config)
            if not success:
                print "crashed"
            else:
                foundGroups = getGroupsFromDisplayedMenu(config)
        else:
            print "Already expanded"
    
        div = foundGroups["selected"]["match"]
        selectedY = div.y + div.h
        print "Starting check is at ", selectedY
    else:
        print "No Selection found"
        if state["endAtGroup"]:
            print "Seem to have over scrolled"
            overScrolled = True

    scrollBarRegion = config["scrollBarRegion"]
    maxY = region.y + region.h + checkHeight*0.5
    print "maxY = ", maxY
    endAtGroup = None
    
    # find end point of checks
    groups = foundGroups["groups"]
    for group in groups:
        match = group["match"]
        y = match.y
        if y < selectedY:
            print "Skipping check y ", y
        else:
            print "Will end at group y", y
            maxY = y
            print "maxY = ", maxY
            endAtGroup = match
            region_ = Region(30, endAtGroup.y, 169, 30)
            text = region_.text().encode('UTF-8')
            print "Ending at group ", text, " at ", region_
            break
    
    checkHeight = config["checkSize"]
    maxGap = checkHeight * 1.4
    divisions = getCheckDivisionsFromDisplayedMenu(region)

    lastY = 10000
    steps = []
    if selectedY:
        startY = selectedY
    elif overScrolled:
        startY = region.y + checkHeight
        print "Overscrolled, setting startY to ", startY
    else:
        steps.append(region.y)
        startY = getYforDivider( divisions[0])
        print "No selected group, setting startY to ", startY

    print " starting Y ", startY
    for divider in divisions:
        y = getYforDivider(divider)
        
        if y < startY :
            print "skipping low check ", y, ", startY ", startY
            continue

        if y > maxY :
            print "skipping high check ", y, ", maxY ", maxY
            continue
            
        delta = (y - lastY)
        if (delta >= 0) and (delta < 5):
            print "skipping check low delta ", y, ", lastY ", lastY
            continue
        
        while (y - lastY) > maxGap:
            newY = lastY + checkHeight
            steps.append(newY)
            lastY = newY
            print "Filling in missing check at", newY
            
        steps.append(y)
        lastY = y

    lastY = lastY + checkHeight
    
    while lastY < maxY:
        print "Filling in missing end check at ", lastY, ", maxY=", maxY
        steps.append(lastY)
        lastY = lastY + checkHeight
        
    print "Check Y's found: ", steps
    checkFailed = False

    # look ahead for selected check
    skipTo = 0
    for i in range(0, len(steps)-1):
        y = steps[i]
        centerClickY = y + checkHeight * 0.5
        textArea = Region(32, y - 2, 169, 25)
        color, colorStr = getColorAt(textArea)
        # print "Color at y ", y, " is ", colorStr
        if colorStr == "checkSelectedColor":
            print "Found highlighted position at ", y
            skipTo = i
            break

    print "Iterating checks, startY= ", startY, ", selectedY= ", selectedY
    for i in range(0, len(steps)-1):
        y = steps[i]
        if i < skipTo:
            print "Skipping over y ", y

        else:
            centerClickY = y + checkHeight * 0.5
            print "Clicking on y= ", centerClickY
            success = doCheck(config, y)
            if not success:
                checkFailed = True
                break

    autoScrolled = False
    cancelled = False
    finished = False
    scrollbarUnchanged = False
    invalidContent = False

    if running:
        print "At end of iteration"
        doMouseMoveOff()
        sleep(1)
        results = checkForAlerts(True)
        invalidContent = results["type"] == INVALID_CONTENT

        if not invalidContent:
            scrollbarUnchanged = scrollBarRegion.exists(startScrollBar.getFile(), 1)

        if invalidContent:
            print "found Invalid content"

        elif not scrollbarUnchanged:
            print "Scrollbar moved"
            autoScrolled = True
        else:
            print "scrollbarUnchanged = ", scrollbarUnchanged
            if endAtGroup:
                print "Selecting next group = ", endAtGroup
                click(endAtGroup)
            else:
                atBottom = not bottomScrollRegion.exists(bottomScroll, 1)
                print "atBottom: " + str(atBottom)
                if atBottom:
                    print "double check if there is another group at end. Last check at ", y
                    endAtGroup = None
                    for group in groups:
                        match = group["match"]
                        # print "Checking match at ", match.y
                        if match.y > y:
                            endAtGroup = match
                            break

                    if endAtGroup:
                        print "Selecting next group = ", endAtGroup
                        click(endAtGroup)
                    else:
                        print "Finished - Scrolled to bottom"
                        global running
                        running = False
                        finished = True                
                else:
                    scrollClickAt = Region(scrollBarRegion.x, scrollBarRegion.y + scrollBarRegion.h, scrollBarRegion.w, 2)  
                    print "Scrolling down ", scrollClickAt
                    click(scrollClickAt)
    else:
        cancelled = True

    alertDialogShown = False
    if alertDialogRegion.exists(alertDialog):
        print "Alert Dialog is showing!"
        results = checkForAlerts(True)
        if results["type"] == INVALID_CONTENT:
            invalidContent = True
        else:
            print "fail on other dialog"
            alertDialogShown = True
            checkFailed = True

    return {
        "scrollbarUnchanged": scrollbarUnchanged,
        "checkFailed": checkFailed,
        "autoScrolled": autoScrolled,
        "endAtGroup": endAtGroup,
        "cancelled": cancelled,
        "finished": finished,
        "alertDialogShown": alertDialogShown,
        "invalidContent": invalidContent
    }

def pauseMsg(msg):
    print "Pausing for ", msg
    answer = popAsk(msg + ", continue")
    if not answer:
        exit(1)

def doPause():
    global pauseAtEachIteration
    global running
    global highLightTime
    
    if pauseAtEachIteration:
        continuePause = 'Continue with Pausing'
        continueNoPause = 'Continue without Pausing'
        quit = 'Abort testing'
        noHighLight = 'Turn off Highlighting'
        highLightOn = 'Turn on Highlighting'
        myOptions = (continuePause, continueNoPause, highLightOn, quit)
        if highLightTime:
            myOptions = (continuePause, continueNoPause, noHighLight, quit)

        result = select ("Paused! Pick an option:", options = myOptions)

        if result == noHighLight:
            print "No HighLighting"
            highLightTime = 0
            
        elif result == highLightOn:
            print "Turn Highlighing on"
            highLightTime = 2
            
        elif result == quit:
            print "Cancelled"
            running = False
        
        elif result == continueNoPause:
            pauseAtEachIteration = False

def elapsedTime(start):
    secs = time.time() - start
    if secs < 60:
        return str(secs) + "secs"
    else:
        minutes = secs / 60
        if minutes < 60:
            return str(minutes) + "min"
        else:
            hours = minutes / 60
            return str(hours) + "hr"

def doChecks():
    print("Starting Checks...")
    global page
    global running
    global pauseAtEachIteration
    global highLightTime
    page = 0
    autoScrolled = False
    checkFailed = False
    running = True
    pauseAtEachIteration = False
    highLightTime = 0
    newState = {}
    invalidContent = 0

    state = {
        "autoScrolled": autoScrolled,
        "endAtGroup": None,
    }

    respondToAlerts()
    
    actionsRegion.wait(action) # make sure tCore is visible

    while not checkFailed and running:
        page = page + 1
        print "Starting Group ", page
        newState = iterateGroupSegment(config, state)
        print "Group ", page, ", elapsed time ", elapsedTime(start), ", results: ", newState

        if not running:
            break

        checkFailed = newState["checkFailed"]

        if newState["invalidContent"]:
            invalidContent = invalidContent + 1
            print "Invalid content found! Count now at ", invalidContent

        doPause()
        
        state = newState

    newState["invalidContent"] = invalidContent
    print ("Finished with checks, running ", running, ", checkFailed ", checkFailed, ", invalid Content Found ", invalidContent) 
    return newState

def getLaunchButtons():
    launches = findAllImagesBase(toolsArea, [], launchButton)
    print ("launch buttons found ", len(launches))
    return launches

def getGlTextAreaFromLaunchButton(launchButton):
    glBoxActual = Region(launchButton.x + launchButton.w/2 - 337, launchButton.y + launchButton.h/2 - 2, glBox.w, glBox.h)
    return glBoxActual

def getGlPopupAreaFromLaunchButton(launchButton, pos):
    glBoxActual = Region(launchButton.x + launchButton.w/2 - 337, launchButton.y + launchButton.h/2 + (glBox.h+8)*pos - 4, glBox.w + 40, glBox.h)
    return glBoxActual

def getPopupText(region, highlight):
    if highlight:
        region.highlight()
        sleep(highlight)
        region.highlightOff()
    
    text = region.text().strip().encode('UTF-8')
    print "At y=", region.y, " found text: '", text, "'"
    return {
        "region": region,
        "text": text,
    }

def getAlertMessage(alertFound, offsetY):
    if not alertFound:
        alertDialogFound = findAllImagesBase(alertRegion, [], alertDialog)
        if len(alertDialogFound):
            alertFound = alertDialogFound[0]

    if alertFound:
        region = Region(alertFound.x + alertFound.w/2 + 62, alertFound.y + alertFound.h/2 + offsetY - 72, messageRegion.w, messageRegion.h)
        text = getPopupText(region, 0.5)
        text["alertFound"] = alertFound
        print "Alert Found!"
        return text

    return None

INVALIDATE_WARNING = "project in translationNotes could invalidate"
CHANGES_DETECTED = "Changes have been detected in your project"
INVALID_CONTENT = "content for this check"

def checkForAlerts(respond = True):
    alert = None
    clicked = False
    type = None
    alertFound = None
    offsetY = 0

    for i in range(4):
        alert = getAlertMessage(alertFound, offsetY)
        if alert == None:
            print "No alert found!"
            break
        else:
            print "found alert message ", alert
            alertMsg = alert["text"]
            if INVALIDATE_WARNING in alertMsg:
                print "Invalidate Warning"
                type = INVALIDATE_WARNING
                continue_ = findFirstImage(alertDialogRegion, continueButton)
                click(continue_)
                clicked = True
                break

            if CHANGES_DETECTED in alertMsg:
                print "Changes Detected"
                type = CHANGES_DETECTED
                continue_ = findFirstImage(alertDialogRegion, okButton)
                click(continue_)
                clicked = True
                break

            if INVALID_CONTENT in alertMsg:
                print "Invalid Content"
                type = INVALID_CONTENT
                text = getPopupText(invalidCheckRegion, 2)
                print "Invalid check details: ", text
                continue_ = findFirstImage(alertDialogRegion, ignoreButton)
                click(continue_)
                clicked = True
                break

            print "Unknown alert text: " + alert["text"]
            if  alert["alertFound"]:
                alertFound = alert["alertFound"]
    
        offsetY = offsetY + 22

    if clicked:
        sleep(1)

    return {
        "alert": alertFound,
        "responded": clicked,
        "type": type
    }

def respondToAlerts():
    alertFound = None
    type = None
    invalidContent = 0

    for j in range(4):
        results = checkForAlerts(True)
        if results["alert"]:
            alertFound = results["alert"]
            type = results["type"]
            print "Alert type found ", type
            if type == INVALID_CONTENT:
                invalidContent = invalidContent + 1
                print "Found invalid content, count now ", invalidContent
            # if alert acknowledged, we check for another
        else:
            break # nothing more to do
        
    return {
        "alertFound": alertFound,
        "type": type,
        "invalidContent": invalidContent
    }

def getGlPopupText(launchButton, pos):
    region = getGlPopupAreaFromLaunchButton(launchButton, pos)
    results = getPopupText(region, 0.5)
    return results
        
def checkAll(launchButton):
    checkArea = Region(launchButton.x + launchButton.w/2 + togglesXOffset, launchButton.y + togglesYOffset, launchButton.w/2 - togglesXOffset, -togglesYOffset)
    #checkArea.highlight()
    #sleep(5)
    for image in [partialChecked, unchecked]:
        print "image ", image
        buttons = findAllImagesBase(checkArea, [], image)
        print "buttons ", buttons
        for button in buttons:
            button.click()

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
        sleep(0.5)
        region.highlightOff()
        text = region.text().strip().encode('UTF-8')
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

def getGlPopupOptions(launchButton, max):
    popups = []
    for i in range(max):
        popup = getGlPopupText(launchButton, i)
        popups.append(popup)
    return popups

def checkOpenProject(langID):
    checkTNotesArray = [True, False]
    finshed = False
    runSingleCheck = False
    invalidContent = 0
    currentProject = 'Unknown'
    finalState = {}
    projectStart = time.time()

    print "Startup!"
    times = {}
    langID = input ("Enter Language (empty for no preference).\nOpen Project to tools page or launch tNotes or tWords.\nDo CTRL-F12 to abort or CTRL-F11 for options.\nAre you ready to start?", langID)
    if langID != None:
        sleep(1)
        projectFolders = findAllImagesBase(headerArea, [], projectFolder)
        print ("projectFolders buttons found ", len(projectFolders))
        if len(projectFolders):
            folder = projectFolders[0]
            region = Region(folder.x + folder.w, folder.y, 150, folder.h, )
            results = getPopupText(region, 0.5)
            currentProject = results["text"]
            print "Current Project: ", currentProject
        else:
            print "no project folders found"

        for checkTNotes in checkTNotesArray:
            if checkTNotes:
                click(scrollUp)
            else:
                click(scrollDown)
            sleep(2)

            
            launchButton_ = getFirstLaunchButtonInfo()
            if not launchButton_:
                print "Launch button not found, try starting checking"
                runSingleCheck = True
            else:
                currentGL = launchButton_["glText"]
                wrongGL = False
                # default select en if none selected
                matchLangStr = "(" + langID + ")"  if (langID != '') else '(en)'
                print "Matching in GL: ", matchLangStr
                if currentGL == 'Select Gateway Language':
                    print "No Gl Selected, want ", langID
                    wrongGL = True
                elif (langID != '') and (not (matchLangStr in currentGL)):
                    print "Wrong Gl Selected '", currentGL, "', want ", langID
                    wrongGL = True

                if wrongGL:
                    click(launchButton_["glTextArea"])
                    sleep(1)
                    popups = getGlPopupOptions(launchButton_["launchButton"], 6)
                    print "popups= ", popups
                    pos = -1
                    glOptionRange = None
                    for i in range(len(popups)):
                        print i
                        popup = popups[i]
                        glText = popup["text"]
                        print "Found popup option ", glText
                        if matchLangStr in glText:
                            print "found Match at ", i
                            pos = i
                            break

                    if pos < 0:
                        print "Match not found, default to 0"
                        pos = 0

                    popup = popups[pos]
                    print "popup= ", popup

                    click(popup["region"])
                    sleep(1)
                    launchButton_ = getFirstLaunchButtonInfo()
                    
                sleep(1)
                checkAll(launchButton_["launchButton"])

                click(launchButton_["launchButton"])
                sleep(1)
                
            toolNameStr = toolName.text().strip().encode('UTF-8')
            print "Running tool '", toolNameStr, "'"
            
            toolStart = time.time()

            finalState = doChecks()

            finished = finalState["finished"]
            checkFailed = finalState["checkFailed"]
            if finalState["invalidContent"]:
                invalidContent = invalidContent + finalState["invalidContent"]
                print "Found ", finalState["invalidContent"], " invalid checks in tool, total is now ", invalidContent
            elapsed = elapsedTime(toolStart)
            times[toolNameStr] = elapsed
            print "Tool ", toolNameStr, " took ", elapsed
            print "Final State = ", finalState
            if not finished or checkFailed:
                print "Checks failed"
                break
            
            if runSingleCheck:
                print "Just ran a single check"
                break
            else:
                print "Return to tools card"
                click(toolName)
                sleep(2)

        finalState["runSingleCheck"] = runSingleCheck
        finalState["invalidContent"] = invalidContent
        final = "doChecks finished with " + str(finalState)
        print "Finished testing ", currentProject
        print "Times= ", times
        print "Project run time= ", elapsedTime(projectStart)
        print(final)
        choice = popAsk (final)
    else:
        print "Cancelled"


