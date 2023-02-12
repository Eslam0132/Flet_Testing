import openai
from flet import *
import time
import numpy as np
import pandas as pd 
from sentence_transformers import SentenceTransformer,util
from openai.embeddings_utils import get_embedding, cosine_similarity

#Importing Sentance Similarity Model
model = SentenceTransformer('all-MiniLM-L6-v2')

#-(Prices) Dataframe 
df=pd.read_excel("Prices.xlsx")
brand_vals=df['Brand'].unique()

#-(Dealears) Dataframe
df_deal_rep=pd.read_excel("Dealers.xlsx",sheet_name='Rep')
df_deal_rep['Similer']=""
df_deal_rep['Brand'].fillna('-', inplace=True)
df_deal_rep['Similer']="Country :"+df_deal_rep['Country']+", Brand: "+df_deal_rep['Brand']+", City: "+df_deal_rep['City']
df_deal_rep['CRS_embedding']=df_deal_rep['Similer'].apply(lambda x: model.encode(x))
brand_vals_t2=df_deal_rep['Brand'].unique()

#-(Process) Dataframe
df_procc=pd.read_excel("RCX_Process_1.xlsx")
df_procc['CRS_embedding']=df_procc['Customer Request (Scenario)'].apply(lambda x: model.encode(x))


def search_semantic(df, query, n=5):
    embedding = model.encode(query)
    embedding_np=np.array(embedding)
    df['similarities'] = df.CRS_embedding.apply(lambda x: cosine_similarity(np.array(x), embedding_np))
    res = df.sort_values('similarities', ascending=False).head(n)
    return res

#On Change Function for NavigationBar 
def main(page:Page):
    page.update()
    def changetab(e):
    # GET INDEX TAB
        my_index = e.control.selected_index
        #--------------
        if my_index == 0:
            tab_1.visible = True
            # tab_14.visible=True
            # tab_12.visible=True
            # tab_13.visible=True

            tab_2.visible = False
            tab_3.visible = False
            tab3_dt.visible=False
            tab2_dt.visible=False
            tab_22.visible=False
            
        #--------------   
        if my_index ==1:
            tab_2.visible = True
            tab2_dt.visible=True
            tab_22.visible=True

            tab_1.visible = False
            tab_3.visible = False
            tab3_dt.visible=False
            tab_12.visible=False
            tab_13.visible=False
            tab_14.visible=False

        #--------------
        if my_index ==2:
            tab_3.visible = True
            tab3_dt.visible=True
            
            tab_1.visible = False
            tab_2.visible = False
            tab2_dt.visible=False
            tab_22.visible=False
            tab_12.visible=False
            tab_13.visible=False
            tab_14.visible=False   

        #--------------
        page.update()
 
    #Creating NavigationBar Consisting of 3 Buttons
    page.navigation_bar = NavigationBar(
    bgcolor="Transparent",
    on_change=changetab,
    selected_index = 0,
    height=50,
    destinations = [
    NavigationDestination(icon=icons.RULE, label="Process"),
    NavigationDestination(icon=icons.CAR_REPAIR, label="Dealers"),
    NavigationDestination(icon=icons.MONEY_OFF,label="Prices"),])

