; example2.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects.
;
; See install-shared.nsi for a more robust way of checking for administrator rights.
; See install-per-user.nsi for a file association example.

;--------------------------------

; The name of the installer
Name "Aion Classic Mods by Load - v0.2.2b RC2"

; The file to write
OutFile "Aion-Classic-Mods.exe"

; Request application privileges for Windows Vista and higher
RequestExecutionLevel admin

; Build Unicode installer
Unicode True

; The default installation directory
InstallDir $PROGRAMFILES\Aion-Classic-Mods

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\Aion-Classic-Mods" "Install_Dir"

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "Example2 (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File "Aion-Classic-Mods.nsi"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\Aion-Classic-Mods "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Aion-Classic-Mods" "DisplayName" "Aion-Classic-Mods"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Aion-Classic-Mods" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Aion-Classic-Mods" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Aion-Classic-Mods" "NoRepair" 1
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\Aion-Classic-Mods"
  CreateShortcut "$SMPROGRAMS\Aion-Classic-Mods\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  CreateShortcut "$SMPROGRAMS\Aion-Classic-Mods\Aion-Classic-Mods.lnk" "$INSTDIR\Aion-Classic-Mods.nsi"

SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Aion-Classic-Mods"
  DeleteRegKey HKLM SOFTWARE\Aion-Classic-Mods

  ; Remove files and uninstaller
  Delete $INSTDIR\Aion-Classic-Mods.nsi
  Delete $INSTDIR\Aion-Classic-Mods.exe

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\Aion-Classic-Mods\*.lnk"

  ; Remove directories
  RMDir "$SMPROGRAMS\Aion-Classic-Mods"
  RMDir "$INSTDIR"

SectionEnd
