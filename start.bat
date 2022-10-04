echo "Starting test in %CD%"

rem get current date
set current=%date%
set cleanDate=%current: =_%
set cleanDate=%cleanDate:/=_%
set logFile=./log/%cleanDate%.log
echo "logFile is set to = %logFile%"

rem clear old compiled class files so not running old code
del *$py.class

1>>%logFile% 2>&1 (
  java -jar %HOMEPATH%\Development\SikulixIDE\sikulixide-2.0.5.jar -c -r %CD%
)
