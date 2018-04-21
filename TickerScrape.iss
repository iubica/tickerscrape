; Installer configuration
; Tested with Inno Installer 5.5.9(a)

[Setup]
AppName=TickerScrape
AppVersion=1.0
ArchitecturesInstallIn64BitMode=x64
DefaultDirName={pf}\TickerScrape
DefaultGroupName=TickerScrape
SetupIconFile=bitmaps\ticker-scrape-logo.ico
UninstallDisplayIcon={app}\TickerScrape.exe
Compression=lzma2
SolidCompression=yes
OutputDir=build\installer

[Files]
Source: "TickerScrape.exe"; DestDir: "{app}"
Source: "python36.dll"; DestDir: "{app}"
Source: "bitmaps/*"; DestDir: "{app}/bitmaps"; Permissions: users-full
Source: "bmp_source/*"; DestDir: "{app}/bmp_source"; Permissions: users-full
Source: "cursors/*"; DestDir: "{app}/cursors"; Permissions: users-full
Source: "data/*"; DestDir: "{app}/data"; Permissions: users-full
Source: "scrape/*"; DestDir: "{app}/scrape"; Permissions: users-full
Source: "src/*"; DestDir: "{app}/src"; Permissions: users-full
Source: "views/*"; DestDir: "{app}/views"; Permissions: users-full
Source: "widgets/*"; DestDir: "{app}/widgets"; Permissions: users-full
Source: "README.md"; DestDir: "{app}"; DestName: "Readme.txt"; Flags: isreadme; Permissions: users-full

; Comment these out if you want InnoInstaller to generate the setup program quickly
Source: "lib/*"; DestDir: "{app}/lib"; Flags: recursesubdirs
Source: "mpl-data/*"; DestDir: "{app}/mpl-data"; Flags: recursesubdirs; Permissions: users-full

[Dirs]
Name: "{app}/downloads"; Permissions: users-full
 
[Icons]
Name: "{group}\TickerScrape"; Filename: "{app}\TickerScrape.exe"; IconFilename: "{app}\bitmaps\ticker-scrape-logo.ico"; Comment: "Launches the TickerScrape app"

[Support]
AppPublisher=TickerScrape
AppPublisherURL=http://tickerscrape.com/

