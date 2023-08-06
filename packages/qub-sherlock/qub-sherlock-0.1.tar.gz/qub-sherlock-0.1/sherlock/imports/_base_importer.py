#!/usr/local/bin/python
# encoding: utf-8
"""
*The base importer for sherlock imports*

:Author:
    David Young

:Date Created:
    August 25, 2015

.. todo::
    
    @review: when complete pull all general functions and classes into dryxPython
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
import codecs
import string

import re
from docopt import docopt
from dryxPython import mysql as dms
from dryxPython import logs as dl
from dryxPython import commonutils as dcu
from fundamentals import tools, times
# from ..__init__ import *


class _base_importer():

    """
    *The worker class for the _base_importer module*

    **Key Arguments:**
        - ``dbConn`` -- mysql database connection
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``pathToDataFIle`` -- path to the _base_importer data file
        - ``version`` -- version of the _base_importer catalogue
        - ``catalogueName`` -- name of the catalogue
        - ``coordinateList`` -- list of coordinates (needed for some streamed tables)
        - ``cataloguesDbConn`` -- catalogues database connection (default false - will be setup here if false)


    .. todo::

        - @review: when complete, clean _base_importer class
        - @review: when complete add logging
        - @review: when complete, decide whether to abstract class to another module
    """
    # Initialisation
    # 1. @flagged: what are the unique attrributes for each object? Add them
    # to __init__

    def __init__(
            self,
            log,
            settings=False,
            pathToDataFile=False,
            version=False,
            catalogueName="",
            coordinateList=[],
            cataloguesDbConn=False
    ):
        self.log = log
        log.debug("instansiating a new '_base_importer' object")
        self.settings = settings
        self.pathToDataFile = pathToDataFile
        self.version = version
        self.catalogueName = catalogueName
        self.coordinateList = coordinateList
        self.cataloguesDbConn = cataloguesDbConn

        # xt-self-arg-tmpx

        # INITIAL ACTIONS
        # SETUP DATABASE CONNECTIONS
        if cataloguesDbConn == False:
            from sherlock import database
            db = database(
                log=self.log,
                settings=self.settings
            )
            self.transientsDbConn, self.cataloguesDbConn, self.pmDbConn = db.get()

        if pathToDataFile:
            pathToReadFile = pathToDataFile
            try:
                self.log.debug("attempting to open the file %s" %
                               (pathToReadFile,))
                readFile = codecs.open(pathToReadFile, mode='r')
                self.catData = readFile.read()
                readFile.close()
            except IOError, e:
                message = 'could not open the file %s' % (pathToReadFile,)
                self.log.critical(message)
                raise IOError(message)
            readFile.close()
        else:
            self.catData = None

        # BUILD VERSION TEXT
        if self.version:
            self.version = "_v" + \
                self.version.replace(" ", "").replace(
                    "v", "").replace(".", "_")
        else:
            self.version = ""
        version = self.version

        # BUILD THE DATABASE TABLE NAME
        self.dbTableName = "tcs_cat_%(catalogueName)s%(version)s" % locals()
        self.primaryIdColumnName = "primaryId"
        self.databaseInsertbatchSize = 2500
        self.raColName = "raDeg"
        self.declColName = "decDeg"
        self.uniqueKeyList = [self.raColName, "decDeg"]

        return None

    # Method Attributes
    def get(self):
        """
        *get the _base_importer object*

        **Return:**
            - ``_base_importer``

        .. todo::

            - @review: when complete, clean get method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get`` method')

        # self.dictList = self.create_dictionary_of__base_importer()
        # self.add_data_to_database_table()
        self.add_htmids_to_database_table()

        self.log.info('completed the ``get`` method')
        return _base_importer

    def create_dictionary_of__base_importer(
            self):
        """
        *create dictionary of _base_importer*

        **Key Arguments:**
            # -

        **Return:**
            - None

        .. todo::

            - @review: when complete, clean create_dictionary_of__base_importer method
            - @review: when complete add logging
        """
        self.log.info(
            'starting the ``create_dictionary_of__base_importer`` method')

        dictList = []
        lines = string.split(self.catData, '\n')
        inserts = [
            11, 25, 51, 57, 64, 71, 75, 78, 81, 89, 97, 106, 110, 134, 158, 181]
        keys = ["raDeg", "decDeg", "name", "descrip", "rmag", "bmag", "comment", "r_psf_class", "b_psf_class", "z",
                "src_cat_name", "src_cat_z", "qso_prob", "x_name", "r_name", "alt_id1", "alt_id2"]

        totalCount = len(lines)
        count = 0

        for line in lines:
            count += 1
            if count > 1:
                # Cursor up one line and clear line
                sys.stdout.write("\x1b[1A\x1b[2K")
            if count > totalCount:
                count = totalCount
            print "%(count)s / %(totalCount)s _base_importer data added to memory" % locals()

            thisDict = {}
            for insert in inserts:
                line.replace("–", "-")
                line = line[:insert] + "|" + line[insert:]

            theseValues = string.split(line, '|')
            for k, v in zip(keys, theseValues):
                v = v.strip()
                if len(v) == 0 or v == "-":
                    v = None
                thisDict[k] = v
            dictList.append(thisDict)

        self.log.info(
            'completed the ``create_dictionary_of__base_importer`` method')
        return dictList

    # use the tab-trigger below for new method
    def add_data_to_database_table(
            self):
        """
        *add data to database table*

        **Key Arguments:**
            # -

        **Return:**
            - None

        .. todo::

            - @review: when complete, clean add_data_to_database_table method
            - @review: when complete add logging
        """
        self.log.info('starting the ``add_data_to_database_table`` method')

        dms.insert_list_of_dictionaries_into_database(
            dbConn=self.cataloguesDbConn,
            log=self.log,
            dictList=self.dictList,
            dbTableName=self.dbTableName,
            uniqueKeyList=self.uniqueKeyList,
            batchSize=self.databaseInsertbatchSize
        )

        self.log.info('completed the ``add_data_to_database_table`` method')
        return None

    # use the tab-trigger below for new method
    def add_htmids_to_database_table(
            self):
        """
        *add htmids to database table*

        **Key Arguments:**
            # -

        **Return:**
            - None

        .. todo::

            - @review: when complete, clean add_htmids_to_database_table method
            - @review: when complete add logging
        """
        self.log.info('starting the ``add_htmids_to_database_table`` method')

        tableName = self.dbTableName
        print "Adding HTMIds to %(tableName)s" % locals()

        from dryxPython import mysql as dms
        dms.add_HTMIds_to_mysql_tables.add_HTMIds_to_mysql_tables(
            raColName=self.raColName,
            declColName=self.declColName,
            tableName=self.dbTableName,
            dbConn=self.cataloguesDbConn,
            log=self.log,
            primaryIdColumnName=self.primaryIdColumnName
        )

        self.log.info('completed the ``add_htmids_to_database_table`` method')
        return None

    def _update_database_helper_table(
            self):
        """
        *update dataasbe helper table*

        **Key Arguments:**
            # -

        **Return:**
            - None

        .. todo::

            - @review: when complete, clean _update_database_helper_table method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_update_database_helper_table`` method')

        tableName = self.dbTableName

        sqlQuery = u"""
            update tcs_helper_catalogue_tables_info set last_updated = now() where table_name = "%(tableName)s";
        """ % locals()

        dms.execute_mysql_write_query(
            sqlQuery=sqlQuery,
            dbConn=self.cataloguesDbConn,
            log=self.log
        )

        self.log.info('completed the ``_update_database_helper_table`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method
