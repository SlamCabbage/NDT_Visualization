# NDT_Visualization

## How to use
Change the file directory in the two lines to your own

    ```
    rviz_process = subprocess.Popen(['rviz', '-d', 'path/to/my.rviz'])
    with open('path/to/demo.txt', 'r') as f:
    ```

then

    ```
    python3 plotNormalDistribution.py
    ```

## Example

<p align="center"><img width="800" alt="image" src="figure/ndt.png">

