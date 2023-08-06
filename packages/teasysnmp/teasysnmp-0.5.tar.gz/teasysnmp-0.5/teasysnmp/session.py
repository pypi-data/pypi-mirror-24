from easysnmp import Session


class Session(Session):

    def __get_tbl_row(self, table, index, *fields):
        """SNMP get given fields of given index row

        :param table: teasysnmp table
        :param index: the index that defines the row in the snmp table
        :returns: snmp get results
        :rtype:

        """
        # If no fields passed get all fields in the table
        if fields is ():
            fields = table[1].keys()

        eOid, tFields = table
        oids = [
            (".".join((eOid, tFields[field][0])), index)
            for field in fields
        ]

        return self.get(oids)

    def get_tbl_row(self, table, index, *fields):
        """Get given fields from table row of given index

        :param table: teasysnmp table tuple
        :param index: the index to fetch
        :returns: tuple of index and given field values of the row
        :rtype:

        """
        snmp_result = self.__get_tbl_row(self, table, index, *fields)

        data = [
            entry.value
            for entry in snmp_result
        ]
        data.insert(0, index)

        return data

    def get_tbl_rows(self, table, indexes, *fields):
        """Get given fields from tbale rows of given indexes

        :param table: teasysnmp table tuple
        :param indexes: the indexes to fetch
        :returns: list of tuples of index and field values
        :rtype:

        """
        return [
            self.get_tbl_row(self, table, index, *fields)
            for index in indexes
        ]

    def get_tbl_row_dict(self, table, index, *fields):
        """Get given fields from table row of given index

        :param table: easysnmp table tuple
        :param index: the index that defines the row in the snmp table
        :returns: dictionary of fields and values
        :rtype:

        NOTE: If no fields are given all fields of the table are fetched
        """
        snmp_result = self.__get_tbl_row(self, table, index, *fields)

        return {
            fields[i]: entry.value
            for i, entry in enumerate(snmp_result)
        }

    def get_tbl_rows_dict(self, table, indexes, *fields):
        """Get given fields from tables rows of given indexes

        :param table: easysnmp table tuple
        :param indexes: a list of indexes that define rows in the snmp table
        :returns: dictionary of index and dictionary of fields and values
        :rtype:

        NOTE: If no fields are given all fields of the table are fetched
        """
        return {
            index: self.get_tbl_row_dict(table, index, *fields)
            for index in indexes
        }

    def get_tbl_field(self, table, field):
        """Get given field of all rows in the given snmp table

        :param table: easysnmp table tuple
        :param field: a list of indexes that define rows in the snmp table
        :returns: list of given field value of all rows
        :rtype:

        """
        eOid, tFields = table
        return [
            var.value
            for var in self.walk(".".join((eOid, tFields[field][0])))
        ]

    def get_tbl_rows_using_index_table(self, indexTable,
                                       indexField, table, *fields):
        """Get given fields of all rows whose index is pointed by anothher
        index table.

        :param indexTable: the table to get indexes
        :param indexField: the field of the table that has index values
        :param table: the table to get rows from
        :returns: list of all rows with given fields
        :rtype:

        """
        indexes = self.get_tbl_field(indexTable, indexField)
        return [
            self.get_tbl_row(table, index, *fields)
            for index in indexes
        ]
