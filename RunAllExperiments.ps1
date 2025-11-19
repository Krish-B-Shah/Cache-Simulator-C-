# Comprehensive Cache Simulator Experiment Runner
# Tests hit rate vs cache size, line size, associativity, and replacement policy

$traceFile = "trace.txt"
$resultsFile = "experiment_results.csv"

# Check if trace file exists
if (-not (Test-Path $traceFile)) {
    Write-Host "Error: $traceFile not found. Generate it first." -ForegroundColor Red
    exit 1
}

# Create results file with header
"CacheSize,LineSize,Associativity,Policy,Hits,Accesses,HitRate" | Out-File -FilePath $resultsFile -Encoding utf8

Write-Host "=" * 70
Write-Host "Cache Simulator - Comprehensive Experiment Suite"
Write-Host "=" * 70
Write-Host "Trace file: $traceFile"
Write-Host "Results will be saved to: $resultsFile"
Write-Host ""

# ============================================================================
# EXPERIMENT 1: Hit Rate vs Cache Size
# ============================================================================
Write-Host "EXPERIMENT 1: Hit Rate vs Cache Size" -ForegroundColor Cyan
Write-Host "-" * 70
Write-Host "Fixed parameters: Line Size=32B (exp 5), Fully Associative, LRU"
Write-Host "Varying: Cache Size (256B to 2048B)"
Write-Host ""

$cacheSizeExps = @(8, 9, 10, 11)  # 256B, 512B, 1024B, 2048B
$lineSizeExp = 5  # 32 bytes
$associativity = "fully"
$policy = "lru"

foreach ($cacheSizeExp in $cacheSizeExps) {
    $cacheSize = [math]::Pow(2, $cacheSizeExp)
    Write-Host "  Testing Cache Size: $cacheSize bytes (exp $cacheSizeExp)..." -NoNewline
    
    try {
        $output = dotnet run -- $cacheSizeExp $lineSizeExp $associativity $policy $traceFile 2>&1 | Select-Object -Last 1
        if ($output -match "^[\d,]+") {
            Add-Content -Path $resultsFile -Value $output.Trim()
            Write-Host " Done" -ForegroundColor Green
        } else {
            Write-Host " Failed" -ForegroundColor Red
        }
    } catch {
        Write-Host " Error: $_" -ForegroundColor Red
    }
}

Write-Host ""

# ============================================================================
# EXPERIMENT 2: Hit Rate vs Line Size
# ============================================================================
Write-Host "EXPERIMENT 2: Hit Rate vs Line Size" -ForegroundColor Cyan
Write-Host "-" * 70
Write-Host "Fixed parameters: Cache Size=1024B (exp 10), Fully Associative, LRU"
Write-Host "Varying: Line Size (16B to 64B)"
Write-Host ""

$cacheSizeExp = 10  # 1024 bytes
$lineSizeExps = @(4, 5, 6)  # 16B, 32B, 64B
$associativity = "fully"
$policy = "lru"

foreach ($lineSizeExp in $lineSizeExps) {
    $lineSize = [math]::Pow(2, $lineSizeExp)
    Write-Host "  Testing Line Size: $lineSize bytes (exp $lineSizeExp)..." -NoNewline
    
    try {
        $output = dotnet run -- $cacheSizeExp $lineSizeExp $associativity $policy $traceFile 2>&1 | Select-Object -Last 1
        if ($output -match "^[\d,]+") {
            Add-Content -Path $resultsFile -Value $output.Trim()
            Write-Host " Done" -ForegroundColor Green
        } else {
            Write-Host " Failed" -ForegroundColor Red
        }
    } catch {
        Write-Host " Error: $_" -ForegroundColor Red
    }
}

Write-Host ""

# ============================================================================
# EXPERIMENT 3: Hit Rate vs Associativity
# ============================================================================
Write-Host "EXPERIMENT 3: Hit Rate vs Associativity" -ForegroundColor Cyan
Write-Host "-" * 70
Write-Host "Fixed parameters: Cache Size=1024B (exp 10), Line Size=32B (exp 5), LRU"
Write-Host "Varying: Associativity (Direct, 2-way, 4-way, Fully)"
Write-Host ""

$cacheSizeExp = 10  # 1024 bytes
$lineSizeExp = 5  # 32 bytes
$associativities = @("direct", "2way", "4way", "fully")
$policy = "lru"

foreach ($associativity in $associativities) {
    Write-Host "  Testing Associativity: $associativity..." -NoNewline
    
    try {
        $output = dotnet run -- $cacheSizeExp $lineSizeExp $associativity $policy $traceFile 2>&1 | Select-Object -Last 1
        if ($output -match "^[\d,]+") {
            Add-Content -Path $resultsFile -Value $output.Trim()
            Write-Host " Done" -ForegroundColor Green
        } else {
            Write-Host " Failed" -ForegroundColor Red
        }
    } catch {
        Write-Host " Error: $_" -ForegroundColor Red
    }
}

Write-Host ""

# ============================================================================
# EXPERIMENT 4: Hit Rate vs Replacement Policy
# ============================================================================
Write-Host "EXPERIMENT 4: Hit Rate vs Replacement Policy" -ForegroundColor Cyan
Write-Host "-" * 70
Write-Host "Fixed parameters: Cache Size=1024B (exp 10), Line Size=32B (exp 5), Fully Associative"
Write-Host "Varying: Replacement Policy (LRU vs FIFO)"
Write-Host ""

$cacheSizeExp = 10  # 1024 bytes
$lineSizeExp = 5  # 32 bytes
$associativity = "fully"
$policies = @("lru", "fifo")

foreach ($policy in $policies) {
    Write-Host "  Testing Policy: $($policy.ToUpper())..." -NoNewline
    
    try {
        $output = dotnet run -- $cacheSizeExp $lineSizeExp $associativity $policy $traceFile 2>&1 | Select-Object -Last 1
        if ($output -match "^[\d,]+") {
            Add-Content -Path $resultsFile -Value $output.Trim()
            Write-Host " Done" -ForegroundColor Green
        } else {
            Write-Host " Failed" -ForegroundColor Red
        }
    } catch {
        Write-Host " Error: $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=" * 70
Write-Host "All experiments complete!" -ForegroundColor Green
Write-Host "Results saved to: $resultsFile" -ForegroundColor Green
Write-Host "=" * 70

