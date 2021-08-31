import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State,MATCH, ALL
#import arxiv
import numpy as np
import argparse
import tqdm
import os
#from arxiv import SortOrder, SortCriterion
import urllib
import feedparser
import time
import re


keyword = 'iccv'
confs = ['all', 'all-arXiv', 'CVPR', "ICCV", "ECCV", "WACV","AAAI","BMVC","NeurIPS","ICML","ICLR"]
max_res = ['all', '100', '200', "300", "400", "500","1000","1500","2000","3000","4000"]

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

if not os.path.isfile('logfav'):
  with open('logfav', 'w+') as f:
    f.close()
    
def loading(children):
  return dcc.Loading(children, type='cube', fullscreen=True, style={'opacity': 0.9})	

app.layout = dbc.Container([html.Br(),
                            
    dbc.InputGroup([dbc.InputGroupAddon(dbc.Checkbox(id = 'check-all'), addon_type="prepend"),
                    dbc.Input(placeholder= 'search anything', id='search_string', style={'width':'250px'}), 
                    dbc.Select(id="select",placeholder= 'venue',options=[{"label":i, "value":idx} for idx,i in enumerate(confs)],value =0),
                    dbc.Select(id="select_max",placeholder= 'max',options=[{"label":i, "value":idx} for idx,i in enumerate(max_res)],value = 1),
                    #dbc.InputGroupAddon("abstract", addon_type="prepend"),
                    #dbc.InputGroupAddon(dbc.RadioButton(id="is_abs"), addon_type="prepend"),
                    dbc.InputGroupAddon(dbc.Button("search", color="light", size = 'sm', id = 'search', className="mr-1")),
                    
                    ],size="sm",style={'width':'600px'}),


    html.Br(),
    (html.Div(id='my-output')),
    html.Div(id='dummy'),
    loading(html.Div(id='loadig'))


], style =  {'align':'center', 'width':'800px'})


