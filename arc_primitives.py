import numpy as np
from scipy.ndimage import label

class GridPrimitives:
    """
    A collection of static methods for performing fundamental transformations on 2D grids,
    specifically designed for use in the ARC solver.
    """

    @staticmethod
    def rotate_90(grid: np.ndarray) -> np.ndarray:
        """
        Rotates the grid 90 degrees clockwise.

        Parameters:
        grid (np.ndarray): A 2D NumPy array representing the grid.

        Returns:
        np.ndarray: The rotated grid.
        """
        return np.rot90(grid, -1)

    @staticmethod
    def reflect_horizontal(grid: np.ndarray) -> np.ndarray:
        """
        Mirrors the grid along the horizontal (X) axis (top-to-bottom).

        Parameters:
        grid (np.ndarray): A 2D NumPy array representing the grid.

        Returns:
        np.ndarray: The horizontally reflected grid.
        """
        return np.flipud(grid)

    @staticmethod
    def crop_to_content(grid: np.ndarray, bg_color: int = 0) -> np.ndarray:
        """
        Finds the bounding box of non-background pixels (color != bg_color) and crops the grid to that area.
        If the grid is entirely background, returns a single 1x1 grid of the background color.

        Parameters:
        grid (np.ndarray): A 2D NumPy array representing the grid.
        bg_color (int): The background color (default is 0).

        Returns:
        np.ndarray: The cropped grid.
        """
        rows, cols = np.where(grid != bg_color)
        if rows.size == 0 or cols.size == 0:
            return np.array([[bg_color]])
        row_min, row_max = rows.min(), rows.max()
        col_min, col_max = cols.min(), cols.max()
        return grid[row_min:row_max + 1, col_min:col_max + 1]

    @staticmethod
    def find_largest_object(grid: np.ndarray, bg_color: int = 0) -> np.ndarray:
        """
        Identifies connected components of non-background pixels and returns a grid containing
        only the largest connected object. Other non-background pixels are set to the background color.

        Parameters:
        grid (np.ndarray): A 2D NumPy array representing the grid.
        bg_color (int): The background color (default is 0).

        Returns:
        np.ndarray: A grid with only the largest connected object.
        """
        labeled_grid, num_features = label(grid != bg_color)
        if num_features == 0:
            return grid.copy()

        max_area = 0
        largest_label = 0
        for label_id in range(1, num_features + 1):
            area = np.sum(labeled_grid == label_id)
            if area > max_area:
                max_area = area
                largest_label = label_id

        result = np.where(labeled_grid == largest_label, grid, bg_color)
        return result

    @staticmethod
    def fill_borders(grid: np.ndarray, border_color: int) -> np.ndarray:
        """
        Expands the grid by one pixel on all sides, filling the new border with the specified color.

        Parameters:
        grid (np.ndarray): A 2D NumPy array representing the grid.
        border_color (int): The color of the border.

        Returns:
        np.ndarray: The grid with borders added.
        """
        new_shape = (grid.shape[0] + 2, grid.shape[1] + 2)
        bordered_grid = np.full(new_shape, border_color, dtype=grid.dtype)
        bordered_grid[1:-1, 1:-1] = grid
        return bordered_grid
