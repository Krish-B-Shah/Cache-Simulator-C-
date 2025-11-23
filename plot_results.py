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
# Plot 1: Hit Rate vs Cache Size
# ============================================================================
ax1 = plt.subplot(2, 2, 1)
exp1 = df[(df['LineSize'] == 32) & (df['Associativity'] == 'fully') & (df['Policy'] == 'LRU')]
exp1 = exp1.drop_duplicates(subset=['CacheSize'], keep='first')
exp1 = exp1.sort_values('CacheSize')
ax1.plot(exp1['CacheSize'], exp1['HitRate'] * 100, 'o-', linewidth=2, markersize=8, color='#2E86AB')
ax1.set_xlabel('Cache Size (bytes)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Hit Rate (%)', fontsize=12, fontweight='bold')
ax1.set_title('Hit Rate vs Cache Size\n(Line Size=32B, Fully Associative, LRU)', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_ylim([85, 95])
for i, row in exp1.iterrows():
    ax1.annotate(f"{row['HitRate']*100:.2f}%", 
                (row['CacheSize'], row['HitRate']*100),
                textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

# ============================================================================
# Plot 2: Hit Rate vs Line Size
# ============================================================================
ax2 = plt.subplot(2, 2, 2)
exp2 = df[(df['CacheSize'] == 1024) & (df['Associativity'] == 'fully') & (df['Policy'] == 'LRU')]
exp2 = exp2.drop_duplicates(subset=['LineSize'], keep='first')
exp2 = exp2.sort_values('LineSize')
ax2.plot(exp2['LineSize'], exp2['HitRate'] * 100, 's-', linewidth=2, markersize=8, color='#A23B72')
ax2.set_xlabel('Line Size (bytes)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Hit Rate (%)', fontsize=12, fontweight='bold')
ax2.set_title('Hit Rate vs Line Size\n(Cache Size=1024B, Fully Associative, LRU)', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_ylim([70, 100])
for i, row in exp2.iterrows():
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

