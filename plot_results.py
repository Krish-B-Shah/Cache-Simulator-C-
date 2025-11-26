#!/usr/bin/env python3
"""
Cache Simulator Results Plotting Script
Generates plots for hit rate analysis across different cache parameters
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the results
df = pd.read_csv('experiment_results.csv')

# Set up the plotting style
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    try:
        plt.style.use('seaborn-darkgrid')
    except:
        plt.style.use('default')
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
fig = plt.figure(figsize=(16, 10))

# ============================================================================
# Plot 1: Hit Rate vs Cache Size (with FIFO and LRU)
# ============================================================================
ax1 = plt.subplot(2, 2, 1)
exp1_lru = df[(df['LineSize'] == 32) & (df['Associativity'] == 'fully') & (df['Policy'] == 'LRU')]
exp1_lru = exp1_lru.drop_duplicates(subset=['CacheSize'], keep='first')
exp1_lru = exp1_lru.sort_values('CacheSize')

exp1_fifo = df[(df['LineSize'] == 32) & (df['Associativity'] == 'fully') & (df['Policy'] == 'FIFO')]
exp1_fifo = exp1_fifo.drop_duplicates(subset=['CacheSize'], keep='first')
exp1_fifo = exp1_fifo.sort_values('CacheSize')

ax1.plot(exp1_lru['CacheSize'], exp1_lru['HitRate'] * 100, 'o-', linewidth=2, markersize=8, 
         color='#2E86AB', label='LRU')
ax1.plot(exp1_fifo['CacheSize'], exp1_fifo['HitRate'] * 100, 's--', linewidth=2, markersize=8, 
         color='#D00000', label='FIFO')

# Add real device markers
ax1.scatter([32768, 65536], [93.7, 93.7], s=250, marker='*', 
            c=['#06A77D', '#A23B72'], edgecolors='black', linewidths=2,
            label='Real Devices', zorder=5)
ax1.text(32768, 94.5, 'Raspberry Pi 4\n(32KB)', fontsize=9, ha='center', 
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
ax1.text(65536, 94.5, 'Intel i7-12700H\n(64KB)', fontsize=9, ha='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

ax1.set_xlabel('Cache Size (bytes)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Hit Rate (%)', fontsize=12, fontweight='bold')
ax1.set_title('Hit Rate vs Cache Size\n(Line Size=32B, Fully Associative)', fontsize=13, fontweight='bold')
ax1.legend(loc='best', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_ylim([85, 96])
ax1.set_xlim([0, 70000])  # Extend to show real devices
for i, row in exp1_lru.iterrows():
    ax1.annotate(f"{row['HitRate']*100:.2f}%", 
                (row['CacheSize'], row['HitRate']*100),
                textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

# ============================================================================
# Plot 2: Hit Rate vs Line Size (with FIFO and LRU)
# ============================================================================
ax2 = plt.subplot(2, 2, 2)
exp2_lru = df[(df['CacheSize'] == 1024) & (df['Associativity'] == 'fully') & (df['Policy'] == 'LRU')]
exp2_lru = exp2_lru.drop_duplicates(subset=['LineSize'], keep='first')
exp2_lru = exp2_lru.sort_values('LineSize')

exp2_fifo = df[(df['CacheSize'] == 1024) & (df['Associativity'] == 'fully') & (df['Policy'] == 'FIFO')]
exp2_fifo = exp2_fifo.drop_duplicates(subset=['LineSize'], keep='first')
exp2_fifo = exp2_fifo.sort_values('LineSize')

ax2.plot(exp2_lru['LineSize'], exp2_lru['HitRate'] * 100, 'o-', linewidth=2, markersize=8, 
         color='#2E86AB', label='LRU')
ax2.plot(exp2_fifo['LineSize'], exp2_fifo['HitRate'] * 100, 's--', linewidth=2, markersize=8, 
         color='#D00000', label='FIFO')

# Add real device markers (both use 64-byte lines)
ax2.scatter([64, 64], [93.7, 93.7], s=250, marker='*', 
            c=['#06A77D', '#A23B72'], edgecolors='black', linewidths=2,
            label='Real Devices', zorder=5)
ax2.text(64, 95.5, 'Raspberry Pi 4 &\nIntel i7-12700H\n(64B lines)', fontsize=9, ha='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

ax2.set_xlabel('Line Size (bytes)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Hit Rate (%)', fontsize=12, fontweight='bold')
ax2.set_title('Hit Rate vs Line Size\n(Cache Size=1024B, Fully Associative)', fontsize=13, fontweight='bold')
ax2.legend(loc='best', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_ylim([70, 97])
for i, row in exp2_lru.iterrows():
    ax2.annotate(f"{row['HitRate']*100:.2f}%", 
                (row['LineSize'], row['HitRate']*100),
                textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

# ============================================================================
# Plot 3: Hit Rate vs Associativity
# ============================================================================
ax3 = plt.subplot(2, 2, 3)
exp3 = df[(df['CacheSize'] == 1024) & (df['LineSize'] == 32) & (df['Policy'] == 'LRU')]
# Remove duplicates, keeping first occurrence
exp3 = exp3.drop_duplicates(subset=['Associativity'], keep='first')
# Map associativity to display order
assoc_order = ['direct', '2way', '4way', 'fully']
assoc_labels = ['Direct\n(1-way)', '2-way', '4-way', 'Fully\nAssociative']
# Create a dictionary for easy lookup
exp3_dict = dict(zip(exp3['Associativity'], exp3['HitRate']))
# Build sorted data in correct order
exp3_sorted = pd.DataFrame({
    'Associativity': assoc_order,
    'HitRate': [exp3_dict.get(a, 0) for a in assoc_order]
})
ax3.bar(range(len(exp3_sorted)), exp3_sorted['HitRate'] * 100, color='#F18F01', alpha=0.7, edgecolor='black', linewidth=1.5)
ax3.set_xticks(range(len(assoc_labels)))
ax3.set_xticklabels(assoc_labels, fontsize=10)
ax3.set_xlabel('Associativity', fontsize=12, fontweight='bold')
ax3.set_ylabel('Hit Rate (%)', fontsize=12, fontweight='bold')
ax3.set_title('Hit Rate vs Associativity\n(Cache Size=1024B, Line Size=32B, LRU)', fontsize=13, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')
ax3.set_ylim([85, 90])
for i, (idx, row) in enumerate(exp3_sorted.iterrows()):
    ax3.text(i, row['HitRate']*100 + 0.3, f"{row['HitRate']*100:.2f}%", 
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# ============================================================================
# Plot 4: Hit Rate vs Replacement Policy
# ============================================================================
ax4 = plt.subplot(2, 2, 4)
exp4 = df[(df['CacheSize'] == 1024) & (df['LineSize'] == 32) & (df['Associativity'] == 'fully')]
exp4 = exp4.drop_duplicates(subset=['Policy'], keep='first')
exp4 = exp4.sort_values('Policy')
colors = ['#06A77D', '#D00000']
bars = ax4.bar(exp4['Policy'], exp4['HitRate'] * 100, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
ax4.set_xlabel('Replacement Policy', fontsize=12, fontweight='bold')
ax4.set_ylabel('Hit Rate (%)', fontsize=12, fontweight='bold')
ax4.set_title('Hit Rate vs Replacement Policy\n(Cache Size=1024B, Line Size=32B, Fully Associative)', fontsize=13, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')
ax4.set_ylim([85, 90])
for i, (idx, row) in enumerate(exp4.iterrows()):
    ax4.text(i, row['HitRate']*100 + 0.3, f"{row['HitRate']*100:.2f}%", 
            ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('cache_simulation_results.png', dpi=300, bbox_inches='tight')
print("Plots saved to 'cache_simulation_results.png'")
plt.show()

# Print summary statistics
print("\n" + "="*70)
print("EXPERIMENT SUMMARY STATISTICS")
print("="*70)
print(f"\nTotal experiments: {len(df)}")
print(f"Average hit rate: {df['HitRate'].mean()*100:.2f}%")
print(f"Highest hit rate: {df['HitRate'].max()*100:.2f}%")
print(f"Lowest hit rate: {df['HitRate'].min()*100:.2f}%")
print(f"\nBest configuration:")
best = df.loc[df['HitRate'].idxmax()]
print(f"  Cache Size: {best['CacheSize']} bytes")
print(f"  Line Size: {best['LineSize']} bytes")
print(f"  Associativity: {best['Associativity']}")
print(f"  Policy: {best['Policy']}")
print(f"  Hit Rate: {best['HitRate']*100:.2f}%")

