#!/usr/local/bin/python
# encoding: utf-8
"""
*Import tmp_sdss catagloue from plain text file*

:Author:
    David Young

:Date Created:
    August 25, 2015

.. todo::
    
    @review: when complete pull all general functions and classes into dryxPython

# xdocopt-usage-tempx
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
from ._base_importer import _base_importer


class tmp_sdss(_base_importer):

    """
    *The worker class for the tmp_sdss module*

    **Key Arguments:**
        - ``dbConn`` -- mysql database connection
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``pathToDataFIle`` -- path to the tmp_sdss data file
        - ``version`` -- version of the tmp_sdss catalogue


    .. todo::

        - @review: when complete, clean tmp_sdss class
        - @review: when complete add logging
        - @review: when complete, decide whether to abstract class to another module
    """
    # Initialisation
    # 1. @flagged: what are the unique attrributes for each object? Add them
    # to __init__

    # 4. @flagged: what actions does each object have to be able to perform? Add them here
    # Method Attributes
    def get(self):
        """
        *get the tmp_sdss object*

        **Return:**
            - ``tmp_sdss``

        .. todo::

            - @review: when complete, clean get method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get`` method')

        self.dbTableName = self.catalogueName
        self.primaryIdColumnName = "qubPrimaryId"
        self.raColName = "ra"
        self.declColName = "dec_"

        # self.dictList = self.create_dictionary_of_tmp_sdss()
        # self.add_data_to_database_table()
        self.create_master_id()
        self.set_master_obj_types()

        # self.add_htmids_to_database_table()

        self.log.info('completed the ``get`` method')
        return tmp_sdss

    def create_master_id(
            self):
        """
        *create master id*

        **Key Arguments:**
            # -

        **Return:**
            - None

        .. todo::

            - @review: when complete, clean create_master_id method
            - @review: when complete add logging
        """
        self.log.info('starting the ``create_master_id`` method')

        batchSize = 1250
        t = self.dbTableName

        if "photo" in t:
            totalRows = 500000000
        else:
            sqlQuery = u"""
                select distinct objId from %(t)s where qubMasterFlag = 2
            """ % locals()
            count = dms.execute_mysql_read_query(
                sqlQuery=sqlQuery,
                dbConn=self.cataloguesDbConn,
                log=self.log
            )
            totalRows = len(count)
        count = ""

        total = totalRows
        batches = int(total / batchSize)

        start = 0
        end = 0
        theseBatches = []
        for i in range(batches):
            end = end + batchSize
            if end > total:
                end = total
            start = i * batchSize

            if start > 1:
                # Cursor up one line and clear line
                sys.stdout.write("\x1b[1A\x1b[2K")
            percent = (float(end) / float(totalRows)) * 100.
            print "%(end)s / %(totalRows)s (%(percent)1.1f%%) masterFlags updated in %(t)s" % locals()

            sqlQuery = u"""
                select distinct objid from %(t)s where qubMasterFlag = 2 limit 0, %(batchSize)s  
            """ % locals()

            rows = dms.execute_mysql_read_query(
                sqlQuery=sqlQuery,
                dbConn=self.cataloguesDbConn,
                log=self.log
            )
            sqlQuery = ""
            for row in rows:
                objid = row["objid"]
                sqlQuery = sqlQuery + \
                    u"""\nupdate %(t)s set qubMasterFlag = 1 where qubPrimaryId = (select * from (SELECT qubPrimaryId FROM %(t)s where objId = %(objid)s  order by clean desc limit 1) as alias);
update %(t)s set qubMasterFlag = 0 where objId = %(objid)s  and qubMasterFlag != 1;""" % locals()

            dms.execute_mysql_write_query(
                sqlQuery=sqlQuery,
                dbConn=self.cataloguesDbConn,
                log=self.log,
                Force=False
            )

        self.log.info('completed the ``create_master_id`` method')
        return None

    # use the tab-trigger below for new method
    def set_master_obj_types(
            self):
        """
        *set master obj types*

        **Key Arguments:**
            # -

        **Return:**
            - None

        .. todo::

            - @review: when complete, clean set_master_obj_types method
            - @review: when complete add logging
        """
        self.log.info('starting the ``set_master_obj_types`` method')

        batchSize = 1250
        t = self.dbTableName

        if "photo" in t:
            totalRows = 500000000
            return
        else:
            sqlQuery = u"""
                select distinct objid from %(t)s  where objType = "Q"
            """ % locals()
            count = dms.execute_mysql_read_query(
                sqlQuery=sqlQuery,
                dbConn=self.cataloguesDbConn,
                log=self.log
            )
            totalRows = len(count)
        count = ""

        total = totalRows
        batches = int(total / batchSize)

        start = 0
        end = 0
        theseBatches = []
        for i in range(batches):
            end = end + batchSize
            if end > total:
                end = total
            start = i * batchSize

            if start > 1:
                # Cursor up one line and clear line
                sys.stdout.write("\x1b[1A\x1b[2K")
            percent = (float(end) / float(totalRows)) * 100.
            print "%(end)s / %(totalRows)s (%(percent)1.1f%%) master objIds updated in %(t)s" % locals()

            sqlQuery = u"""
                select distinct objid from %(t)s  where objType = "Q" limit %(start)s , %(batchSize)s  
            """ % locals()

            rows = dms.execute_mysql_read_query(
                sqlQuery=sqlQuery,
                dbConn=self.cataloguesDbConn,
                log=self.log
            )
            sqlQuery = ""
            for row in rows:
                objid = row["objid"]
                sqlQuery = sqlQuery + \
                    u"""\nupdate %(t)s set objType = "Q" where objId = %(objid)s;""" % locals(
                    )

            dms.execute_mysql_write_query(
                sqlQuery=sqlQuery,
                dbConn=self.cataloguesDbConn,
                log=self.log,
                Force=False
            )

        self.log.info('completed the ``set_master_obj_types`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method

if __name__ == '__main__':
    main()
