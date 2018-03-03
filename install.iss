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
Source: "wxPortfolio.exe"; DestName: "TickerScrape.exe"; DestDir: "{app}"
Source: "README.md"; DestDir: "{app}"; DestName: "Readme.txt"; Flags: isreadme

[Icons]
Name: "{group}\TickerScrape"; Filename: "{app}\TickerScrape.exe"