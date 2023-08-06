
import atexit
import os
import platform
import subprocess
import time
import traceback

from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JError
import exception
from tmp import settings, image


class DRCOptions(object):

    def __init__(self):
        self.imgsize = (480, 320)
        self.activity_range = None
        self.ac50_unit_type = "uM"
        self.ac50_digits = 6
        self.hill_digits = 3


class Connection(object):
    """Bridge class for Java libraries.
    This module behaves as a Singleton instance.
    from cheddar.interface.java import CONNECTION
    """

    def __init__(self):
        self._process = None
        self._gateway = None
        self._start()

    def _start(self):
        cmd = [
            "java", "-jar", settings.JAR_FILE,
            settings.ENTRY_POINT_CLASS
        ]
        jar_cwd = os.getcwd() + settings.JAR_DIR
        if platform.system() == "Windows":
            cmd[0] = "javaw"
        try:
            self._process = subprocess.Popen(cmd, cwd=jar_cwd)
        except OSError:
            print traceback.format_exc()
            raise exception.JavaConnectionError
        print "JVM started: " + str(self._process.pid)
        atexit.register(self.kill)
        time.sleep(2)  # waiting for JVM start up
        try:
            self._gateway = JavaGateway()
        except Py4JError:
            self._process.kill()
            self._process = None
            print "JVM killed: " + str(self._process.pid)
            print traceback.format_exc()
            raise exception.JavaConnectionError

    def restart(self):
        self._start()

    def kill(self):
        """Shutdown gateway and kill JVM subprocess. In the case of Windows,
        python will crash when JVM was killed without closing gateway.
        """
        if self._gateway is not None:
            self._gateway.shutdown()
            self._gateway = None
        if self._process is not None:
            self._process.kill()
            print "JVM killed: " + str(self._process.pid)
            self._process = None

    def is_alive(self):
        """Check JavaGateway is alive"""
        if self._gateway is not None:
            return True
        return False

    def renderMolecule(self, string):
        """Get PNG image of molecule structure by using JChemPaint.

        Args:
          MOLfile format structure data
        Returns:
          bytearray(PNG format) or empty bytearray(if rendering failed)
        """
        return self._gateway.entry_point.renderMolecule(string)

    def get_logical_assays(self):
        """Get logical assay report list through GenedataAPI connection.

        Returns:
          {name: (path, LogicalAssayReportKey object), ...}
        """
        client = self._gateway.entry_point.getClient()
        if client is None:
            return {}
        keys = client.getLogicalAssayKeys()
        client.close()
        results = {}
        for k in keys:
            results[k.getLogicalAssayName()] = (k.getFolderName(), k)
        return results

    def get_drc_data(self, logical_assay_key, compounds, options=DRCOptions()):
        """Get logical assay report list through GenedataAPI connection.

        Returns:
          {name: (path, LogicalAssayReportKey object), ...}
        """
        drc_results = {}
        ac50_results = {}
        hill_results = {}
        client = self._gateway.entry_point.getClient()
        if client is None:
            return []
        report = client.getLogicalAssayReport(logical_assay_key)
        drc_data = report.readLogicalAssayDRCData()
        for compound in compounds:
            idx = None
            for i in range(drc_data.getCompoundCount()):
                if compound == drc_data.getCompoundId(i):
                    idx = i
                    break
            if idx is None:
                drc_results[compound] = image.render_text(
                    "", options.imgsize, "Sans 12", (0, 0, 0))
                ac50_results[compound] = ""
                hill_results[compound] = ""
                continue
            request = drc_data.createDRCImageRequest(idx)
            prop = drc_data.getDRCData(idx)
            request.setImageSize(*options.imgsize)
            if options.activity_range:
                request.setActivityRange(
                    client.getRange(*options.activity_range))
            img = request.performRequest()
            if options.ac50_unit_type == "uM":
                ac50form = "{{0:.{}f}}".format(options.ac50_digits)
                ac50 = ac50form.format(prop.getLinearAC50() * 1000000)
            elif options.ac50_unit_type == "nM":
                ac50form = "{{0:.{}f}}".format(options.ac50_digits)
                ac50 = ac50form.format(prop.getLinearAC50() * 1000000000)
            elif options.ac50_unit_type == "log":
                ac50form = "{{0:.{}e}}".format(options.ac50_digits)
                ac50 = ac50form.format(prop.getLinearAC50())
            else:
                raise ValueError
            hillform = "{{0:.{}f}}".format(options.hill_digits)
            hill = hillform.format(prop.getHillCoefficient())
            if str(ac50) == "nan":
                ac50 = "n.d."
            if str(hill) == "nan":
                hill = "n.d."
            drc_results[compound] = img
            ac50_results[compound] = ac50
            hill_results[compound] = hill
        client.close()
        return [drc_results, ac50_results, hill_results]

"""JavaGateway connection instance"""
CONNECTION = Connection()
