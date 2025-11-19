# Cache Simulator Experiment Plan and Results

## Overview
This document outlines the experimental plan for analyzing cache performance across different parameters and presents the collected results.

## Trace File
- **File**: `trace.txt`
- **Size**: 2000 memory accesses
- **Pattern**: Mixed (75% loads, 25% stores, sequential addresses)
- **Address Range**: 0x00000000 to 0x00001F3C (0-8000 bytes)

## Experiment Design

### Experiment 1: Hit Rate vs Cache Size
**Objective**: Measure how cache size affects hit rate

**Fixed Parameters**:
- Line Size: 32 bytes (exponent 5)
- Associativity: Fully Associative
- Replacement Policy: LRU

**Variable**: Cache Size
- 256 bytes (exponent 8)
- 512 bytes (exponent 9)
- 1024 bytes (exponent 10)
- 2048 bytes (exponent 11)

**Expected Trend**: Hit rate should increase as cache size increases due to more cache lines available.

---

### Experiment 2: Hit Rate vs Line Size
**Objective**: Measure how line (block) size affects hit rate

**Fixed Parameters**:
- Cache Size: 1024 bytes (exponent 10)
- Associativity: Fully Associative
- Replacement Policy: LRU

**Variable**: Line Size
- 16 bytes (exponent 4)
- 32 bytes (exponent 5)
- 64 bytes (exponent 6)

**Expected Trend**: Larger line sizes can improve hit rate for sequential access patterns (spatial locality), but may also increase conflict misses.

---

### Experiment 3: Hit Rate vs Associativity
**Objective**: Measure how associativity affects hit rate

**Fixed Parameters**:
- Cache Size: 1024 bytes (exponent 10)
- Line Size: 32 bytes (exponent 5)
- Replacement Policy: LRU

**Variable**: Associativity
- Direct Mapped (1-way)
- 2-way Set Associative
- 4-way Set Associative
- Fully Associative

**Expected Trend**: Higher associativity should improve hit rate by reducing conflict misses, with fully associative performing best.

---

### Experiment 4: Hit Rate vs Replacement Policy
**Objective**: Compare LRU vs FIFO replacement policies

**Fixed Parameters**:
- Cache Size: 1024 bytes (exponent 10)
- Line Size: 32 bytes (exponent 5)
- Associativity: Fully Associative

**Variable**: Replacement Policy
- LRU (Least Recently Used)
- FIFO (First In First Out)

**Expected Trend**: LRU should perform better than FIFO for workloads with temporal locality, as it keeps recently used items in cache.

---

## Results Summary

All results are saved in `experiment_results.csv` with the following format:
```
CacheSize,LineSize,Associativity,Policy,Hits,Accesses,HitRate
```

### Key Metrics to Analyze:
1. **Hit Rate**: Percentage of cache hits (Hits/Accesses)
2. **Hits**: Number of successful cache accesses
3. **Accesses**: Total number of memory accesses (2000 for our trace)

---

## Next Steps for Analysis

1. **Import Data**: Load `experiment_results.csv` into Excel, Python (pandas), or MATLAB
2. **Create Plots**:
   - Plot 1: Hit Rate vs Cache Size (from Experiment 1)
   - Plot 2: Hit Rate vs Line Size (from Experiment 2)
   - Plot 3: Hit Rate vs Associativity (from Experiment 3)
   - Plot 4: Hit Rate comparison: LRU vs FIFO (from Experiment 4)
3. **Analysis**: 
   - Identify trends and explain why they occur
   - Discuss trade-offs (e.g., larger cache = better hit rate but more hardware cost)
   - Compare theoretical expectations with actual results
   - Note any anomalies or unexpected behaviors

---

## Running Additional Experiments

To run the experiments again:
```powershell
.\RunAllExperiments.ps1
```

To run individual experiments, use the cache simulator directly:
```powershell
dotnet run -- <cacheSizeExp> <lineSizeExp> <associativity> <policy> <traceFile>
```

Example:
```powershell
dotnet run -- 10 5 fully lru trace.txt
```

