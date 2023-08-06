#!/usr/local/bin/python
# encoding: utf-8
"""
*The classifier object for Sherlock*

:Author:
    David Young

:Date Created:
    June 29, 2015

:Notes:
    - If you have any questions requiring this script/module please email me: d.r.young@qub.ac.uk
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
import time
import MySQLdb as ms
from docopt import docopt
from dryxPython import logs as dl
from dryxPython import commonutils as dcu
from dryxPython import mysql as dms
from fundamentals import tools, times
from sherlock.update_ned_stream import update_ned_stream


class classifier():

    """
    *The classifier object for Sherlock*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``update`` -- update the transient database with crossmatch results (boolean)
    """
    # INITIALISATION

    def __init__(
            self,
            log,
            settings=False,
            update=False
    ):
        self.log = log
        log.debug("instansiating a new 'classifier' object")
        self.settings = settings
        self.update = update
        # xt-self-arg-tmpx

        # VARIABLE DATA ATRRIBUTES
        self.transientsMetadataList = []

        # INITIAL ACTIONS
        # SETUP DATABASE CONNECTIONS
        from sherlock import database
        db = database(
            log=self.log,
            settings=self.settings
        )
        self.transientsDbConn, self.cataloguesDbConn, self.pmDbConn = db.get()
        self.crossmatchTablename = self.settings[
            "database settings"]["transients"]["crossmatchTable"]

        return None

    # METHOD ATTRIBUTES

    def get(self):
        """
        *perform the classifications*
        """
        self.log.debug('starting the ``get`` method')

        self._create_crossmatch_table_if_not_existing()
        self._grab_column_name_map_from_database()

        # GRAB TRANSIENT METADATA BEFORE CLASSIFICATION
        self.transientsMetadataList = self._get_transient_metadata_from_sqlquery()

        updater = update_ned_stream(
            log=self.log,
            cataloguesDbConn=self.cataloguesDbConn,
            settings=self.settings,
            transientsMetadataList=self.transientsMetadataList
        ).get()
        del updater

        self._crossmatch_transients_against_catalogues()

        if self.update:
            self._update_transient_database()

        self.log.debug('completed the ``get`` method')
        return None

    def _get_transient_metadata_from_sqlquery(
            self):
        """ get transient metadata from a given workflow list in the transient database
        """
        self.log.debug(
            'starting the ``_get_transient_metadata_from_sqlquery`` method')

        sqlQuery = self.settings["database settings"][
            "transients"]["transient query"]
        transientsMetadataList = dms.execute_mysql_read_query(
            sqlQuery=sqlQuery,
            dbConn=self.transientsDbConn,
            log=self.log
        )

        self.log.debug(
            'completed the ``_get_transient_metadata_from_sqlquery`` method')
        return transientsMetadataList

    def _get_transient_metadata_from_database_list(
            self):
        """
        *get transient metadata from a given workflow list in the transient database*
        """
        self.log.debug(
            'starting the ``_get_transient_metadata_from_database_list`` method')

        sqlQuery = self.settings["database settings"][
            "transients"]["transient query"]
        self.transientsMetadataList = dms.execute_mysql_read_query(
            sqlQuery=sqlQuery,
            dbConn=self.transientsDbConn,
            log=self.log
        )

        self.log.debug(
            'completed the ``_get_transient_metadata_from_database_list`` method')
        return None

    def _crossmatch_transients_against_catalogues(
            self):
        """
        *crossmatch transients against catalogue*

        **Key Arguments:**
            # -

        **Return:**
            - None

        .. todo::

            - @review: when complete, clean _crossmatch_transients_against_catalogues method
            - @review: when complete add logging
        """
        self.log.debug(
            'starting the ``_crossmatch_transients_against_catalogues`` method')

        from sherlock import crossmatcher
        self.allClassifications = []

        cm = crossmatcher(
            log=self.log,
            dbConn=self.cataloguesDbConn,
            transients=self.transientsMetadataList,
            settings=self.settings,
            colMaps=self.colMaps
        )
        self.classifications = cm.get()
        del cm

        self.log.debug(
            'completed the ``_crossmatch_transients_against_catalogues`` method')
        return None

    # use the tab-trigger below for new method
    def _update_transient_database(
            self):
        """
        *update transient database*

        **Key Arguments:**
            # -

        **Return:**
            - None

        .. todo::

            - @review: when complete, clean _update_transient_database method
            - @review: when complete add logging
        """
        self.log.debug('starting the ``_update_transient_database`` method')

        crossmatchTablename = self.crossmatchTablename

        from datetime import datetime, date, time
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")

        transientTable = self.settings["database settings"][
            "transients"]["transient table"]
        transientTableClassCol = self.settings["database settings"][
            "transients"]["transient classification column"]
        transientTableIdCol = self.settings["database settings"][
            "transients"]["transient primary id column"]

        for c in self.classifications:

            objectType = c["object_classification_new"]
            transientObjectId = c["id"]

            # DELETE PREVIOUS CROSSMATCHES
            try:
                thisId = int(transientObjectId)
            except:
                thisId = '"%(transientObjectId)s"' % locals()

            sqlQuery = u"""
                  delete from %(crossmatchTablename)s  where transient_object_id = %(thisId)s
            """ % locals()
            dms.execute_mysql_write_query(
                sqlQuery=sqlQuery,
                dbConn=self.transientsDbConn,
                log=self.log
            )

            # INSERT NEW CROSSMATCHES
            sqlQuery = u"""INSERT ignore into %(crossmatchTablename)s""" % locals(
            )
            sqlQuery += u""" (
                           transient_object_id,
                           catalogue_object_id,
                           catalogue_table_id,
                           catalogue_view_id,
                           catalogue_object_ra,
                           catalogue_object_dec,
                           catalogue_object_mag,
                           catalogue_object_filter,
                           original_search_radius_arcsec,
                           separation,
                           z,
                           scale,
                           distance,
                           distance_modulus,
                           date_added,
                           association_type,
                           physical_separation_kpc,
                           catalogue_object_type,
                           catalogue_object_subtype,
                           catalogue_table_name,
                           catalogue_view_name,
                           search_name,
                           major_axis_arcsec,
                           direct_distance,
                           direct_distance_scale,
                           direct_distance_modulus
                           )
                        values (
                           %s,
                           "%s",
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s)
                        """
            manyValueList = []
            for crossmatch in c["crossmatches"]:
                for k, v in crossmatch.iteritems():
                    if v == None:
                        crossmatch[k] = None
                if "physical_separation_kpc" not in crossmatch.keys():
                    crossmatch["physical_separation_kpc"] = None
                if "sourceFilter" not in crossmatch.keys():
                    crossmatch["sourceFilter"] = None
                if "sourceMagnitude" not in crossmatch.keys():
                    crossmatch["sourceMagnitude"] = None

                if crossmatch["sourceSubType"] and "null" not in str(crossmatch["sourceSubType"]):
                    crossmatch["sourceSubType"] = '"%s"' % (crossmatch[
                        "sourceSubType"],)
                else:
                    crossmatch["sourceSubType"] = None

                for k, v in crossmatch.iteritems():
                    if v == "null":
                        crossmatch[k] = None

                theseValues = (thisId, crossmatch["catalogueObjectId"], crossmatch["catalogueTableId"], crossmatch["catalogueViewId"], crossmatch["sourceRa"], crossmatch["sourceDec"], crossmatch["sourceMagnitude"], crossmatch["sourceFilter"],  crossmatch["originalSearchRadius"], crossmatch["separation"], crossmatch["z"], crossmatch["scale"], crossmatch["distance"], crossmatch[
                               "distanceModulus"], now, crossmatch["association_type"], crossmatch["physical_separation_kpc"], crossmatch["sourceType"], crossmatch["sourceSubType"], crossmatch["catalogueTableName"], crossmatch["catalogueViewName"], crossmatch["searchName"], crossmatch["xmmajoraxis"], crossmatch["xmdirectdistance"], crossmatch["xmdirectdistancescale"], crossmatch["xmdirectdistanceModulus"])
                manyValueList.append(theseValues)

            dms.execute_mysql_write_query(
                sqlQuery=sqlQuery,
                dbConn=self.transientsDbConn,
                log=self.log,
                manyValueList=manyValueList
            )

        for ob in self.transientsMetadataList:
            transId = ob["id"]
            if not isinstance(transId, int):
                transId = '"%(transId)s"' % locals()
            name = ob["name"]

            sqlQuery = u"""
                select id, separation, catalogue_view_name, association_type, physical_separation_kpc, major_axis_arcsec from %(crossmatchTablename)s  where transient_object_id = %(transId)s order by separation
            """ % locals()
            rows = dms.execute_mysql_read_query(
                sqlQuery=sqlQuery,
                dbConn=self.transientsDbConn,
                log=self.log
            )

            rankScores = []
            for row in rows:
                if row["separation"] < 2. or (row["physical_separation_kpc"] != None and row["physical_separation_kpc"] < 20. and row["association_type"] == "SN") or (row["major_axis_arcsec"] != "null" and row["association_type"] == "SN"):
                    # print row["separation"]
                    # print row["physical_separation_kpc"]
                    # print row["major_axis_arcsec"]
                    rankScore = 2. - \
                        self.colMaps[row["catalogue_view_name"]][
                            "object_type_accuracy"] * 0.1
                    # print rankScore
                else:
                    # print row["separation"]
                    # print row["physical_separation_kpc"]
                    # print row["major_axis_arcsec"]
                    rankScore = row["separation"] + 1. - \
                        self.colMaps[row["catalogue_view_name"]][
                            "object_type_accuracy"] * 0.1
                rankScores.append(rankScore)

            rank = 0
            theseValues = []
            for rs, row in sorted(zip(rankScores, rows)):
                rank += 1
                primaryId = row["id"]
                theseValues.append("(%(primaryId)s,%(rank)s)" % locals())

            theseValues = ",".join(theseValues)
            if len(theseValues):
                sqlQuery = u"""
                    INSERT INTO %(crossmatchTablename)s (id,rank) VALUES %(theseValues)s 
                    ON DUPLICATE KEY UPDATE rank=VALUES(rank);
                """ % locals()
                dms.execute_mysql_write_query(
                    sqlQuery=sqlQuery,
                    dbConn=self.transientsDbConn,
                    log=self.log,
                )

            sqlQuery = u"""
               select distinct association_type from (select association_type from %(crossmatchTablename)s  where transient_object_id = %(transId)s  order by rank) as alias;
            """ % locals()
            rows = dms.execute_mysql_read_query(
                sqlQuery=sqlQuery,
                dbConn=self.transientsDbConn,
                log=self.log
            )

            classification = ""
            for row in rows:
                classification += row["association_type"] + "/"
            classification = classification[:-1]

            if len(classification) == 0:
                classification = "ORPHAN"

            sqlQuery = u"""
                    update %(transientTable)s  set %(transientTableClassCol)s = "%(classification)s"
                        where %(transientTableIdCol)s  = %(transId)s
                """ % locals()

            print """%(name)s: %(classification)s """ % locals()

            dms.execute_mysql_write_query(
                sqlQuery=sqlQuery,
                dbConn=self.transientsDbConn,
                log=self.log
            )

        self.log.debug('completed the ``_update_transient_database`` method')
        return None

    def _grab_column_name_map_from_database(
            self):
        """
        *grab column name map from database*

        **Return:**
            - None
        """
        self.log.info(
            'starting the ``_grab_column_name_map_from_database`` method')

        # GRAB THE NAMES OF THE IMPORTANT COLUMNS FROM DATABASE
        sqlQuery = u"""
            select v.id as view_id, view_name, raColName, decColName, object_type, subTypeColName, objectNameColName, redshiftColName, distanceColName, semiMajorColName, semiMajorToArcsec, table_id, table_name, object_type_accuracy, filter1ColName, filterErr1ColName, filterName1ColName, filter2ColName, filterErr2ColName, filterName2ColName, filter3ColName, filterErr3ColName, filterName3ColName, filter4ColName, filterErr4ColName, filterName4ColName, filter5ColName, filterErr5ColName, filterName5ColName from tcs_helper_catalogue_views_info v, tcs_helper_catalogue_tables_info t where v.table_id = t.id
        """ % locals()
        rows = dms.execute_mysql_read_query(
            sqlQuery=sqlQuery,
            dbConn=self.cataloguesDbConn,
            log=self.log
        )
        self.colMaps = {}
        for row in rows:
            self.colMaps[row["view_name"]] = row

        self.log.info(
            'completed the ``_grab_column_name_map_from_database`` method')
        return None

    def _create_crossmatch_table_if_not_existing(
            self):
        """
        *create crossmatch table if it does not yet exist in the transients database*

        **Return:**
            - None
        """
        self.log.info(
            'starting the ``_create_crossmatch_table_if_not_existing`` method')

        crossmatchTablename = self.crossmatchTablename

        sqlQuery = u"""
            CREATE TABLE `%(crossmatchTablename)s` (
              `transient_object_id` varchar(50) NOT NULL DEFAULT '---',
              `catalogue_object_id` varchar(30) NOT NULL DEFAULT '---',
              `catalogue_table_id` smallint(5) unsigned NOT NULL DEFAULT '0',
              `separation` double DEFAULT NULL,
              `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
              `z` double DEFAULT NULL,
              `scale` double DEFAULT NULL,
              `distance` double DEFAULT NULL,
              `distance_modulus` double DEFAULT NULL,
              `association_type` varchar(45) DEFAULT NULL,
              `date_added` datetime DEFAULT NULL,
              `physical_separation_kpc` double DEFAULT NULL,
              `catalogue_object_type` varchar(45) DEFAULT NULL,
              `catalogue_object_subtype` varchar(45) DEFAULT NULL,
              `association_rank` int(11) DEFAULT NULL,
              `catalogue_table_name` varchar(100) DEFAULT NULL,
              `catalogue_view_name` varchar(100) DEFAULT NULL,
              `rank` int(11) DEFAULT NULL,
              `search_name` varchar(100) DEFAULT NULL,
              `major_axis_arcsec` double DEFAULT NULL,
              `direct_distance` double DEFAULT NULL,
              `direct_distance_scale` double DEFAULT NULL,
              `direct_distance_modulus` double DEFAULT NULL,
              `catalogue_object_ra` double DEFAULT NULL,
              `catalogue_object_dec` double DEFAULT NULL,
              `original_search_radius_arcsec` double DEFAULT NULL,
              `catalogue_view_id` int(11) DEFAULT NULL,
              `catalogue_object_mag` float DEFAULT NULL,
              `catalogue_object_filter` varchar(10) DEFAULT NULL,
              PRIMARY KEY (`id`),
              UNIQUE KEY `transId_cata_obj_id` (`transient_object_id`,`catalogue_object_id`),
              UNIQUE KEY `catid_search_name` (`catalogue_object_id`,`catalogue_table_id`,`search_name`),
              KEY `key_transient_object_id` (`transient_object_id`),
              KEY `key_catalogue_object_id` (`catalogue_object_id`),
              KEY `idx_separation` (`separation`)
            ) ENGINE=MyISAM AUTO_INCREMENT=15168904 DEFAULT CHARSET=latin1 DELAY_KEY_WRITE=1;
        """ % locals()
        try:
            dms.execute_mysql_write_query(
                sqlQuery=sqlQuery,
                dbConn=self.transientsDbConn,
                log=self.log
            )
        except:
            pass

        self.log.info(
            'completed the ``_create_crossmatch_table_if_not_existing`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method


if __name__ == '__main__':
    main()
