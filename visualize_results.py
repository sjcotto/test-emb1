"""
Visualization script for embedding model comparison results
Generates charts and detailed analysis from evaluation_results.json
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any


def load_results(filename: str = 'evaluation_results.json') -> Dict:
    """Load evaluation results"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Run embedding_tester.py first.")
        return None


def create_comparison_table(results: Dict) -> pd.DataFrame:
    """Create a comparison table of all metrics"""
    data = []

    for search_type in ['product_search', 'category_search']:
        if search_type not in results:
            continue

        for model_name, metrics in results[search_type].items():
            data.append({
                'Search Type': 'Product' if search_type == 'product_search' else 'Category',
                'Model': model_name,
                'Hit Rate': f"{metrics['hit_rate']:.1%}",
                'MRR': f"{metrics['mrr']:.3f}",
                'Avg Similarity': f"{metrics['avg_similarity']:.3f}",
                'Queries': metrics['num_queries']
            })

    return pd.DataFrame(data)


def plot_comparison(results: Dict, save_path: str = 'comparison_plot.png'):
    """Create comparison plots"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Embedding Model Comparison', fontsize=16, fontweight='bold')

    # Extract data
    models = []
    product_hit_rates = []
    product_mrr = []
    category_hit_rates = []
    category_mrr = []

    if 'product_search' in results:
        for model_name, metrics in results['product_search'].items():
            if model_name not in models:
                models.append(model_name)
            product_hit_rates.append(metrics['hit_rate'] * 100)
            product_mrr.append(metrics['mrr'])

    if 'category_search' in results:
        for model_name, metrics in results['category_search'].items():
            category_hit_rates.append(metrics['hit_rate'] * 100)
            category_mrr.append(metrics['mrr'])

    x = np.arange(len(models))
    width = 0.35

    # Plot 1: Product Search - Hit Rate
    ax1 = axes[0, 0]
    bars1 = ax1.bar(x, product_hit_rates, width, color=['#3498db', '#e74c3c'])
    ax1.set_ylabel('Hit Rate (%)', fontweight='bold')
    ax1.set_title('Product Search - Hit Rate@10')
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, rotation=15, ha='right')
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

    # Plot 2: Product Search - MRR
    ax2 = axes[0, 1]
    bars2 = ax2.bar(x, product_mrr, width, color=['#3498db', '#e74c3c'])
    ax2.set_ylabel('MRR', fontweight='bold')
    ax2.set_title('Product Search - Mean Reciprocal Rank')
    ax2.set_xticks(x)
    ax2.set_xticklabels(models, rotation=15, ha='right')
    ax2.set_ylim(0, 1)
    ax2.grid(axis='y', alpha=0.3)

    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom', fontweight='bold')

    # Plot 3: Category Search - Hit Rate
    ax3 = axes[1, 0]
    bars3 = ax3.bar(x, category_hit_rates, width, color=['#3498db', '#e74c3c'])
    ax3.set_ylabel('Hit Rate (%)', fontweight='bold')
    ax3.set_title('Category Search - Hit Rate@5')
    ax3.set_xticks(x)
    ax3.set_xticklabels(models, rotation=15, ha='right')
    ax3.set_ylim(0, 100)
    ax3.grid(axis='y', alpha=0.3)

    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

    # Plot 4: Category Search - MRR
    ax4 = axes[1, 1]
    bars4 = ax4.bar(x, category_mrr, width, color=['#3498db', '#e74c3c'])
    ax4.set_ylabel('MRR', fontweight='bold')
    ax4.set_title('Category Search - Mean Reciprocal Rank')
    ax4.set_xticks(x)
    ax4.set_xticklabels(models, rotation=15, ha='right')
    ax4.set_ylim(0, 1)
    ax4.grid(axis='y', alpha=0.3)

    for bar in bars4:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Comparison plot saved to {save_path}")
    return fig


def plot_similarity_distribution(results: Dict, save_path: str = 'similarity_dist.png'):
    """Plot similarity score distributions"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Average Similarity Scores', fontsize=16, fontweight='bold')

    models = []
    product_sim = []
    category_sim = []

    if 'product_search' in results:
        for model_name, metrics in results['product_search'].items():
            if model_name not in models:
                models.append(model_name)
            product_sim.append(metrics['avg_similarity'])

    if 'category_search' in results:
        for model_name, metrics in results['category_search'].items():
            category_sim.append(metrics['avg_similarity'])

    x = np.arange(len(models))

    # Product search similarities
    bars1 = ax1.barh(x, product_sim, color=['#2ecc71', '#f39c12'])
    ax1.set_xlabel('Average Similarity Score', fontweight='bold')
    ax1.set_title('Product Search')
    ax1.set_yticks(x)
    ax1.set_yticklabels(models)
    ax1.set_xlim(0, 1)
    ax1.grid(axis='x', alpha=0.3)

    for i, bar in enumerate(bars1):
        width = bar.get_width()
        ax1.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.3f}', ha='left', va='center', fontweight='bold')

    # Category search similarities
    bars2 = ax2.barh(x, category_sim, color=['#2ecc71', '#f39c12'])
    ax2.set_xlabel('Average Similarity Score', fontweight='bold')
    ax2.set_title('Category Search')
    ax2.set_yticks(x)
    ax2.set_yticklabels(models)
    ax2.set_xlim(0, 1)
    ax2.grid(axis='x', alpha=0.3)

    for i, bar in enumerate(bars2):
        width = bar.get_width()
        ax2.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.3f}', ha='left', va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Similarity distribution plot saved to {save_path}")
    return fig


