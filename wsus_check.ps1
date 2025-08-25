# -------------------------------
# 检测 SECRET_KEY 环境变量 / Check SECRET_KEY environment variable
# -------------------------------
if (-not $env:SECRET_KEY -or $env:SECRET_KEY -ne "HDfPkbdM7X-Qn4cCqMC-sJTVi5DSLA3j1p_Xi5s3lJI=") {
    Write-Output "SECRET_KEY 不存在或不等于指定值，自动设置... / SECRET_KEY not set or incorrect, automatically setting..."
    $env:SECRET_KEY = "HDfPkbdM7X-Qn4cCqMC-sJTVi5DSLA3j1p_Xi5s3lJI="
} else {
    Write-Output "SECRET_KEY 已经正确设置 / SECRET_KEY already correctly set"
}

# -------------------------------
# 原 WSUS 查询逻辑 / Original WSUS query logic
# -------------------------------
$result = [PSCustomObject]@{
    Computer_Needing_Updates = (Get-WsusComputer -ComputerUpdateStatus Needed |
        Where-Object { $_.OSDescription -notmatch "Windows 10 Enterprise" }).Count
    Computer_With_Error = (Get-WsusComputer -ComputerUpdateStatus Failed |
        Where-Object { $_.OSDescription -notmatch "Windows 10 Enterprise" }).Count
}

# -------------------------------
# 输出 SECRET_KEY，方便调试 / Output SECRET_KEY for debugging
# -------------------------------
$result | Add-Member -NotePropertyName "SecretKey_From_Env" -NotePropertyValue $env:SECRET_KEY

# -------------------------------
# 输出 JSON / Output as JSON
# -------------------------------
$result | ConvertTo-Json -Depth 3
