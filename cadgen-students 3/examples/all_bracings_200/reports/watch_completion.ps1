param([string]$Root)
do { Start-Sleep -Seconds 30; $m=Get-Content -Raw -LiteralPath (Join-Path $Root 'manifest.json') | ConvertFrom-Json } while($m.status -ne 'complete')
$r=Get-Content -Raw -LiteralPath (Join-Path $Root 'reports/results.json') | ConvertFrom-Json
$lines=@('# Results','', '| Metric | Count |','|---|---:|', '| Source models | 200 |', "| geometry_verified | $($r.counts.geometry_verified) |", "| Rejected | $($r.counts.rejected) |", "| Timeout 600s | $($r.counts.timeout) |", "| Error | $($r.counts.error) |", "| Unprocessed | $($r.unprocessed) |", "| Joints | $($r.total_joints) |", '', '## Joint types')
$r.joints.psobject.Properties | ForEach-Object { $lines+=('- '+$_.Name+': '+$_.Value) }
$lines | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $Root 'reports/REPORT.md')
