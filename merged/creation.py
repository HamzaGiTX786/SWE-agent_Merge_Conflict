from django.db.backends.creation import BaseDatabaseCreation
from django.db.backends.util import truncate_name


class DatabaseCreation(BaseDatabaseCreation):
    # This dictionary maps Field objects to their associated PostgreSQL column
    # types, as strings. Column-type strings can contain format strings; they'll
    # be interpolated against the values of Field.__dict__ before being output.
    # If a column type is set to None, it won't be included in the output.
    data_types = {
        'AutoField':         'serial',
        'BinaryField':       'bytea',
        'BooleanField':      'boolean',
        'CharField':         'varchar(%(max_length)s)',
        'CommaSeparatedIntegerField': 'varchar(%(max_length)s)',
        'DateField':         'date',
        'DateTimeField':     'timestamp with time zone',
        'DecimalField':      'numeric(%(max_digits)s, %(decimal_places)s)',
        'FileField':         'varchar(%(max_length)s)',
        'FilePathField':     'varchar(%(max_length)s)',
        'FloatField':        'double precision',
        'IntegerField':      'integer',
        'BigIntegerField':   'bigint',
        'IPAddressField':    'inet',
        'GenericIPAddressField': 'inet',
<<<<<<< a
        'NullBooleanField':  'boolean',
        'OneToOneField':     'integer',
        'PositiveIntegerField': 'integer',
        'PositiveSmallIntegerField': 'smallint',
        'SlugField':         'varchar(%(max_length)s)',
||||||| base
        'NullBooleanField': 'boolean',
        'OneToOneField': 'integer',
        'PositiveIntegerField': 'integer CHECK ("%(column)s" >= 0)',
        'PositiveSmallIntegerField': 'smallint CHECK ("%(column)s" >= 0)',
        'SlugField': 'varchar(%(max_length)s)',
=======
        'NullBooleanField':  'boolean',
        'OneToOneField':     'integer',
        'PositiveIntegerField': 'integer CHECK ("%(column)s" >= 0)',
        'PositiveSmallIntegerField': 'smallint CHECK ("%(column)s" >= 0)',
        'SlugField':         'varchar(%(max_length)s)',
>>>>>>> b
        'SmallIntegerField': 'smallint',
<<<<<<< a
        'TextField':         'text',
        'TimeField':         'time',
    }

    data_type_check_constraints = {
        'PositiveIntegerField': '"%(column)s" >= 0',
        'PositiveSmallIntegerField': '"%(column)s" >= 0',
||||||| base
        'TextField': 'text',
        'TimeField': 'time',
=======
        'TextField':         'text',
        'TimeField':         'time',
>>>>>>> b
    }

    def sql_table_creation_suffix(self):
        assert self.connection.settings_dict['TEST_COLLATION'] is None, "PostgreSQL does not support collation setting at database creation time."
        if self.connection.settings_dict['TEST_CHARSET']:
            return "WITH ENCODING '%s'" % self.connection.settings_dict['TEST_CHARSET']
        return ''

    def sql_indexes_for_field(self, model, f, style):
        output = []
        if f.db_index or f.unique:
            qn = self.connection.ops.quote_name
            db_table = model._meta.db_table
            tablespace = f.db_tablespace or model._meta.db_tablespace
            if tablespace:
                tablespace_sql = self.connection.ops.tablespace_sql(tablespace)
                if tablespace_sql:
                    tablespace_sql = ' ' + tablespace_sql
            else:
                tablespace_sql = ''

            def get_index_sql(index_name, opclass=''):
                return (style.SQL_KEYWORD('CREATE INDEX') + ' ' +
                        style.SQL_TABLE(qn(truncate_name(index_name,self.connection.ops.max_name_length()))) + ' ' +
                        style.SQL_KEYWORD('ON') + ' ' +
                        style.SQL_TABLE(qn(db_table)) + ' ' +
                        "(%s%s)" % (style.SQL_FIELD(qn(f.column)), opclass) +
                        "%s;" % tablespace_sql)

            if not f.unique:
                output = [get_index_sql('%s_%s' % (db_table, f.column))]

            # Fields with database column types of `varchar` and `text` need
            # a second index that specifies their operator class, which is
            # needed when performing correct LIKE queries outside the
            # C locale. See #12234.
            db_type = f.db_type(connection=self.connection)
            if db_type.startswith('varchar'):
                output.append(get_index_sql('%s_%s_like' % (db_table, f.column),
                                            ' varchar_pattern_ops'))
            elif db_type.startswith('text'):
                output.append(get_index_sql('%s_%s_like' % (db_table, f.column),
                                            ' text_pattern_ops'))
        return output