#########################################    
#████████╗ █████╗ ██████╗      ██╗
#╚══██╔══╝██╔══██╗██╔══██╗    ███║
#   ██║   ███████║██████╔╝    ╚██║
#   ██║   ██╔══██║██╔══██╗     ██║
#   ██║   ██║  ██║██████╔╝     ██║
#   ╚═╝   ╚═╝  ╚═╝╚═════╝      ╚═╝
#########################################

   #Send Button Function Displaying Buttons with the highest 3 similarities 
    def tab1_sendb(e):
        tab_12.visible=False
        tab_13.visible=False
        tab_14.visible=True

        query = tab1_txt.value
        dfx=search_semantic(df_procc,query,3).reset_index(drop=True)
        case_txt=dfx['Case/Enquiry Name'][0]
        scenario_txt=dfx['Customer Request (Scenario)'][0]
        data_collection_txt=dfx['Data Collection'][0]
        agent_action=dfx['Agent Actions / Script'][0]
        sys_action=dfx['Actions on System'][0]
        email_r=dfx['Email Required'][0]
        comment=dfx['Comment'][0]

        tab1_query1.text=dfx['Case/Enquiry Name'][0]
        tab1_query2.text=dfx['Case/Enquiry Name'][1]
        tab1_query3.text=dfx['Case/Enquiry Name'][2]
        page.update()

    #Function to fill the Containers Cards with Data depending on the Index
    def button_fun_query(num):
        query = tab1_txt.value
        dfx=search_semantic(df_procc,query,3).reset_index(drop=True)
        case_txt=str(dfx['Case/Enquiry Name'][num])
        scenario_txt=str(dfx['Customer Request (Scenario)'][num])
        data_collection_txt=str(dfx['Data Collection'][num])
        agent_action=str(dfx['Agent Actions / Script'][num])
        sys_action=str(dfx['Actions on System'][num])
        email_r=str(dfx['Email Required'][num])
        comment=str(dfx['Comment'][num])

        case_txt12.content=Text(case_txt,color="white")
        page.update()
        scen_txt12.content=Text(scenario_txt,color="white")
        page.update()
        mail_txt12.content=Text(email_r,color="white")
        page.update()

        dc_txt13.content=Text("Data Collection : \n\n"+data_collection_txt,color="white")
        page.update()
        agent_txt13.content=Text("Agent Actions : \n\n"+agent_action,color="white")
        page.update()
        action_txt13.content=Text("System Actions : \n\n"+sys_action,color="white")
        page.update()
        comment_txt13.content=Text("Comment : \n\n"+comment,color="white")
        page.update()        

    def tab1_q1(e):
        tab_12.visible=True
        tab_13.visible=True
        tab_14.visible=False
        button_fun_query(0)
        page.update()

    def tab1_q2(e):
        tab_12.visible=True
        tab_13.visible=True
        tab_14.visible=False
        button_fun_query(1)
        page.update()

    def tab1_q3(e):
        tab_12.visible=True
        tab_13.visible=True
        tab_14.visible=False
        button_fun_query(2)
        page.update()

    #Send Button And the TextFeild
    tab1_txt=TextField(label="Process Search",hint_text="What Is The Customer's Inquirey", expand=True)
    tab1_button=FloatingActionButton(icon=icons.SEND ,on_click=tab1_sendb)
    tab1_button2=FloatingActionButton(icon=icons.SEND ,on_click=tab1_sendb ,bgcolor=colors.AMBER_400)

    #First Row of Cards
    case_txt12=Container(content=Text("Non clickable"),padding=10,alignment=alignment.center,bgcolor=colors.CYAN_400,width=280,height=45,border_radius=10,)    
    scen_txt12=Container(content=Text("Non clickable"),padding=10,alignment=alignment.center,bgcolor=colors.CYAN_400,width=550,height=45,border_radius=10,)    
    mail_txt12=Container(content=Text("Non clickable"),padding=10,alignment=alignment.center,bgcolor=colors.CYAN_400,width=280,height=45,border_radius=10,)    

    #Second Row of Cards
    dc_txt13=Container(content=Text("Non clickable"),padding=10,alignment=alignment.center,bgcolor=colors.CYAN_400,width=280,height=320,border_radius=10)
    agent_txt13=Container(content=Text("Non clickable"),padding=10,alignment=alignment.center,bgcolor=colors.CYAN_400,width=260,height=320,border_radius=10 ,margin=margin.only(left=10))
    action_txt13=Container(content=Text("Non clickable"),padding=10,alignment=alignment.center,bgcolor=colors.CYAN_400,width=260,height=320,border_radius=10)
    comment_txt13=Container(content=Text("Non clickable"),padding=10,alignment=alignment.center,bgcolor=colors.CYAN_400,width=280,height=320,border_radius=10 ,margin=margin.only(left=10))

    #Button Row
    tab1_query1=ElevatedButton(text="Elevated button",on_click=tab1_q1)
    tab1_query2=ElevatedButton(text="Elevated button",on_click=tab1_q2)
    tab1_query3=ElevatedButton(text="Elevated button",on_click=tab1_q3)

    #Tab 1 Rows
    tab_1 = Row(controls=[tab1_txt,tab1_button])
    tab_12 =Row([case_txt12,scen_txt12,mail_txt12])
    tab_13 =Row([dc_txt13,agent_txt13,action_txt13,comment_txt13])
    tab_14=Row([tab1_query1,tab1_query2,tab1_query3],alignment=MainAxisAlignment.CENTER)


