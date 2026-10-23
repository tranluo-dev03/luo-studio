; Inno Setup (https://jrsoftware.org/isinfo.php) - dong goi LUO Studio thanh installer.
; Bien dich xong thi ky file Output\LUO-Studio-Setup.exe bang sign-files.ps1.
; Chay: ISCC.exe installer.iss
#define AppName "LUO Studio"
#define AppVer  "1.1.0"   ; giữ khớp với dòng đầu của version.txt
#define Src     ".."

[Setup]
AppName={#AppName}
AppVersion={#AppVer}
AppPublisher=Nexax
DefaultDirName={autopf}\LUO-Studio
DefaultGroupName={#AppName}
OutputBaseFilename=LUO-Studio-Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "{#Src}\*"; DestDir: "{app}"; Excludes: "release-tools\*,userdata\*"; Flags: recursesubdirs createallsubdirs ignoreversion

[Dirs]
Name: "{app}\userdata"; Permissions: users-modify

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\LUO Studio.bat"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\LUO Studio.bat"

[Run]
Filename: "{app}\LUO Studio.bat"; Description: "Mo LUO Studio"; Flags: postinstall nowait skipifsilent
