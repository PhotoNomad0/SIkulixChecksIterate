import checkIterateMain

# run with:
#java -jar %HOMEPATH%\Development\SikulixIDE\sikulixide-2.0.5.jar -c -r %HOMEPATH%\Development\SikulixTesting\SIkulixChecksIterate.sikuli

print "Startup!"
choice = popAsk ("Are you ready to start?")
if choice:
    finshed = checkIterateMain.doChecks()
    final = "doChecks finished with " + str(finshed)
    print(final)
    choice = popAsk (final)
else:
    print "Cancelled"