#█████╗█████╗█████╗█████╗█████╗█████╗█████╗
#╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝

#########################################
#████████╗ █████╗ ██████╗     ██████╗ 
#╚══██╔══╝██╔══██╗██╔══██╗    ╚════██╗
#   ██║   ███████║██████╔╝     █████╔╝
#   ██║   ██╔══██║██╔══██╗    ██╔═══╝ 
#   ██║   ██║  ██║██████╔╝    ███████╗
#   ╚═╝   ╚═╝  ╚═╝╚═════╝     ╚══════╝
#########################################

    tab2_dt=DataTable(
        bgcolor="grey",
        border=border.all(2, "blue"),
        border_radius=10,
        data_row_height=45,
        )
    class Summing:
        def __init__(self):
            self.x = 0

        def suming(self):
            self.x += 1
            return self.x  
    summing_obj_2 = Summing()                  

    def tab2_sendb(e):
        query = tab2_txt.value
        dfx=search_semantic(df_deal_rep,query)
        zoka = summing_obj_2.suming() 
        if zoka >1 :
            page.remove(tab2_dt)
        tab2_dt.columns.clear()
        tab2_dt.rows.clear()

        dfx=dfx.drop(columns=['CRS_embedding','similarities','Similer']).reset_index(drop=True)
        for i in range (len(dfx.columns)):
            tab2_dt.columns.append(DataColumn(Text(dfx.columns[i])))
        for i in range (dfx.shape[0]):
            tab2_dt.rows.append(DataRow(cells=[
                DataCell(Text(dfx['Country'][i])),
                DataCell(Text(dfx['Dealer'][i])),
                DataCell(Text(dfx['Brand'][i])),
                DataCell(Text(dfx['City'][i])),
                DataCell(Text(dfx['Name'][i])),
                DataCell(Text(dfx['Designation'][i])),
                DataCell(Text(dfx['Mobile'][i])),
                DataCell(Text(dfx['Email'][i]))
            ]))
        page.add(tab2_dt)
        page.update()    

    tab2_txt=TextField(label="Dealers Info",hint_text="What City/Country/Brand Do You Want To Search With", expand=True) 
    tab2_button=FloatingActionButton(icon=icons.SEND,on_click=tab2_sendb)  
    
    t2_brnd=Dropdown(width=200,height=35, hint_text="Choose Brand")
    for brand in brand_vals_t2:
        t2_brnd.options.append(dropdown.Option(brand)) 

    tab_22=Row(controls=[])
    tab_2 = Row(controls=[tab2_txt,tab2_button])

#█████╗█████╗█████╗█████╗█████╗█████╗█████╗
#╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝

