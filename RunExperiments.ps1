# Cache Simulator Experiment Runner
# This script runs multiple cache simulations and collects results

$traceFile = "trace.txt"
$resultsFile = "results.csv"

# Check if trace file exists
if (-not (Test-Path $traceFile)) {
    Write-Host "Error: $traceFile not found. Run GenerateTrace.cs first." -ForegroundColor Red
    exit 1
}

# Create results file with header
"CacheSize,LineSize,Associativity,Policy,Hits,Accesses,HitRate" | Out-File -FilePath $resultsFile -Encoding utf8

# Test different cache sizes (exponents: 8, 9, 10, 11)
$cacheSizeExps = @(8, 9, 10, 11)

# Test different line sizes (exponents: 4, 5, 6)
$lineSizeExps = @(4, 5, 6)

# Test different associativities
$associativities = @("direct", "2way", "4way", "fully")

# Test both replacement policies
$policies = @("lru", "fifo")

Write-Host "Running cache simulation experiments..."
Write-Host "This may take a while...`n"

$experimentCount = 0
$totalExperiments = $cacheSizeExps.Count * $lineSizeExps.Count * $associativities.Count * $policies.Count

foreach ($cacheSizeExp in $cacheSizeExps) {
    foreach ($lineSizeExp in $lineSizeExps) {
        # Skip invalid combinations (line size can't be larger than cache size)
        if ($lineSizeExp -ge $cacheSizeExp) {
            continue
        }
        
        foreach ($associativity in $associativities) {
            foreach ($policy in $policies) {
                $experimentCount++
                $cacheSize = [math]::Pow(2, $cacheSizeExp)
                $lineSize = [math]::Pow(2, $lineSizeExp)
                
                Write-Host "Experiment $experimentCount/$totalExperiments`: " -NoNewline
                Write-Host "Cache=$cacheSize B, Line=$lineSize B, Assoc=$associativity, Policy=$($policy.ToUpper())... " -NoNewline
                
                try {
                    # Run the simulator with command-line arguments
                    $output = dotnet run -- $cacheSizeExp $lineSizeExp $associativity $policy $traceFile 2>&1
                    
                    if ($LASTEXITCODE -eq 0 -and $output) {
                        # Extract the CSV line (last line of output)
                        $csvLine = ($output | Select-Object -Last 1).Trim()
                        if ($csvLine -match "^[\d,]+") {
                            Add-Content -Path $resultsFile -Value $csvLine
                            Write-Host "Done" -ForegroundColor Green
                        } else {
                            Write-Host "No valid output" -ForegroundColor Yellow
                        }
                    } else {
                        Write-Host "Error" -ForegroundColor Red
                    }
                } catch {
                    Write-Host "Exception: $_" -ForegroundColor Red
                }
            }
        }
    }
}

Write-Host "`nExperiments complete! Results saved to $resultsFile" -ForegroundColor Green

