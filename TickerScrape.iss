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

; Comment these out if you want InnoInstaller to generate the setup program quickly
Source: "lib/*"; DestDir: "{app}/lib"; Flags: recursesubdirs
Source: "mpl-data/*"; DestDir: "{app}/mpl-data"; Flags: recursesubdirs; Permissions: users-full

[Dirs]
; Set full user permissions for non-lib folders. 
; This is needed by the upgrade operation.
Name: "{app}/bitmaps"; Permissions: users-full
Name: "{app}/bmp_source"; Permissions: users-full
Name: "{app}/cursors"; Permissions: users-full
Name: "{app}/data"; Permissions: users-full
Name: "{app}/downloads"; Permissions: users-full
Name: "{app}/mpl-data"; Permissions: users-full
Name: "{app}/scrape"; Permissions: users-full
Name: "{app}/src"; Permissions: users-full
Name: "{app}/views"; Permissions: users-full
Name: "{app}/widgets"; Permissions: users-full
Name: "{app}"; Permissions: users-full
 
[InstallDelete]
Type: filesandordirs; Name: "{app}/bitmaps"
Type: filesandordirs; Name: "{app}/bmp_source"
Type: filesandordirs; Name: "{app}/cursors"
Type: filesandordirs; Name: "{app}/data"
Type: filesandordirs; Name: "{app}/libs"
Type: filesandordirs; Name: "{app}/mpl-data"
Type: filesandordirs; Name: "{app}/scrape"
Type: filesandordirs; Name: "{app}/src"
Type: filesandordirs; Name: "{app}/views"
Type: filesandordirs; Name: "{app}/widgets"
Type: filesandordirs; Name: "{app}/TickerScrape.exe"
Type: filesandordirs; Name: "{app}/python36.dll"

[UninstallDelete]
Type: filesandordirs; Name: "{app}/bitmaps"
Type: filesandordirs; Name: "{app}/bmp_source"
Type: filesandordirs; Name: "{app}/cursors"
Type: filesandordirs; Name: "{app}/data"
Type: filesandordirs; Name: "{app}/downloads"
Type: filesandordirs; Name: "{app}/libs"
Type: filesandordirs; Name: "{app}/mpl-data"
Type: filesandordirs; Name: "{app}/scrape"
Type: filesandordirs; Name: "{app}/src"
Type: filesandordirs; Name: "{app}/views"
Type: filesandordirs; Name: "{app}/widgets"
Type: filesandordirs; Name: "{app}/TickerScrape.exe"
Type: filesandordirs; Name: "{app}/python36.dll"

[Tasks]
Name: StartAfterInstall; Description: Run TickerScrape app after install

[Run]
Filename: {app}\TickerScrape.exe; Flags: shellexec skipifsilent nowait; Tasks: StartAfterInstall

[Icons]
Name: "{group}\TickerScrape"; Filename: "{app}\TickerScrape.exe"; IconFilename: "{app}\bitmaps\ticker-scrape-logo.ico"; Comment: "Launches the TickerScrape app"

[Support]
AppPublisher=TickerScrape
AppPublisherURL=http://tickerscrape.com/