#########################################
#████████╗ █████╗ ██████╗     ██████╗ 
#╚══██╔══╝██╔══██╗██╔══██╗    ╚════██╗
#   ██║   ███████║██████╔╝     █████╔╝
#   ██║   ██╔══██║██╔══██╗     ╚═══██╗
#   ██║   ██║  ██║██████╔╝    ██████╔╝
#   ╚═╝   ╚═╝  ╚═╝╚═════╝     ╚═════╝ 
#########################################

    def filter_brand(e):
        filtered_df = df[df['Brand'] == brnd.value]
        country_vals=filtered_df['Country'].unique()

        cntry.options.clear()
        car_d.options.clear()
        page.update()
        for counrty in country_vals:
            cntry.options.append(dropdown.Option(counrty))
        
        page.update()           

    def filter_country(e):
        filtered_df = df[df['Brand'] == brnd.value]
        filtered_df = filtered_df[filtered_df['Country'] == cntry.value]
        cars_vals=filtered_df['CAR LINE'].unique()

        car_d.options.clear()
        page.update()
        for car in cars_vals:
            car_d.options.append(dropdown.Option(car))   
        page.update()


    tab3_dt=DataTable(
        bgcolor="grey",
        border=border.all(2, "blue"),
        border_radius=10,
        data_row_height=35,
        )

    class Summing:
        def __init__(self):
            self.x = 0

        def suming(self):
            self.x += 1
            return self.x

    summing_obj = Summing()


    def filter_car(e):
        zoka = summing_obj.suming() 
        if zoka >1 :
            page.remove(tab3_dt)
        print(zoka)
        tab3_dt.columns.clear()
        tab3_dt.rows.clear()
        dfx=df.copy()
        dfx = dfx[dfx['Brand'] == brnd.value]
        dfx = dfx[dfx['Country'] == cntry.value]
        dfx = dfx[dfx['CAR LINE'] == car_d.value].reset_index(drop=True)
        for i in range (len(df.columns)):
            tab3_dt.columns.append(DataColumn(Text(df.columns[i])))
        for i in range (dfx.shape[0]):
            tab3_dt.rows.append(DataRow(cells=[
                DataCell(Text(dfx['Brand'][i])),
                DataCell(Text(dfx['CAR LINE'][i])),
                DataCell(Text(dfx['CAB'][i])),
                DataCell(Text(dfx['MODEL CODE'][i])),
                DataCell(Text(dfx['PEG'][i])),
                DataCell(Text(dfx['TRIM'][i])),
                DataCell(Text(dfx['Price'][i])),
                DataCell(Text(dfx['Country'][i]))
            ]))
        page.add(tab3_dt)
        page.update()     
            
        
    brnd=Dropdown(width=200, on_change=filter_brand, hint_text="Choose Brand")
    cntry=Dropdown(width=200, on_change=filter_country ,hint_text="Choose Country")
    car_d=Dropdown(width=200,on_change=filter_car, hint_text="Choose CarLine")

    for brand in brand_vals:
        brnd.options.append(dropdown.Option(brand)) 

    tab_3 = Row(controls=[brnd,cntry,car_d])
    
                                          
                                          
#█████╗█████╗█████╗█████╗█████╗█████╗█████╗
#╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝
                                          
                                          
                                          

    ## App Bar
    page.theme_mode='light'

    def changetheme(e):
    # page.splash.visible=True
        page.theme_mode='light' if page.theme_mode == 'dark' else 'dark'
        page.update()        
        #delay Animation
        time.sleep(0.5)

    view = Column(
        controls=[
            Row(spacing=0,
                controls=[
                Image(src=f"/images/gm.png",
                width=150,
                height=150,
                
                ),
                Text(value="Knowledge Base",
                        size=30,
                        weight=FontWeight.BOLD,
                        color=colors.BLUE_600),

                Text(value= " " * 202), 

                IconButton(
                        on_click=changetheme,
                        icon="dark_mode",
                        selected_icon="light_mode",
                        
                         )  
                ]#,alignment=MainAxisAlignment.START,
            ),

        ]
    )

    page.add(view)

    page.add(
        Container(
        margin = margin.only(
        #top=page.window_height/2,
        left=50
 
            ),
            content=Column(controls=[
                
                tab_1,
                tab_12,
                tab_13,
                tab_14,
                tab_2,
                tab_22,
                tab_3,
    
                ])
 
            )
 
        )
    
    tab_12.visible=False
    tab_13.visible=False
    tab_14.visible=False
    tab_2.visible = False
    tab_3.visible = False
    tab3_dt.visible=False
    tab2_dt.visible=False 
    tab_22.visible=False 
    page.update()   
    
flet.app(target=main)
