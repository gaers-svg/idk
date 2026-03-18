# Spawn + multiply notepads
$notepads = @()

# Play sound
$player = New-Object System.Media.SoundPlayer
$player.SoundLocation = "C:\Windows\Media\tada.wav"
$player.PlayLooping()

Add-Type @"
using System;
using System.Runtime.InteropServices;

public class Win {
    [DllImport("user32.dll")]
    public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int W, int H, bool repaint);
}
"@

while ($true) {

    # Multiply: spawn more over time
    for ($i=0; $i -lt (Get-Random -Minimum 1 -Maximum 3); $i++) {
        $p = Start-Process notepad -PassThru
        $notepads += $p
    }

    Start-Sleep -Milliseconds 800

    # Write "KEY" into each new notepad
    foreach ($p in $notepads) {
        if ($p.MainWindowHandle -ne 0) {
            $wshell = New-Object -ComObject WScript.Shell
            $wshell.AppActivate($p.Id)
            Start-Sleep -Milliseconds 50
            $wshell.SendKeys("KEY")
        }
    }

    # Move + resize all notepads
    foreach ($p in $notepads) {
        if ($p.MainWindowHandle -ne 0) {
            $x = Get-Random -Minimum 0 -Maximum 1000
            $y = Get-Random -Minimum 0 -Maximum 700

            # Small windows (tiny chaos)
            [Win]::MoveWindow($p.MainWindowHandle, $x, $y, 200, 150, $true)
        }
    }

    Start-Sleep -Milliseconds 500
}
