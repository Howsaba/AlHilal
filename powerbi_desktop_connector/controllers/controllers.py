# -*- coding: utf-8 -*-
                                    
# relative imports
import json
import logging

# absolute imports
from odoo import http
from odoo.http import request, Response
from itertools import groupby
from odoo.tools import date_utils
from odoo.addons.powerbi_desktop_connector.controllers.validate_token import validate_token
from odoo.addons.powerbi_desktop_connector.common import datefields_extracter
from math import ceil



_logger = logging.getLogger(__name__)


def check_constraint_and_return_columns(constraint_type,model):

    request.env.cr.execute(f'''
                            SELECT c.column_name
                            FROM information_schema.key_column_usage AS c
                            LEFT JOIN information_schema.table_constraints AS t
                            ON t.constraint_name = c.constraint_name
                            WHERE 
                            t.table_name = '{model.replace('.', '_')}' 
                            AND 
                            t.constraint_type = '{constraint_type}'
                            ''')
        
    columns = request.env.cr.dictfetchall()
    return (True if columns else False , [ obj['column_name'] for obj in columns])
    

def get_column_names_with_datatype(model,columns):
    schemas = request.env.cr.execute(f'''
                                        SELECT 
                                        column_name,data_type 
                                        FROM 
                                        information_schema.columns 
                                        WHERE 
                                        table_schema = 'public' 
                                        AND
                                        table_name = '{model.replace('.', '_')}'
                                        AND
                                        column_name in {str(tuple(columns))}
                                        ''')
    return request.env.cr.dictfetchall()


def get_all_column_names_with_datatype(model):
    schemas = request.env.cr.execute(f'''
                                        SELECT 
                                        column_name,data_type 
                                        FROM 
                                        information_schema.columns 
                                        WHERE 
                                        table_schema = 'public' 
                                        AND
                                        table_name = '{model.replace('.', '_')}'
                                        ''')
    return request.env.cr.dictfetchall()



def get_num_of_columns(model):
    request.env.cr.execute(f'''
                            select count(*) as column_count
                            from 
                            information_schema.columns
                            where 
                            table_name= '{model.replace('.', '_')}'

                            ''')
        
    return request.env.cr.dictfetchall()[0]['column_count']


def get_number_of_records(model):
    request.env.cr.execute(f'''
                            SELECT 
                            COUNT(*) AS size 
                            FROM 
                            {model.replace('.', '_')}

                            ''')
    return request.env.cr.dictfetchall()[0]['size']


def get_integer_Columns(columns):
    for d in columns:
        if d['data_type'] == "integer":
           return d['column_name']
    return columns[0]['column_name']

def get_all_orderby_Columns(columns):
    
    tmp_lst = [ d['column_name'] for d in columns if d['data_type'] == 'integer']
           
    return tmp_lst if tmp_lst else [columns[0]['column_name']]



