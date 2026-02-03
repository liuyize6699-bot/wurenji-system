@echo off
echo 正在创建桌面快捷方式...

set "desktop=%USERPROFILE%\Desktop"
set "shortcut=%desktop%\轻语AI飞控指挥系统.lnk"
set "target=%~dp0启动轻语飞控.bat"

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut%'); $Shortcut.TargetPath = '%target%'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.IconLocation = 'shell32.dll,21'; $Shortcut.Description = '轻语AI飞控指挥系统'; $Shortcut.Save()"

echo 桌面快捷方式创建完成！
echo 快捷方式位置: %shortcut%
pause