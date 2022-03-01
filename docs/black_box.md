# Black-box models

```python
from physicool.optimization import PhysiCellBlackBox

# Create a black box model based on a PhysiCell executable
# The black box updates the input parameters, runs the executable and returns the cell data
bbox = PhysiCellBlackBox(project_name="project", project_path=Path("../tests/PhysiCell"))
bbox.run()
```
