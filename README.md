# Cache Simulator - Experiment Guide

This cache simulator tests different cache configurations and generates results for analysis.

## Files

- `Program.cs` - Main cache simulator (supports both interactive and command-line modes)
- `GenerateTrace.cs` - Trace file generator with different access patterns
- `RunExperiments.cs` - Automated experiment runner
- `trace.txt` - Input trace file for the simulator
- `results.csv` - Output file with experiment results

## Quick Start

### Step 1: Generate a Trace File

**Option 1: Compile and run GenerateTrace.cs separately**
```bash
csc GenerateTrace.cs
GenerateTrace.exe sequential 1000
```

**Option 2: Use dotnet script (if installed)**
```bash
dotnet script GenerateTrace.cs sequential 1000
```

**Option 3: Create a simple inline script** (see examples below)

Available patterns:
- `sequential` - Sequential memory accesses (default, 1000 accesses)
- `repeated` - Repeated access to same addresses (tests temporal locality)
- `random` - Random memory accesses (worst case)
- `mixed` - Mix of loads and stores

Examples:
```bash
GenerateTrace.exe sequential 1000
GenerateTrace.exe repeated 2000
GenerateTrace.exe random 5000
GenerateTrace.exe mixed 1000
```

### Step 2: Run Experiments

**Option A: Interactive Mode** (for manual testing)
```bash
dotnet run
```
Then follow the prompts.

**Option B: Command-Line Mode** (for single experiment)
```bash
dotnet run -- <cacheSizeExp> <lineSizeExp> <associativity> <policy> <traceFile>
```

Example:
```bash
dotnet run -- 10 5 fully lru trace.txt
```

**Option C: Automated Experiments** (runs multiple configurations)

Using PowerShell script (recommended):
```powershell
.\RunExperiments.ps1
```

Or compile and run RunExperiments.cs:
```bash
csc RunExperiments.cs
RunExperiments.exe
```

This will test:
- Cache sizes: 256B, 512B, 1024B, 2048B (exponents 8-11)
- Line sizes: 16B, 32B, 64B (exponents 4-6)
- Associativities: direct, 2-way, 4-way, fully associative
- Policies: LRU, FIFO

Results are saved to `results.csv` in CSV format.

## Command-Line Arguments

When using command-line mode:
```
<cacheSizeExp> - Cache size exponent (e.g., 10 = 1024 bytes)
<lineSizeExp> - Line size exponent (e.g., 5 = 32 bytes)
<associativity> - One of: "direct", "2way", "4way", "8way", "16way", "fully"
<policy> - "lru" or "fifo"
<traceFile> - Path to trace file (e.g., "trace.txt")
```

## Results Format

The CSV output contains:
```
CacheSize,LineSize,Associativity,Policy,Hits,Accesses,HitRate
```

Example:
```
1024,32,fully,LRU,800,1000,0.8000
1024,32,fully,FIFO,750,1000,0.7500
```

## Experiment Planning

### Testing Cache Size Impact
Fix line size and associativity, vary cache size:
- Line size: 32B (exp 5)
- Associativity: fully associative
- Policy: LRU
- Cache sizes: 256B, 512B, 1024B, 2048B

### Testing Line Size Impact
Fix cache size and associativity, vary line size:
- Cache size: 1024B (exp 10)
- Associativity: fully associative
- Policy: LRU
- Line sizes: 16B, 32B, 64B

### Testing Associativity Impact
Fix cache size and line size, vary associativity:
- Cache size: 1024B (exp 10)
- Line size: 32B (exp 5)
- Policy: LRU
- Associativities: direct, 2-way, 4-way, fully

### Testing Replacement Policy Impact
Fix all other parameters, compare LRU vs FIFO:
- Cache size: 1024B (exp 10)
- Line size: 32B (exp 5)
- Associativity: fully associative
- Policies: LRU, FIFO

## Next Steps

1. Import `results.csv` into Excel, Python (pandas), or MATLAB
2. Create plots showing:
   - Hit rate vs Cache Size
   - Hit rate vs Line Size
   - Hit rate vs Associativity
   - LRU vs FIFO comparison
3. Analyze trends and write your analysis paper
