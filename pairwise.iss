; Inno Setup script for Pairwise Test Case Generator (Windows)
; Requires:
;   1. Python + PyInstaller (run build_windows.bat first)
;   2. Inno Setup (https://jrsoftware.org/isinfo.php)
;
; Usage:
;   1. Run build_windows.bat to create dist\Pairwise\Pairwise.exe
;   2. Right-click this .iss file → "Compile"
;      OR drag this .iss onto ISCC.exe

#define MyAppName "Pairwise Test Case Generator"
#define MyAppShortName "Pairwise"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Timur Poltorakov"
#define MyAppURL "https://github.com/vyaaliy/pairwise"
#define MyAppExeName "Pairwise.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppShortName}
DefaultGroupName={#MyAppShortName}
DisableProgramGroupPage=yes
OutputDir=.
OutputBaseFilename=Pairwise-Windows-Setup
SetupIconFile=pairwise.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
Source: "dist\Pairwise\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Pairwise\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppShortName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppShortName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppShortName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent