import sciter, sys
from sciter.capi.scdom import HELEMENT

import model


"""More complex PySciter sample."""

import sciter
import asyncio

# main frame
class Frame(sciter.Window):
    def __init__(self, model):
        super().__init__(ismain=True, uni_theme=True)
        self.model=model

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
    def queryProjects(self):
        return list(self.model.projects)

    @sciter.script
    def queryPeople(self):
        return list(self.model.people)

    def camcellcurrenttask(self):
        # todo ; make every call async, and cancellable
        asyncio.current_task().cancel()
        #todo: make sure in task to properly exit, letting it interrupt the main
        # phase, but using try catche during the clusing end phase to ignore a camcel/ask for cancel confirmation if
        # the work was done and was about to be displayed

    @sciter.script
    def asyncioqueryProjects(self):
        # fixme : how to add callback that warns Sciter that the data is ready ?
        qp_task = asyncio.get_event_loop().create_task(self.model.investments)
        qp_task.add_done_callback(self.call_function("onProjectBackendAnswer", None))
        asyncio.get_event_loop().run_until_complete(qp_task)

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
    m = model.Model_Lazy()
    import os
    htm = os.path.join(os.path.dirname(__file__), 'main.htm')
    frame = Frame(model=m)
    frame.load_file(htm)
    frame.run_app()
