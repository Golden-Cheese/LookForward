import sciter, sys
from sciter.capi.scdom import HELEMENT

import model


"""More complex PySciter sample."""

import sciter

# main frame
class Frame(sciter.Window):
    def __init__(self):
        super().__init__(ismain=True, uni_theme=True)
        pass

    def on_subscription(self, groups):
        # subscribing only for scripting calls and document events
        from sciter.event import EVENT_GROUPS
        return EVENT_GROUPS.HANDLE_BEHAVIOR_EVENT | EVENT_GROUPS.HANDLE_SCRIPTING_METHOD_CALL

    def on_script_call(self, name, args):
        # script calls
        print(name, "called from script")
        return self.dispatch(name, args)


    ## @name The following functions are called from scripts:
    @sciter.script
    def PythonCall(self, arg):
        return "Pythonic window (%s)" % str(arg)

    @sciter.script
    def gotoprojects(self):
        self.load_file(os.path.join(os.path.dirname(__file__), 'projects.htm'))

    @sciter.script
    def gotohome(self):
        self.load_file(os.path.join(os.path.dirname(__file__), 'main.htm'))

    @sciter.script
    def gotopeople(self):
        pass

    # @sciter.script
    # def GetNativeApi(self):
    #
    #     def on_add(a, b):
    #         return a + b
    #
    #     def on_sub(a, b):
    #         raise Exception("sub(%d,%d) raised exception" % (a, b))
    #
    #     api = { 'add': on_add,              # plain function
    #             'sub': on_sub,              # raised exception will propagated to script
    #             'mul': lambda a,b: a * b,   # lambdas support
    #             }
    #     return api

    ## @}

# end


if __name__ == '__main__':
    sciter.runtime_features(allow_sysinfo=True)

    import os
    htm = os.path.join(os.path.dirname(__file__), 'main.htm')
    frame = Frame()
    frame.load_file(htm)
frame.run_app()