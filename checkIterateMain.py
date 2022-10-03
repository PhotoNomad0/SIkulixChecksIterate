################################
# iterates through all of checks starting with current location
# Note: Use control-F12 to abort
# Note: Use control-F11 to toggle pausing

from sikuli.Sikuli import *

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

################################
# initial config

Settings.MouseMoveDelay = 0
pauseAtEachIteration = False
bottomScrollWidth = 9
bottomScrollHeight = 9
scrollBarRegion = Region(241,54,8,758)
bottomScrollRegion = Region(scrollBarRegion.x-1, scrollBarRegion.y+scrollBarRegion.h-bottomScrollHeight+8,bottomScrollWidth+2,bottomScrollHeight+2)
highLightTime = 0 # set to zero to disable highlighting, otherwise set to how many seconds you want to wait on a highlight
page = 0
running = True

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
# init vars

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

print "scrollBarRegion=", scrollBarRegion
print "bottomScroll = ", bottomScroll
print "bottomScrollRegion=", bottomScrollRegion

print 'Running'

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

def by_y(group):
    return group["match"].y

def by_y_item(item):
    return item.y

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
    print "groups=", len(groups), " found"
    if len(groups):
        groups = sorted(groups, key=by_y_item) # sort keys by y order
    return groups

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
        wait(action)
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
    region = Region(30, y - 4, 169, 25)
    doHighLight(region)
    text = region.text()
    print "At y=", y, " found text: ", text
    click(region)
    success_ = verifyNotCrashed(config)
    return (success_)

def doHighLight(region):
    if highLightTime:
        region.highlight()
        sleep(highLightTime)
        region.highlightOff()

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
    sleep(0.125)
    startScrollBar = scrollBarRegion.getScreen().capture(scrollBarRegion)
    print " startScrollBar = ", startScrollBar

    selectedY = region.y
    overScrolled = False
    print "FInding selected group"
    results = getGroupsFromDisplayedMenu(config)
    if (results["selected"]):
        match = results["selected"]["match"]
        region_ = Region(37, match.y - 10, 169, 35)
        doHighLight(region_)
        text = region_.text()
        print "Starting at group ", text, " at ", region_
        
        if (results["collapsed"]):
            print "Expanding selection ", match
            click(match)
            success = verifyNotCrashed(config)
            if not success:
                print "crashed"
            else:
                results = getGroupsFromDisplayedMenu(config)
        else:
            print "Already expanded"
    
        div = results["selected"]["match"]
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
    groups = results["groups"]
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
            text = region_.text()
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

    print "Iterating checks, startY= ", startY, ", selectedY= ", selectedY
    for i in range(0, len(steps)-1):
        y = steps[i]
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
    if running:
        sleep(0.125)
        scrollbarUnchanged = scrollBarRegion.exists(startScrollBar.getFile(), 1)
        if not scrollbarUnchanged:
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

    return {
        "scrollbarUnchanged": scrollbarUnchanged,
        "checkFailed": checkFailed,
        "autoScrolled": autoScrolled,
        "endAtGroup": endAtGroup,
        "cancelled": cancelled,
        "finished": finished,
    }


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

    state = {
        "autoScrolled": autoScrolled,
        "endAtGroup": None,
    }
    
    wait(action)

    while not checkFailed and running:
        page = page + 1
        print "Starting Group ", page
        newState = iterateGroupSegment(config, state)
        print "Group ", page, ", elapsed time ", elapsedTime(start), ", results: ", newState

        if not running:
            break

        if newState["checkFailed"]:
            break

        doPause()
        
        state = newState

    print ("Finished with checks, running ", running) 
    return newState["finished"]


                    