class BIConnecter(http.Controller):

    ''' Contain all the API's where You can get schema of tables and  getting the specified table data.'''
    
    @http.route('/finnabi/powerbi/schemas/', type='http',website=False, auth="none",methods=['GET','OPTIONS'],csrf=False,cors='*')
    def get_schema(self, **kwargs):
        
        ''' This Api's helps to getting all the database tables schema '''
        
        key_func = lambda v: v['table_name']
        res = dict()

        _logger.info('getting database tables with its schema')
        try:
            with http.request.env.cr.savepoint():
                schemas = request.env.cr.execute(f'''
                                                    SELECT 
                                                    column_name,data_type AS column_type,table_name 
                                                    FROM 
                                                    information_schema.columns 
                                                    WHERE 
                                                    table_schema = 'public' 
                                                    ORDER BY table_name
                                                    ''')
                schemas = request.env.cr.dictfetchall()
                
                for key, value in groupby(schemas, key_func):
                    value = list(value)
                    res[key.replace('_','.')] = [ {"column_name":obj["column_name"],"column_type":obj["column_type"]}for obj in value]
        except Exception as e:
            _logger.error(str(e))
            return Response(
                        json.dumps({'error':f'{str(e)}'},default=date_utils.json_default),
                        content_type='application/json',
                        status= 500
                        )
        _logger.info('Schema collection done')
        response = Response(
                        json.dumps(res,default=date_utils.json_default),
                        content_type='application/json',
                        status=200
                        )
        response.status = '200'
        return response

    @http.route('/finnabi/name/entitylist/', type='http', auth="none",website=False, methods=['GET', 'OPTIONS'], csrf=False, cors='*')
    def get_model_names(self, **kwargs):

        '''This Api's helps to getting all the database tables schema '''
       
        _logger.info('getting database tables')
        models = []
        try:
            with http.request.env.cr.savepoint():

                tables = request.env.cr.execute('''SELECT 
                                                    relname AS table  
                                                    FROM 
                                                    pg_stat_user_tables 
                                                    ORDER BY relname
                                                    ''')
                tables = request.env.cr.dictfetchall()

                for obj in tables:
                    models.append(obj['table'].replace('_', '.'))

        except Exception as e:
            _logger.error(str(e))
            return Response(
                json.dumps({'error': f'{e}'}, default=date_utils.json_default),
                content_type='application/json',
                status=500
            )

        _logger.info('tables collection done')
        return Response(
            json.dumps(models, default=date_utils.json_default),
            content_type='application/json',
            status=200
        )


    @validate_token
    @http.route(['/finnabi/<string:model>', '/finnabi/<string:model>/'], type='http', auth="none",methods=['GET', 'OPTIONS'], website=False, csrf=False,cors='*')
    def get_model(self, model, **kwargs):

        ''' This Api gets the data of specified table in URL parameter '''
        
        _logger.info(f'getting data of {model} ')

        status = 200
        size = False
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        

        try:
            
            size,column_count = get_number_of_records(model),get_num_of_columns(model)
            is_pk_exist,pk_columns = check_constraint_and_return_columns(constraint_type='PRIMARY KEY',model=model)
            is_uq_exist,uq_columns = check_constraint_and_return_columns(constraint_type='UNIQUE',model=model) 

        except Exception as e:

            _logger.error(str(e))
            params = {'error': str(e)}
            status = 500
            return Response(json.dumps(params, default=date_utils.json_default), content_type='application/json',
                            status=status)

        
        params = {
            "count": int(kwargs.get('count', 20000)) * (2 if column_count <= 40 else 1) ,
            "prev": None,
            "current": int(kwargs.get('current', 1)),
            "next": None,
            "total_pages": None,
            "data": [],
            "size":size
        }

        params['total_pages'] = ceil(size / params.get('count'))
        params['next'] = None if params.get('current') == params.get('total_pages') or params.get('total_pages') == 0  else str(base_url).strip("/") + '/finnabi/' + model + '?current=' + str(params.get('current') + 1)
        params['prev'] = None if params.get('current') == 1 else str(base_url).strip("/") + 'finnabi/' + model + '?current=' + str(params.get('current') - 1)
        if not params.get('prev', False):
            params.pop('prev')
        if not params.get('next', False):
            params.pop('next')
        to = params.get('current') * params.get('count')
        frm = to - params.get('count')
        if not params.get('total_pages', False):
            params.pop('current')


        try:
            with http.request.env.cr.savepoint():

                if is_pk_exist:
                    _logger.info("running PK block")
                    order_by = ','.join(pk_columns) if len(pk_columns) > 1 else pk_columns[0]
                    values = request.env.cr.execute(f'''
                                                SELECT * 
                                                FROM 
                                                {model.replace('.', '_')} 
                                                ORDER BY {order_by}
                                                LIMIT {params.get('count')} OFFSET {frm} '''
                                                )
                    values = request.env.cr.dictfetchall()
                
                elif is_uq_exist:
                    _logger.info("running UNIQUE block")
                    columns = get_column_names_with_datatype(model=model,columns=uq_columns)
                    order_by = get_integer_Columns(columns)
                    values = request.env.cr.execute(f'''
                                                SELECT * 
                                                FROM 
                                                {model.replace('.', '_')} 
                                                ORDER BY {order_by}
                                                LIMIT {params.get('count')} OFFSET {frm} '''
                                                )
                    values = request.env.cr.dictfetchall()
                
                else:
                    _logger.info("running else block")
                    columns = get_all_column_names_with_datatype(model=model)
                    order_by = get_all_orderby_Columns(columns=columns)
                    order_by = order_by[0] if len(order_by) == 1 else ','.join(order_by)
                    values = request.env.cr.execute(f'''
                                                SELECT * 
                                                FROM 
                                                {model.replace('.', '_')} 
                                                ORDER BY {order_by}
                                                LIMIT {params.get('count')} OFFSET {frm} '''
                                                )
                    values = request.env.cr.dictfetchall()


                
                params['data'] = values
        except Exception as e:
            _logger.error(str(e))
            params['data'] = []
            status = 200

        return Response(json.dumps(params, default=date_utils.json_default), content_type='application/json',
                        status=status)

    