def generate_report(results: Dict, output_file: str = 'comparison_report.txt'):
    """Generate a detailed text report"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("EMBEDDING MODEL COMPARISON REPORT\n")
        f.write("="*80 + "\n\n")

        f.write(f"Evaluation Date: {results.get('timestamp', 'N/A')}\n")
        f.write(f"Number of Products: {results.get('num_products', 'N/A')}\n")
        f.write(f"Number of Categories: {results.get('num_categories', 'N/A')}\n")
        f.write(f"Number of Test Queries: {results.get('num_queries', 'N/A')}\n\n")

        # Product Search Results
        f.write("="*80 + "\n")
        f.write("PRODUCT SEARCH RESULTS\n")
        f.write("="*80 + "\n\n")

        if 'product_search' in results:
            models = list(results['product_search'].keys())

            for model_name, metrics in results['product_search'].items():
                f.write(f"{model_name}:\n")
                f.write(f"  Hit Rate@10:      {metrics['hit_rate']:.1%}\n")
                f.write(f"  MRR:              {metrics['mrr']:.3f}\n")
                f.write(f"  Avg Similarity:   {metrics['avg_similarity']:.3f}\n")
                f.write(f"  Queries Tested:   {metrics['num_queries']}\n\n")

            # Winner analysis
            hit_rates = [results['product_search'][m]['hit_rate'] for m in models]
            mrrs = [results['product_search'][m]['mrr'] for m in models]

            best_hit_idx = np.argmax(hit_rates)
            best_mrr_idx = np.argmax(mrrs)

            f.write("Analysis:\n")
            f.write(f"  Best Hit Rate: {models[best_hit_idx]} ({hit_rates[best_hit_idx]:.1%})\n")
            f.write(f"  Best MRR:      {models[best_mrr_idx]} ({mrrs[best_mrr_idx]:.3f})\n")

            if hit_rates[0] != hit_rates[1]:
                improvement = abs(hit_rates[0] - hit_rates[1]) / min(hit_rates) * 100
                f.write(f"  Hit Rate Improvement: {improvement:.1f}%\n")

            f.write("\n")

        # Category Search Results
        f.write("="*80 + "\n")
        f.write("CATEGORY SEARCH RESULTS\n")
        f.write("="*80 + "\n\n")

        if 'category_search' in results:
            models = list(results['category_search'].keys())

            for model_name, metrics in results['category_search'].items():
                f.write(f"{model_name}:\n")
                f.write(f"  Hit Rate@5:       {metrics['hit_rate']:.1%}\n")
                f.write(f"  MRR:              {metrics['mrr']:.3f}\n")
                f.write(f"  Avg Similarity:   {metrics['avg_similarity']:.3f}\n")
                f.write(f"  Queries Tested:   {metrics['num_queries']}\n\n")

            # Winner analysis
            hit_rates = [results['category_search'][m]['hit_rate'] for m in models]
            mrrs = [results['category_search'][m]['mrr'] for m in models]

            best_hit_idx = np.argmax(hit_rates)
            best_mrr_idx = np.argmax(mrrs)

            f.write("Analysis:\n")
            f.write(f"  Best Hit Rate: {models[best_hit_idx]} ({hit_rates[best_hit_idx]:.1%})\n")
            f.write(f"  Best MRR:      {models[best_mrr_idx]} ({mrrs[best_mrr_idx]:.3f})\n")

            if hit_rates[0] != hit_rates[1]:
                improvement = abs(hit_rates[0] - hit_rates[1]) / min(hit_rates) * 100
                f.write(f"  Hit Rate Improvement: {improvement:.1f}%\n")

            f.write("\n")

        # Recommendations
        f.write("="*80 + "\n")
        f.write("RECOMMENDATIONS\n")
        f.write("="*80 + "\n\n")

        if 'product_search' in results and 'category_search' in results:
            product_models = list(results['product_search'].keys())
            product_scores = [
                results['product_search'][m]['hit_rate'] + results['product_search'][m]['mrr']
                for m in product_models
            ]
            category_scores = [
                results['category_search'][m]['hit_rate'] + results['category_search'][m]['mrr']
                for m in product_models
            ]

            best_product_idx = np.argmax(product_scores)
            best_category_idx = np.argmax(category_scores)

            f.write(f"Best for Product Search: {product_models[best_product_idx]}\n")
            f.write(f"Best for Category Search: {product_models[best_category_idx]}\n\n")

            if best_product_idx == best_category_idx:
                f.write(f"Overall Recommendation: {product_models[best_product_idx]}\n")
                f.write("This model performs best in both product and category search.\n")
            else:
                f.write("Consider:\n")
                f.write(f"  - Use {product_models[best_product_idx]} for product search\n")
                f.write(f"  - Use {product_models[best_category_idx]} for category search\n")
                f.write("  - Or choose based on your primary use case\n")

    print(f"✓ Detailed report saved to {output_file}")


def main():
    """Main visualization execution"""
    print("\n" + "="*80)
    print("EMBEDDING MODEL COMPARISON VISUALIZATION")
    print("="*80 + "\n")

    # Load results
    results = load_results()
    if not results:
        return

    # Create comparison table
    print("Creating comparison table...")
    table = create_comparison_table(results)
    print("\n" + table.to_string(index=False))
    table.to_csv('comparison_table.csv', index=False)
    print("\n✓ Table saved to comparison_table.csv")

    # Create plots
    print("\nGenerating plots...")
    plot_comparison(results)
    plot_similarity_distribution(results)

    # Generate report
    print("\nGenerating detailed report...")
    generate_report(results)

    print("\n" + "="*80)
    print("VISUALIZATION COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  - comparison_table.csv")
    print("  - comparison_plot.png")
    print("  - similarity_dist.png")
    print("  - comparison_report.txt")


if __name__ == "__main__":
    # Update requirements if matplotlib not included
    try:
        import matplotlib
        main()
    except ImportError:
        print("Error: matplotlib not installed")
        print("Install with: pip install matplotlib")
