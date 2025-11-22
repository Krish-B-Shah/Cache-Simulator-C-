# Cache Simulator Experiment Results Summary

## Experiment Results

All experiments completed successfully with 2000 memory accesses per test.

### Experiment 1: Hit Rate vs Cache Size
| Cache Size | Line Size | Associativity | Policy | Hits | Accesses | Hit Rate |
|------------|-----------|---------------|--------|------|----------|----------|
| 256 B      | 32 B      | Fully         | LRU    | 1750 | 2000     | 87.50%   |
| 512 B      | 32 B      | Fully         | LRU    | 1750 | 2000     | 87.50%   |
| 1024 B     | 32 B      | Fully         | LRU    | 1750 | 2000     | 87.50%   |
| 2048 B     | 32 B      | Fully         | LRU    | 1750 | 2000     | 87.50%   |

**Observation**: Hit rate remains constant at 87.5% across all cache sizes. This suggests the trace fits entirely in even the smallest cache (256B) for this access pattern.

---

### Experiment 2: Hit Rate vs Line Size
| Cache Size | Line Size | Associativity | Policy | Hits | Accesses | Hit Rate |
|------------|-----------|---------------|--------|------|----------|----------|
| 1024 B     | 16 B      | Fully         | LRU    | 1500 | 2000     | 75.00%   |
| 1024 B     | 32 B      | Fully         | LRU    | 1750 | 2000     | 87.50%   |
| 1024 B     | 64 B      | Fully         | LRU    | 1875 | 2000     | 93.75%   |

**Observation**: Hit rate increases with line size (75% → 87.5% → 93.75%). Larger line sizes exploit spatial locality better for sequential access patterns.

---

### Experiment 3: Hit Rate vs Associativity
| Cache Size | Line Size | Associativity | Policy | Hits | Accesses | Hit Rate |
|------------|-----------|---------------|--------|------|----------|----------|
| 1024 B     | 32 B      | Direct        | LRU    | 1750 | 2000     | 87.50%   |
| 1024 B     | 32 B      | 2-way         | LRU    | 1750 | 2000     | 87.50%   |
| 1024 B     | 32 B      | 4-way         | LRU    | 1750 | 2000     | 87.50%   |
| 1024 B     | 32 B      | Fully         | LRU    | 1750 | 2000     | 87.50%   |

**Observation**: Hit rate is constant across all associativities (87.5%). This suggests minimal conflict misses for this trace pattern, so associativity doesn't significantly impact performance.

---

### Experiment 4: Hit Rate vs Replacement Policy
| Cache Size | Line Size | Associativity | Policy | Hits | Accesses | Hit Rate |
|------------|-----------|---------------|--------|------|----------|----------|
| 1024 B     | 32 B      | Fully         | LRU    | 1750 | 2000     | 87.50%   |
| 1024 B     | 32 B      | Fully         | FIFO   | 1750 | 2000     | 87.50%   |

**Observation**: LRU and FIFO perform identically (87.5% hit rate). This suggests the access pattern doesn't benefit from LRU's temporal locality optimization.

---

## Key Findings

1. **Cache Size Impact**: No significant impact for this trace (all sizes achieve 87.5% hit rate)
   - The trace fits in even the smallest cache configuration
   - Suggests the working set is smaller than 256B

2. **Line Size Impact**: Strong positive correlation (75% → 93.75%)
   - Larger line sizes significantly improve hit rate
   - Demonstrates spatial locality benefits for sequential access patterns

3. **Associativity Impact**: No impact (constant 87.5%)
   - Minimal conflict misses for this access pattern
   - Direct-mapped cache performs as well as fully associative

4. **Replacement Policy Impact**: No difference between LRU and FIFO
   - Access pattern doesn't exhibit strong temporal locality
   - Both policies perform identically

---

## Recommendations for Further Analysis

1. **Generate more diverse traces**:
   - Random access patterns
   - Repeated access patterns (temporal locality)
   - Strided access patterns

2. **Test with larger traces** that exceed cache capacity to see cache size effects

3. **Test with non-sequential patterns** to see associativity and replacement policy effects

4. **Create visualizations**:
   - Line charts for hit rate trends
   - Bar charts comparing configurations
   - Heatmaps for multi-dimensional analysis

---

## Data Files

- **Raw Results**: `experiment_results.csv`
- **Experiment Plan**: `EXPERIMENT_PLAN.md`
- **Trace File**: `trace.txt` (2000 accesses)