@app.callback(
    [Output(component_id='my-output', component_property='children'),Output(component_id='loadig', component_property='children'),],
    [Input(component_id='search', component_property='n_clicks'), Input(component_id='check-all', component_property='checked')],
    [State(component_id='select', component_property='value'), State(component_id='search_string', component_property='value'), State(component_id='select_max', component_property='value')]
)
def update_output_div(n_click, check_all, select_id, string, select_max):

  with open('logfav', 'r') as f:
    favlist = [ii[:-1][:-2] for ii in f.readlines()]
    f.close()
  with open('logfav', 'r') as f:
    favlistv = [ii[:-1] for ii in f.readlines()]
    f.close()
  
  print (check_all)

  if n_click or check_all:

     # print (confs, select_id)
      conf = confs[int(select_id)] 
      max = max_res[int(select_max)]
      if max == 'all':
        max = float('inf')
      else:
        max = int(max)
      
      if conf == 'all':
        conf_query = "("+' OR '.join(['(co:'+conf +' OR jr:'+conf+')' for conf in confs[1:]])
      elif conf == 'all-arXiv':
        conf_query = "("+'cat:cs.CV'
      else:
        conf_query = "("+'co:'+conf +' OR jr:'+conf

      print (conf_query)

      if string is None or string.strip() is "":
        query = conf_query + ')'
      else:

     
        string = re.sub(' +', ' ', string).strip()
        
        query = conf_query + ") AND "  + '(('+ ' AND '.join(['all:'+i for i in string.split(' ')]) + '))' #OR (' + ' AND '.join(['abs:'+i for i in string.split(' ')]) + '))'

      print (query)

      query = query.replace(' ', '+').replace('(','%28').replace(')','%29')
      strtime = time.time()
      if check_all:
        #print('https://export.arxiv.org/api/query?'+ 'search_query='+query+'&max_results='+str(max)+'&id_list='+','.join(favlistv) +'&sortBy=submittedDate&sortOrder=descending')
        data = urllib.request.urlopen('https://export.arxiv.org/api/query?id_list='+','.join(list(set(favlistv))) +'&sortBy=submittedDate&sortOrder=descending').read()
        search = feedparser.parse(data)
      else:

        data = urllib.request.urlopen('https://export.arxiv.org/api/query?search_query='+query+'&max_results='+str(max)+ '&sortBy=submittedDate&sortOrder=descending').read() 
        search = feedparser.parse(data)

      time_diff = time.time()-strtime

      all_text = [html.P('fetched '+str(len(search['entries'])) + ' results in '+str(round(time_diff, 2)) +' seconds' , style={
                               'margin-top':   '0px',
                               'margin-left':  '0px',
                               'font-size': '12px'})]


      for idx, result in tqdm.tqdm(enumerate(search['entries'])):
        skip = False

        categories = result['arxiv_primary_category']['term']
        title = result['title']
        authors = ', '.join([i.name for i in result['authors']])
        comments = result['arxiv_comment'] if ('arxiv_comment' in result.keys()) else None
        jour_ref = result['arxiv_journal_ref'] if ('arxiv_journal_ref' in result.keys()) else None
        arxiv_id = result['id']
        pdf_url = arxiv_id.replace('abs', 'pdf')
        published = '-'.join(result['published'].split('-')[:2])


        if comments is not None:
          for q in confs[2:]:
            if q.lower() in comments.lower():
              conf_name_show = q
              skip = True
        if jour_ref is not None and skip is False:

          for q in confs[2:]:
            if q.lower() in jour_ref.lower():
              conf_name_show = q
              skip = True

        if skip is False:
          conf_name_show = 'arXiv'
  

        author_list = authors#', '.join([au.name for au in result.authors])
        if arxiv_id.split('/abs/')[-1][:-2] in favlist:
          check_fav = True
        else:
          check_fav = False
        arxiv_list = html.Div([dbc.Checkbox(className="form-check-input", checked = check_fav, id = {'type': 'check-fav','index': arxiv_id},  style={'margin-top':'7px'}), dbc.Badge('[' + published + '] ', color="primary", className="mr-1"), 
                   
                            dbc.Badge(conf_name_show, color="success", className="mr-1"), 
                            #
                            dbc.Badge(title, color="light", href = arxiv_id, className="mr-1", id={'type': 'title','index': arxiv_id}, target='_blank') ,
                            dbc.Badge('[pdf]', color="light", href = pdf_url, className="mr-1", target='_blank'), 
                            html.P(author_list, style={
                               'margin-top':   '0px',
                               'margin-left':  '20px',
                               'font-size': '12px'}),
                            #dbc.Badge('[abstract]', color="light",href = result.pdf_url, className="mr-1"),
                            #html.Img(src = 'http://www.arxiv-sanity.com/static/thumbs/2104.08850v1.pdf.jpg')
                            ])

        all_text.append(arxiv_list)
        #if is_abs:
        #  all_text.append(html.P('Abstract: ' + result['summary'], style={
        #                        'margin-top':   '0px',
        #                        'margin-left':  '20px',
        #                        'font-size': '10px'}),
        #                    #dbc.Badge('[abstract]', color="light",href = result.pdf_url, className="mr-1"),
        #                    #html.Img(src = 'http://www.arxiv-sanity.com/static/thumbs/2104.08850v1.pdf.jpg')
        #                    )
        
      return all_text, dash.no_update

  else:

      return dash.no_update, dash.no_update


@app.callback(
    Output(component_id='dummy', component_property='children'),
    [Input(component_id={'type': 'check-fav',  'index': ALL}, component_property='checked')],)
   # [State(component_id='check-fav', component_property='id')])

def update_fav(checked):

    print ('********')

    print (checked, len(dash.callback_context.triggered),dash.callback_context.triggered[0]['prop_id'])

    if len(dash.callback_context.triggered) == 1:

      if dash.callback_context.triggered[0]['value'] == True:
        arxivid = dash.callback_context.triggered[0]['prop_id'].split('/abs/')[1].split('","type":"check-fav"')[0]
      
        with open('logfav', 'a+') as f:
          f.write(arxivid + '\n')
          f.close()

      if dash.callback_context.triggered[0]['value'] == False:

        arxivid = dash.callback_context.triggered[0]['prop_id'].split('/abs/')[1].split('","type":"check-fav"')[0]
        #print (arxivid)

        with open('logfav', 'r') as f:
          favlist = [ii[:-1] for ii in f.readlines()]
          f.close()

        #if arxivid in favlist:
        #  #print ('removed')
        #  favlist.remove(arxivid)

        favlist = [i for j, i in enumerate(favlist) if i != arxivid]

        with open('logfav', 'w+') as f:
          for i in favlist:
            f.write(i + '\n')
          f.close()


        



if __name__ == '__main__':
    app.run_server(debug=False)