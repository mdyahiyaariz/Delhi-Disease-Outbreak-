"""Utility functions for output formatting and reporting."""

import numpy as np


def print_header(title):
    """Print a formatted section header."""
    print('=' * 60)
    print(title)
    print('=' * 60)


def print_summary(summary):
    """Print pipeline summary statistics."""
    print('\n' + '=' * 60)
    print('PIPELINE SUMMARY REPORT')
    print('=' * 60)
    for name, value in summary.items():
        print(f'   {name:<28}: {value}')


def format_alert(alert):
    """Format a single alert for display."""
    z = alert.get('z_score', float('nan'))
    z_str = f'{z:.2f}' if not (isinstance(z, float) and np.isnan(z)) else 'N/A'
    return f"""
        ⚠️  OUTBREAK ALERT
        Disease   : {alert['disease']}
        Cluster   : {alert['cluster_id']}
        Location  : ({alert['centroid_lat']:.4f}, {alert['centroid_lon']:.4f})
        Period    : {alert['time_window']}
        Cases     : {int(alert['case_count'])}
        LLR Score : {alert['llr']}
        Z-Score   : {z_str}
        """
