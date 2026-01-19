def convex_hull(points):
    """
    Compute convex hull using Graham Scan algorithm.
    Returns points in counter-clockwise order.
    """
    def cross(o, a, b):
        # Cross product to determine turn direction
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    # Sort points lexicographically (by x, then by y)
    points = sorted(set(points))
    
    if len(points) <= 1:
        return points
    
    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    
    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    
    # Remove last point of each half because it's repeated
    return lower[:-1] + upper[:-1]


# Example usage
if __name__ == "__main__":
    points = [
        (0, 3), (1, 1), (2, 2), (4, 4),
        (0, 0), (1, 2), (3, 1), (3, 3)
    ]
    
    hull = convex_hull(points)
    print("Convex Hull Points:")
    for point in hull:
        print(f"  {point}")
    
    # Visualize (optional - requires matplotlib)
    try:
        import matplotlib.pyplot as plt
        
        # Plot all points
        x, y = zip(*points)
        plt.scatter(x, y, c='blue', label='All Points')
        
        # Plot hull
        hull_x, hull_y = zip(*hull)
        hull_x += (hull_x[0],)  # Close the polygon
        hull_y += (hull_y[0],)
        plt.plot(hull_x, hull_y, 'r-', linewidth=2, label='Convex Hull')
        plt.scatter(hull_x[:-1], hull_y[:-1], c='red', s=100, zorder=5)
        
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.title('Convex Hull')
        plt.show()
    except ImportError:
        print("\nInstall matplotlib to see visualization: pip install matplotlib")