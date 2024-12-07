[Setup]
AppName=Music Player
AppVersion=1.9
DefaultDirName={pf}\MusicPlayer
DefaultGroupName=MusicPlayer
OutputDir=Output
OutputBaseFilename=MusicPlayerSetup

[Files]
Source: "dist\Musicplayer.exe"; DestDir: "{app}"

[Icons]
Name: "{commondesktop}\MusicPlayer"; Filename: "{app}\Musicplayer.exe"
