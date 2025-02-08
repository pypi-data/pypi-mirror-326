#!/usr/bin/env python
"""
_Builder_

Interface definition for Step Builder implementations

"""
from __future__ import print_function

from builtins import object
import logging

import WMCore.WMSpec.Steps.BuildTools as BuildTools
from WMCore.WMSpec.ConfigSectionTree import nodeName

taskSpaceInit = "#!/usr/bin/env python\n"
taskSpaceInit += "# StepSpace Init module for Step\n"
taskSpaceInit += "# Autogenerated by WMCore.WMSpec.Steps.Builder\n"
taskSpaceInit += "\n__all__ = []\n\n"
taskSpaceInit += "from WMCore.WMRuntime.Bootstrap import establishStepSpace\n\n"
taskSpaceInit += "def _Locator():\n"
taskSpaceInit += "    pass\n\n"
taskSpaceInit += "args = {}\n"


class Builder(object):
    """
    _Builder_

    base interface for any WMStep Builder

    """

    def __init__(self):
        self.taskName = None
        self.stepName = None
        self.stepDir = None
        self.taskSpaceInitMod = None

    def __call__(self, step, taskName, workingDirectory, **args):
        """
        _operator(step)_


        """
        self.stepName = nodeName(step)
        self.taskName = taskName
        self.coreBuild(step, workingDirectory)
        self.build(step, workingDirectory, **args)

    def coreBuild(self, step, workingDirectory):
        """
        _coreBuild_

        Build standard stuff that is common to all jobs

        """
        logging.info("%s.coreBuild invoked", self.__class__.__name__)
        dirs = BuildTools.makeDirectory(step)
        dirs.create(workingDirectory)
        self.stepDir = "%s/%s" % (workingDirectory, self.stepName)
        #
        # Install the basic __init__.py module into the step
        # directory

        self.taskSpaceInitMod = "%s/__init__.py" % self.stepDir

        with open(self.taskSpaceInitMod, 'w') as handle:
            handle.write(taskSpaceInit)
            handle.write("""args["TaskName"] = "%s"\n""" % self.taskName)
            handle.write("""args["StepName"] = "%s"\n""" % self.stepName)
            handle.write("""args["Locator"] = _Locator\n""")
            handle.write("""stepSpace = establishStepSpace(**args)\n""")

    def build(self, step, workingDirectory, **args):
        """
        _build_

        Build the step into the working area provided
        args is for all the things we havent thought of yet

        """
        msg = "WMSpec.Steps.Builder.build method not overridden in "
        msg += "implementation: %s\n" % self.__class__.__name__
        raise NotImplementedError(msg)

    def installWorkingArea(self, step, workingArea, **args):
        """
        _installWorkingArea_

        Install working directory information into the step in a standard
        way.

        """
        step.section_("builder")
        step.builder.workingDir = workingArea
        return
