[CmdletBinding()]
param(
    [string]$TargetHost = "www.microsoft.com",
    [int]$DiskWarningPercent = 85,
    [string[]]$CriticalServices = @("Dnscache", "Spooler"),
    [string]$OutputPath = ".\artifacts\windows-endpoint-health.json"
)

$ErrorActionPreference = "Stop"

function New-CheckResult {
    param(
        [string]$Name,
        [ValidateSet("PASS", "WARN", "FAIL")][string]$Status,
        [string]$Severity,
        [string]$Summary,
        [hashtable]$Data = @{}
    )

    [pscustomobject]@{
        Name     = $Name
        Status   = $Status
        Severity = $Severity
        Summary  = $Summary
        Data     = $Data
    }
}

$results = [System.Collections.Generic.List[object]]::new()

# System inventory
$os = Get-CimInstance Win32_OperatingSystem
$computer = Get-CimInstance Win32_ComputerSystem
$results.Add((New-CheckResult -Name "system_inventory" -Status "PASS" -Severity "info" `
    -Summary "$($os.Caption) $($os.Version) on $($computer.Model)" `
    -Data @{ ComputerName = $env:COMPUTERNAME; Manufacturer = $computer.Manufacturer; Model = $computer.Model }))

# Disk pressure
Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
    if ($_.Size -gt 0) {
        $usedPercent = [math]::Round((($_.Size - $_.FreeSpace) / $_.Size) * 100, 1)
        $status = if ($usedPercent -ge $DiskWarningPercent) { "WARN" } else { "PASS" }
        $severity = if ($status -eq "WARN") { "medium" } else { "info" }
        $results.Add((New-CheckResult -Name "disk:$($_.DeviceID)" -Status $status -Severity $severity `
            -Summary "$($_.DeviceID) is $usedPercent% utilized" `
            -Data @{ UsedPercent = $usedPercent; FreeBytes = $_.FreeSpace; SizeBytes = $_.Size }))
    }
}

# DNS
try {
    $dns = Resolve-DnsName -Name $TargetHost -Type A -ErrorAction Stop
    $addresses = @($dns | Where-Object IPAddress | Select-Object -ExpandProperty IPAddress -Unique)
    $results.Add((New-CheckResult -Name "dns_health" -Status "PASS" -Severity "info" `
        -Summary "Resolved $TargetHost to $($addresses.Count) IPv4 address(es)" `
        -Data @{ Host = $TargetHost; Addresses = $addresses }))
}
catch {
    $results.Add((New-CheckResult -Name "dns_health" -Status "WARN" -Severity "medium" `
        -Summary "DNS lookup failed: $($_.Exception.Message)" -Data @{ Host = $TargetHost }))
}

# HTTPS reachability
$tcp = Test-NetConnection -ComputerName $TargetHost -Port 443 -WarningAction SilentlyContinue
$results.Add((New-CheckResult -Name "tcp_443" -Status $(if ($tcp.TcpTestSucceeded) { "PASS" } else { "WARN" }) `
    -Severity $(if ($tcp.TcpTestSucceeded) { "info" } else { "medium" }) `
    -Summary "TCP/443 to ${TargetHost}: $($tcp.TcpTestSucceeded)" `
    -Data @{ RemoteAddress = [string]$tcp.RemoteAddress; SourceAddress = [string]$tcp.SourceAddress }))

# Critical Windows services
foreach ($serviceName in $CriticalServices) {
    try {
        $service = Get-Service -Name $serviceName -ErrorAction Stop
        $healthy = $service.Status -eq "Running"
        $results.Add((New-CheckResult -Name "service:$serviceName" -Status $(if ($healthy) { "PASS" } else { "WARN" }) `
            -Severity $(if ($healthy) { "info" } else { "medium" }) `
            -Summary "$serviceName is $($service.Status)" -Data @{ StartType = [string]$service.StartType }))
    }
    catch {
        $results.Add((New-CheckResult -Name "service:$serviceName" -Status "WARN" -Severity "medium" `
            -Summary "Service query failed: $($_.Exception.Message)"))
    }
}

# Recent system/application errors; collection only, no remediation
$since = (Get-Date).AddHours(-4)
$events = Get-WinEvent -FilterHashtable @{ LogName = @("System", "Application"); Level = 2; StartTime = $since } `
    -ErrorAction SilentlyContinue | Select-Object -First 50 TimeCreated, LogName, ProviderName, Id, Message

$score = 0
foreach ($item in $results) {
    if ($item.Status -ne "PASS") {
        switch ($item.Severity) {
            "low"      { $score += 1 }
            "medium"   { $score += 3 }
            "high"     { $score += 6 }
            "critical" { $score += 10 }
        }
    }
}
$priority = if ($score -ge 10) { "P1" } elseif ($score -ge 6) { "P2" } elseif ($score -ge 3) { "P3" } else { "P4" }

$report = [pscustomobject]@{
    GeneratedAtUtc = (Get-Date).ToUniversalTime().ToString("o")
    ComputerName    = $env:COMPUTERNAME
    Priority        = $priority
    RiskScore       = $score
    Checks          = $results
    RecentErrors    = $events
}

$directory = Split-Path -Parent $OutputPath
if ($directory) { New-Item -ItemType Directory -Path $directory -Force | Out-Null }
$report | ConvertTo-Json -Depth 8 | Set-Content -Path $OutputPath -Encoding UTF8

$results | Format-Table Name, Status, Severity, Summary -AutoSize
Write-Host "`nPriority: $priority | Risk score: $score"
Write-Host "Evidence written to: $OutputPath"
