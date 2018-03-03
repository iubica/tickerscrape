; Installer configuration
; Tested with Inno Installer 5.5.9(a)

[Setup]
AppName=TickerScrape
AppVersion=1.0
DefaultDirName={pf}\TickerScrape
DefaultGroupName=TickerScrape
UninstallDisplayIcon={app}\wxPortfolio.exe
Compression=lzma2
SolidCompression=yes
OutputDir=build\installer

[Files]
Source: "TickerScrape.exe"; DestDir: "{app}"
Source: "python36.dll"; DestDir: "{app}"
Source: "*.py"; DestDir: "{app}"
Source: "bitmaps/*"; DestDir: "{app}/bitmaps"
Source: "bmp_source/*"; DestDir: "{app}/bmp_source"
Source: "cursors/*"; DestDir: "{app}/cursors"
Source: "data/*"; DestDir: "{app}/data"
Source: "scrape/*"; DestDir: "{app}/scrape"
Source: "views/*"; DestDir: "{app}/views"
Source: "widgets/*"; DestDir: "{app}/widgets"
Source: "README.md"; DestDir: "{app}"; DestName: "Readme.txt"; Flags: isreadme

; Comment these out if you want InnoInstaller to generate the setup program quickly
Source: "lib/*"; DestDir: "{app}/lib"; Flags: recursesubdirs
Source: "mpl-data/*"; DestDir: "{app}/mpl-data"; Flags: recursesubdirs
Source: "tcl/*"; DestDir: "{app}/tcl"; Flags: recursesubdirs
Source: "tk/*"; DestDir: "{app}/tk"; Flags: recursesubdirs


[Icons]
Name: "{group}\TickerScrape"; Filename: "{app}\TickerScrape.exe"
