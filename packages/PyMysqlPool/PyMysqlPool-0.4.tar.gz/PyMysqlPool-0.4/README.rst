.. image:: https://readthedocs.org/projects/pymysql/badge/?version=latest
    :target: http://pymysql.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/PyMySQL/PyMySQL.svg?branch=master
    :target: https://travis-ci.org/PyMySQL/PyMySQL

.. image:: https://coveralls.io/repos/PyMySQL/PyMySQL/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/PyMySQL/PyMySQL?branch=master

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/LuciferJack/python-mysql-pool/blob/master/LICENSE.txt


PyMysqlPool
=======

.. contents:: Table of Contents
    :local:

This package contains a pure-python mysql connector library. The goal of PyMysqlPool
is to be a  mysql pool and motivation from=>[lost connection to MySQL server during query]  base on mysql-connector .

Requirements
-------------

* Python -- one of the following:
    None


Installation
------------

The last stable release is available on PyPI and can be installed with ``pip``::

    $ pip install PyMysqlPool


Documentation
-------------

Documentation is available online: http://PyMysqlPool.readthedocs.io/

For support, please refer to the `StackOverflow
<http://stackoverflow.com/questions/tagged/PyMysqlPool>`_.

Example
-------

The following pool examples below:


.. code:: python

    step:1

    """
    file:mysql_config.py change to your db config
    """
    db_config = {
        'local': {
            'host': "10.95.130.118", 'port': 8899,
            'user': "root", 'passwd': "123456",
            'db': "marry", 'charset': "utf8",
        },
        'poi': {
            'host': "10.95.130.***", 'port': 8787,
            'user': "lujunxu", 'passwd': "****",
            'db': "poi_relation", 'charset': "utf8",
        },
    }

    step:2

    """
    Note:create your own table
    """

    step:3 (example show below)

    """
    use pool
    """
    def query_pool():
        job_status = 2
        _sql = "select *  from master_job_list j  where j.job_status  !=%s "
        _args = (job_status,)
        task = query('local', _sql,_args)
        logging.info("query_npool method query_npool result is %s ,input _data is %s ", task , _args)
        return


    """
    pool in operation
    """
    def query_pool_in():
        job_status = 2
        _sql = "select *  from master_job_list j  where j.job_status  in (%s) "
        _args = (job_status,)
        task = query('local', _sql,_args)
        logging.info("query_npool method query_npool result is %s ,input _data is %s ", task , _args)
        return

    """
    pool size special operation
    """
    def query_pool_size():
        job_status = 2
        _sql = "select *  from master_job_list j  where j.job_status  in (%s) "
        _args = (job_status,)
        pool_info = {}
        pool_info['pool_size'] = 100
        task = query('local', _sql,_args)
        logging.info("query_npool method query_npool result is %s ,input _data is %s ", task , _args)
        return

    """
    single query
    """
    def query_npool():
        job_status = 2
        _sql = "select *  from master_job_list j  where j.job_status  !=%s "
        _args = (job_status,)
        task = query_single('local', _sql,_args)
        logging.info("query_npool method query_npool result is %s ,input _data is %s ", task , _args)
        return

    """
    insert
    """
    def insert(nlp_rank_id,hit_query_word):
        #add more args
        _args = (nlp_rank_id,hit_query_word)
        _sql = """INSERT INTO nlp_rank_poi_online (nlp_rank_id,hit_query_word,rank_type,poi_list,poi_raw_list,article_id,city_id,status,create_time,version,source_from) VALUES (%s,%s,%s, %s, %s,%s, %s,%s, %s,%s,%s)"""
        affect = insertOrUpdate("local", _sql, _args)
        logging.info("insert method insert result is %s ,input _data is %s ", affect , _args)
        return

    """
    update
    """
    def update(query_word,query_id):
        _args = (query_word,query_id)
        _sql = """update nlp_rank  set query_word = %s  WHERE  id = %s"""
        affect = insertOrUpdate("local", _sql, _args)
        logging.info("update method update result is %s ,input _data is %s ", affect , _args)
        return



Resources
---------

python mysql connector: https://dev.mysql.com/downloads/connector/python/

MySQL Reference Manuals: http://dev.mysql.com/doc/

MySQL client/server protocol:
http://dev.mysql.com/doc/internals/en/client-server-protocol.html

PyMysqlPool mailing list: https://groups.google.com/forum/#!forum/PyMysqlPool-users

License
-------

PyMysqlPool is released under the MIT License. See LICENSE for more information.