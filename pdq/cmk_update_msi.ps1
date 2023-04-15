# [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
# Disable SSL verification
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Version
)
# CheckMK - Vars
$HOST_NAME = "status.$(($env:USERDNSDomain).ToLower())"
$SITE_NAME = "INSERTSITENAMEHERE"
$USERNAME = "INSERTAPIUSERHERE"
$PASSWORD = "INSERTCOINHERE"
$API_URL = "https://$HOST_NAME/$SITE_NAME/check_mk/api/1.0/"

# PDQ - Vars
$PDQServer = "\\INSERTPDQHOSTHERE"
$PDQInvPath = "c$\Program Files (x86)\Admin Arsenal\PDQ Inventory"
$PDQDepPath = "c$\Program Files (x86)\Admin Arsenal\PDQ Deploy"
$PDQInvVarName = "CheckMKAgentVer"
$PDQDepVarName = "CheckMKAgentVer"
$PDQRepo = "\\INSERT\PATH\TO\REPO\HERE\PDQ"

$sep = [IO.Path]::DirectorySeparatorChar
$WorkingDir = $PDQRepo + $sep + "checkmk"
# Overwrite if we are invoked directly from PDQDeploy
if (Get-Command Repository -ErrorAction Ignore) { $WorkingDir = "$(Repository)" + $sep + "checkmk" }

# RestApi Default Headers
$Headers = @{
    'Accept'        = 'application/json'
    'Authorization' = "Bearer $USERNAME $PASSWORD"
    'Content-Type'  = 'application/json'
}

Function getVersion {
    $API = $API_URL+"version"
    $Headers.Accept = 'application/json'
    $CMKV = Invoke-RestMethod -Method Get -Uri $API -Headers $Headers
    Return $CMKV.versions.checkmk
}

Function getMSI {
    $API = $API_URL+"domain-types/agent/actions/download/invoke"
    $Body = @{
        'os_type'   = 'windows_msi'
    }
    $File = $WorkingDir + $sep + "check_mk_agent-$LatestVersion.msi"
    $Headers.Accept = 'application/octet-stream'
    Invoke-RestMethod -Method Get -Uri $API -Headers $Headers -Body $Body -OutFile $File
}

Write-Host "Called with V=$Version"
$LatestVersion = $(getVersion).TrimEnd('.cre')
Write-Host "Found Latest V=$LatestVersion"
$LatestFile = $null
$LatestFile = Get-ChildItem -Path $WorkingDir *$LatestVersion*
if ($null -eq $LatestFile) {
    getMSI
    $LatestFile = Get-ChildItem -Path $WorkingDir *$LatestVersion*
    Write-Host "Downloaded $LatestFile"
}

if ($Version -notlike $LatestVersion) { 
    Write-Host "Updating Inventory and Deploy to V=$LatestVersion"
    &  "$PDQServer\$PDQInvPath\PDQInventory.exe" UpdateCustomVariable -Name $PDQInvVarName -Value $LatestVersion
    &  "$PDQServer\$PDQDepPath\PDQDeploy.exe" UpdateCustomVariable -Name $PDQDepVarName -Value $LatestVersion
}
