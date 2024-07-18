# ida-plugin-plugin
Plugins for plugins

"ida-plugin-plugin" goes in `<ida plugin directory>/`  
Plugins for "ida-plugin-plugin" go in `<ida plugin directory>/pm-plugins/`  

## Example

```py
import ida_hexrays

class Optimizer(ida_hexrays.optinsn_t):
    def func(self, blk, ins):
        if blk.mba.maturity != ida_hexrays.MMAT_GLBOPT1:
            return 0
        print(f"minsn: {ins.dstr()}")
        return 0

class Plugin:
    def __init__(self):
        self.optimizer = Optimizer()
        pass

    def on_load(self):
        self.optimizer.install()

    def on_unload(self):
        self.optimizer.remove()
```
