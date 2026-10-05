param([switch]$Restore)
$ErrorActionPreference = 'Stop'
if ([IntPtr]::Size -ne 8) { throw 'Use 64-bit PowerShell.' }
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($identity)
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) { throw 'Run PowerShell as Administrator.' }
$originalHash = 'FBF17423E5CD778CD8D59768C5CBB71D3A24447EB7C34FBCA8379B0F11DCAF5E'
$patchedHash = '8A7A9A9D226A50CFF6C03028F841A3D2C7A96BA213EC9DAA9957669E8013A454'
$target = Join-Path ([Environment]::SystemDirectory) 'SaiQFFB5.dll'
$backup = "$target.codex-v01-original.bak"
$source = Join-Path $PSScriptRoot 'patched\SaiQFFB5.dll'
if (-not (Test-Path -LiteralPath $target -PathType Leaf)) { throw 'Original Saitek DLL is not installed. This script does not install a driver package.' }
$current = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
if ($Restore) {
 if ($current -ne $patchedHash) { throw 'Current DLL is not this patch; refusing to replace another version.' }
 if (-not (Test-Path -LiteralPath $backup -PathType Leaf)) { throw 'Backup missing.' }
 if ((Get-FileHash -LiteralPath $backup -Algorithm SHA256).Hash -ne $originalHash) { throw 'Unexpected backup hash.' }
 Copy-Item -LiteralPath $backup -Destination $target -Force
 if ((Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash -ne $originalHash) { throw 'Restore verification failed.' }
 Write-Host 'Original Saitek DLL restored. Reconnect the joystick and restart the test program.'
 exit
}
if ($current -eq $patchedHash) { Write-Host 'This patch is already installed.'; exit }
if ($current -ne $originalHash) { throw 'Unsupported installed DLL. This script will not replace a previous patch or an alternative driver.' }
if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw 'Patched DLL missing. Generate it locally with build_patch.py; see README.md.' }
if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash -ne $patchedHash) { throw 'Patch file hash mismatch.' }
if (Test-Path -LiteralPath $backup) {
 if ((Get-FileHash -LiteralPath $backup -Algorithm SHA256).Hash -ne $originalHash) { throw 'Existing backup has an unexpected hash.' }
} else { Copy-Item -LiteralPath $target -Destination $backup }
Copy-Item -LiteralPath $source -Destination $target -Force
if ((Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash -ne $patchedHash) { throw 'Installation verification failed.' }
Write-Host 'Experimental Saitek DLL installed. Reconnect joystick and restart test program. Rollback: .\Install.ps1 -Restore'
