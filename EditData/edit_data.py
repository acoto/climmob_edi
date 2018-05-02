import json
import pprint
import transaction
import xml.etree.ElementTree as ET
from climmob.models.schema import mapFromSchema
from lxml import etree, html
from zope.sqlalchemy import mark_changed


def get_FieldsByType(types, db, self):
    return [item[0] for item in getNamesEditByColums(db, self.request.registry.settings['user.repository']) if
            item[2] in types]


def make_selOneOpt(self, bd, lkp_field):  # make value for select one and multiple in jqgrid
    mySession = self.request.dbsession
    vals = {}
    result = mySession.execute(
        'select %s_cod as qc, %s_des as qd from %s.reg_lkp%s;' % (lkp_field, lkp_field, bd, lkp_field))
    for res in result:
        vals[str(res['qc'])] = res['qd']
    return vals


def getNamesEditByColums(db, odk_repository):  # create available list of columns for editing online
    # request.registry.settings['odktools.path']
    try:
        file = odk_repository + "/" + db + '/odk/registry.xml'
        tree = ET.parse(file)
        columns = []  # var name, desc, type

        for elem in tree.iter('{http://www.w3.org/2002/xforms}group'):
            for g in elem.iter():
                if g.tag.replace('{http://www.w3.org/2002/xforms}', '') in ['input', 'select1', 'select']:
                    columns.append([g.attrib['ref'].split('/')[-1], g.find('{http://www.w3.org/2002/xforms}label').text])

        for elem in tree.iter('{http://www.w3.org/2002/xforms}bind'):
            if elem.attrib['nodeset'].split('/')[-1] != 'instanceID':
                for i, col in enumerate(columns):
                    if elem.attrib['nodeset'].split('/')[-1] == col[0]:
                        col.append(elem.attrib['type'])
        return columns
    except:
        return []


def fillDataTable(self, db, columns):
    ret = {'colNames': [], 'data': [], 'colModel': []}
    sql = 'select '

    columns.insert(0, 'surveyid$%*ID$%*string')

    # hidden field
    ret['colNames'].append('flag_update')

    ret['colModel'].append(
        {'name': 'flag_update', 'hidden': True, 'editable': True, 'editrules': {'edithidden': False}})

    for col in columns:
        print col
        col = col.split("$%*")
        ret['colNames'].append(col[1])
        if col[0] == 'surveyid':
            ret['colModel'].append(
                {'align': 'center', 'label': col[0], 'name': col[0], 'index': col[0], 'editable': False, 'width': 50,
                 'sortable': True, 'align': "center"})
        else:
            if 'select1' in col[2]:  # list select type
                ret['colModel'].append(
                    {'align': 'center', 'label': col[1], 'name': col[0], 'index': col[0], 'editable': True,
                     "formatter": "select", 'edittype': "select",
                     'editoptions': {'multiple': False, 'value': make_selOneOpt(self, db, col[0])}})
            else:
                if 'select' in col[2]:  # list select multiple
                    ret['colModel'].append(
                        {'align': 'center', 'label': col[1], 'name': col[0], 'index': col[0], 'editable': True,
                         "formatter": "select", 'edittype': "select",
                         'editoptions': {'multiple': True, 'value': make_selOneOpt(self, db, col[0])}})
                else:
                    if 'decimal' in col[2] or 'int' == col[2]:  # integer values
                        ret['colModel'].append(
                            {'align': 'center', 'label': col[1], 'name': col[0], 'index': col[0], 'editable': True,
                             'edittype': "text", "formatter": "integer",
                             'editrules': {'number': True, 'required': False}})
                    else:
                        if 'date' in col[2]:
                            ret['colModel'].append(
                                {'align': 'center', 'label': col[1], 'name': col[0], 'index': col[0], 'editable': True,
                                 'edittype': "text", "formatter": "date",
                                 'editrules': {'date': True, 'required': True}})
                        else:
                            ret['colModel'].append(
                                {'align': 'center', 'label': col[1], 'name': col[0], 'index': col[0], 'editable': True,
                                 'edittype': "text"})

        # formatter formatter:'date'
        sql = sql + col[0] + ','

    sql = sql[:-1] + ' from %s.reg_maintable order by surveyid;' % db
    mySession = self.request.dbsession
    result = mySession.execute(sql)
    for res in result:
        rowx = {}
        rowx['flag_update'] = False
        for r in zip(result._metadata.keys, res):
            if str(r[0]) in get_FieldsByType(['select1', 'select'], db, self):
                rowx[str(r[0])] = map(int, str(r[1]).split(','))
            else:
                rowx[str(r[0])] = str(r[1])
        ret['data'].append(rowx)
    print '*-*-*-*-*-*-*-*'
    pprint.pprint(ret, width=1)
    print '*-*-*-*-*-*-*-*'
    return json.dumps(ret)


def update_edited_data(self, db, data):
    mySession = self.request.dbsession
    data = json.loads(data[0])

    for row in data:
        if row['flag_update']:
            query_update = 'update %s.reg_maintable set ' % db
            del row['flag_update']
            for key in row:
                val = ''
                if key in get_FieldsByType(['int', 'decimal'], db, self):
                    val = str(row[key])
                else:
                    if key in get_FieldsByType(['select1'], db, self):
                        val = str(row[key]).replace('[', '').replace(']', '')
                    else:
                        if key in get_FieldsByType(['select'], db, self):
                            val = "'" + str(row[key]).replace('[', '').replace(']', '').replace(' ', '') + "'"
                        else:
                            val = "'" + str(row[key]) + "'"
                query_update += key + '=' + val + ', '
            query_update = query_update[:-2] + ' where surveyid =' + str(row['surveyid']) + ';'
            try:
                transaction.begin()
                mySession.execute(query_update)
                mark_changed(mySession)
                transaction.commit()
            except:
                return 0
    return 1
