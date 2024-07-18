import os
import sys
import importlib
import ida_idaapi

my_dirname, _ = os.path.split(__file__)

class PluginManager(ida_idaapi.plugin_t):
    flags = 0
    comment = "Allows for dynamically re-loading script files"
    help = ""
    wanted_name = "Plugin Manager"
    wanted_hotkey = "Ctrl-r"
    
    def __init__(self):
        self.plugins = dict()
        pass

    def load_plugin(self, plugin_name):
        if not isinstance(plugin_name, str):
            print("[plugin manager] load_plugin requires a string")
        try:
            if plugin_name in sys.modules:
                self.plugins[plugin_name].on_unload()
                importlib.reload(sys.modules[plugin_name])
            else:
                importlib.import_module(plugin_name)
        except Exception as e:
            print(f"[plugin manager] Exception: {repr(e)}")
            pass

        if plugin_name not in sys.modules:
            return
                
        module = sys.modules[plugin_name]
        try:
            plugin_class = getattr(module, "Plugin")
            instance = plugin_class()
            self.plugins[plugin_name] = instance
            instance.on_load()
        except Exception as e:
            print(f"[plugin manager] Exception: {repr(e)}")
            pass
        return

    def unload_plugin(self, plugin_name):
        if not isinstance(plugin_name, str):
            print("[plugin manager] load_plugin requires a string")
        
        if plugin_name not in self.plugins:
            return
        if plugin_name not in sys.modules:
            return

        self.plugins[plugin_name].on_unload()
        del sys.modules[plugin_name]
        del self.plugins[plugin_name]
        
    def init(self):
        try:
            modules_path = os.path.join(my_dirname, "pm-plugins")
            if not modules_path in sys.path:
                sys.path.append(modules_path)
            for filename in os.listdir(modules_path):
                if not (filename.startswith("plugin_") and filename.endswith(".py")):
                    continue
                plugin_name = filename[:-3]
                self.load_plugin(plugin_name)
        except Exception as e:
            print(f"[plugin manager] Exception: {repr(e)}")
            pass
            
        return ida_idaapi.PLUGIN_KEEP

    def run(self, arg):
        for name in self.plugins:
            self.load_plugin(name)
        return True

    def term(self):
        pass

plugin_manager = PluginManager()
def PLUGIN_ENTRY():
    global plugin_manager
    return plugin_manager
