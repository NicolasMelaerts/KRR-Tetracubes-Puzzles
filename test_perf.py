import subprocess
import time
import statistics
import os
import matplotlib.pyplot as plt
import numpy as np

def run_command_and_measure(command, num_runs=5):
    """Run a command multiple times and measure execution time"""
    times = []
    
    print(f"Running command: {command}")
    for i in range(num_runs):
        print(f"  Run {i+1}/{num_runs}...", end="", flush=True)
        start_time = time.time()
        
        # Run the command and redirect output to a temporary file
        with open("temp_solution.txt", "w") as outfile:
            process = subprocess.run(command, shell=True, stdout=outfile, stderr=subprocess.PIPE)
        
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
        print(f" {elapsed_time:.3f} seconds")
        
        # Check if the command was successful
        if process.returncode != 0:
            print(f"  Error in run {i+1}: {process.stderr.decode('utf-8')}")
            # Continue with the next run instead of stopping
    
    # Clean up temporary file
    if os.path.exists("temp_solution.txt"):
        os.remove("temp_solution.txt")
        
    return times

def create_comparison_plots(times_list, cmd_names, cells_info, tetracubes_info):
    """Create comparison plots for the execution times"""
    # Calculate statistics
    avgs = [statistics.mean(times) for times in times_list]
    
    # Create figure with multiple subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # 1. Bar chart for average times
    bars = ax1.bar(cmd_names, avgs, color=['#3498db', '#e74c3c'])
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Average Execution Time')
    
    # Add values on top of bars
    for i, v in enumerate(avgs):
        ax1.text(i, v + 0.1, f"{v:.3f}s", ha='center')
    
    # 2. Box plot for distribution
    ax2.boxplot(times_list, labels=cmd_names)
    ax2.set_ylabel('Time (seconds)')
    ax2.set_title('Execution Time Distribution')
    
    # 3. Line plot for individual runs
    runs = list(range(1, len(times_list[0]) + 1))
    colors = ['#3498db', '#e74c3c']
    
    for i, times in enumerate(times_list):
        ax3.plot(runs, times, 'o-', label=f"{cmd_names[i]}", color=colors[i])
    
    ax3.set_xlabel('Run Number')
    ax3.set_ylabel('Time (seconds)')
    ax3.set_title('Execution Time per Run')
    ax3.legend()
    ax3.grid(True, linestyle='--', alpha=0.7)
    
    # Add overall title with cell and tetracube info
    plt.suptitle(f'Performance Comparison: PUZZLE.lp ({cells_info[0]} cells, {tetracubes_info[0]} tetracubes) vs ' +
                f'PUZZLE_COMPLEX.lp ({cells_info[1]} cells, {tetracubes_info[1]} tetracubes)', fontsize=14)
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)
    
    # Save the figure
    plt.savefig('clingo_performance_comparison.png', dpi=300)
    print("\nGraph saved as 'clingo_performance_comparison.png'")
    
    # Show the plot
    plt.show()

def main():
    # Commands to compare - adding output redirection to solution.txt
    cmd1 = "clingo PUZZLE.lp -c grid_type=3 -c num_hints=3 --seed=42"
    cmd2 = "clingo PUZZLE_COMPLEX.lp -c grid_type=3 -c num_hints=3 --seed=42"
    
    cmd1_name = "PUZZLE.lp"
    cmd2_name = "PUZZLE_COMPLEX.lp"
    
    # Information about cells and tetracubes for each command
    cells_info = [32, 64]  # 32 cells for PUZZLE.lp, 64 cells for PUZZLE_COMPLEX.lp
    tetracubes_info = [8, 16]  # 8 tetracubes for PUZZLE.lp, 16 tetracubes for PUZZLE_COMPLEX.lp
    
    # Number of runs for each command
    num_runs = 20
    
    print("=== Performance Comparison ===")
    print(f"Each command will be run {num_runs} times\n")
    
    # Run first command
    print("\n=== Command 1 ===")
    times1 = run_command_and_measure(cmd1, num_runs)
    
    # Run second command
    print("\n=== Command 2 ===")
    times2 = run_command_and_measure(cmd2, num_runs)
    
    # Calculate statistics
    avg1 = statistics.mean(times1)
    avg2 = statistics.mean(times2)
    
    median1 = statistics.median(times1)
    median2 = statistics.median(times2)
    
    if len(times1) > 1:
        stdev1 = statistics.stdev(times1)
        stdev2 = statistics.stdev(times2)
    else:
        stdev1 = stdev2 = 0
    
    # Print results
    print("\n=== Results ===")
    print(f"Command 1 ({cmd1_name}) - {cells_info[0]} cells, {tetracubes_info[0]} tetracubes:")
    print(f"  Average: {avg1:.3f} seconds")
    print(f"  Median: {median1:.3f} seconds")
    print(f"  Std Dev: {stdev1:.3f} seconds")
    print(f"  All times: {[round(t, 3) for t in times1]}")
    
    print(f"\nCommand 2 ({cmd2_name}) - {cells_info[1]} cells, {tetracubes_info[1]} tetracubes:")
    print(f"  Average: {avg2:.3f} seconds")
    print(f"  Median: {median2:.3f} seconds")
    print(f"  Std Dev: {stdev2:.3f} seconds")
    print(f"  All times: {[round(t, 3) for t in times2]}")
    
    # Compare
    ratio = avg2 / avg1 if avg1 > 0 else float('inf')
    diff = avg2 - avg1
    
    print("\n=== Comparison ===")
    if avg1 < avg2:
        print(f"{cmd1_name} is faster than {cmd2_name} by {diff:.3f} seconds ({ratio:.2f}x)")
    elif avg2 < avg1:
        print(f"{cmd2_name} is faster than {cmd1_name} by {-diff:.3f} seconds ({1/ratio:.2f}x)")
    else:
        print(f"{cmd1_name} and {cmd2_name} have the same average execution time")
    
    # Create and display comparison plots
    create_comparison_plots([times1, times2], [cmd1_name, cmd2_name], cells_info, tetracubes_info)

if __name__ == "__main__":
    main()