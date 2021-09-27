# Save a module init file that contains a custom function that we'll use
# to verify that import works.


#Code1
def LoadData(loadmat,pd,np,Display_Results):

    
    #[1] North and south segments data and general parameters
    #Load data
    m=loadmat('Input/zos_data_B300_segments.mat')
    ndata = {n: m['row'][n][0,0] for n in m['row'].dtype.names}
    dfm=pd.DataFrame.from_dict(dict((column, ndata[column][0]) for column in [n for n, v in ndata.items() if v.size == 1]))

    #Segment name 
    NSeg=dfm['N'][0];

    #Start and end locations of north segment
    ns=dfm['Nstr'][0]; 
    ne=dfm['Nend'][0];

    #Start and end locations of south segment
    ss=dfm['Sstr'][0]; 
    se=dfm['Send'][0];

    #Name of the Karenia brevis data processing method 
    #2QL10G5: 2 quarters of a year (2Q) period with 10 day length (L) cell counts larger than 100000 and with gap (G) less than 5 days
    KB_bloom=dfm['KB'][0];

    #Name of the zos data processing method 
    #MSXP: zos mean (M) per segment (S) and then delta per period
    model=dfm['model'][0];

    #[2] Load Karenia brevis (KB) data
    # For details about K. brevis data analysis check "Karenia_brevis_data_analysis" folder
    G=int(KB_bloom[-1]) 
    file='Input/KB_data_2Q2014L10G5.csv'
    Kdf=pd.read_csv(file)
    kb=Kdf.iloc[:,-1].copy()
    kb[kb>0]=1
    kb[kb.isnull()]=0
    KBCC=Kdf['max_cells/L_raw_b1e5'].copy()
    KBCC[pd.isna(Kdf['n_days_bloom'])]=0
    KB2Q=kb.to_numpy()
    KBCC2Q=KBCC.to_numpy()
    nm=6;Q='2Q';KB=KB2Q
    #print(KB_bloom,Q,NSeg,model,ne,ns,ss,se)
    print('Karenia brevis data size {}'.format(KB.shape))
    
    #[3] Load zos reanalysis data
    #(Obs)   CMEMS.AVISO-1-0.phy-001-030.r1.Omon.zos.gn (1 realization)
    zosO=np.loadtxt('Input/zos_data_B300_Reanalysis10_phy001_030_r1.csv',delimiter=',')
    print('zos reanalysis data size along the two segments on the Bathymetry 300 {}'.format(zosO.shape))

    #[4] Load zos model data
    #(0-1)   CMIP6.HighResMIP.NCAR.CESM1-CAM5-SE-HR.hist-1950.r1i1p1f1.Omon.zos.gn (1 realization)   [Q 3]
    #(1-2)   CMIP6.HighResMIP.CMCC.CMCC-CM2-HR4.hist-1950.r1i1p1f1.Omon.zos.gn (1 realization) [Q 2]
    #(2-3)   CMIP6.HighResMIP.CMCC.CMCC-CM2-VHR4.hist-1950.r1i1p1f1.Omon.zos.gn (1 realization) [Q 2]
    #(3-6)   CMIP6.HighResMIP.CNRM-CERFACS.CNRM-CM6-1-HR.hist-1950.r1i1p1f2.Omon.zos.gn (3 realizations)  [Q 1]
    #(6-7)   CMIP6.CMIP.CNRM-CERFACS.CNRM-CM6-1-HR.historical.r1i1p1f2.Omon.zos.gn (1 realizations) [Q 1]
    #(7-12)  CMIP6.CMIP.E3SM-Project.ES3M-1-0.historical.r1i1p1f1.Omon.zos.gr (5 realizations) [Q 0]
    #(12-15) CMIP6.HighResMIP.EC-Earth-Consortium.EC-Earth3P-HR.hist-1950.r1i1p2f1.Omon.zos.gn (3 realizations) [Q 0]
    #(15-18) CMIP6.HighResMIP.EC-Earth-Consortium.EC-Earth3P.hist-1950.r1i1p2f1.Omon.zos.gn (3 realizations) [Q 4]
    #(18-24) CMIP6.HighResMIP.ECMWF.ECMWF-IFS-HR.hist-1950.r1i1p1f1.Omon.zos.gn (6 realizations) [Q 5]
    #(24-27) CMIP6.HighResMIP.ECMWF.ECMWF-IFS-MR.hist-1950.r1i1p1f1.Omon.zos.gn (3 realizations)[Q 5]
    #(27-28) CMIP6.CMIP.NOAA-GFDL.GFDL-CM4.historical.r1i1p1f1.Omon.zos.gn (1 realizations) [Q 4]
    #(28-30) CMIP6.CMIP.NOAA-GFDL.GFDL-ESM4.historical.r2i1p1f1.Omon.zos.gn (2 realizations) [Q 3]
    #(30-31) CMIP6.HighResMIP.NERC.HadGEM3-GC31-HH.hist-1950.r1i1p1f1.Omon.zos.gn (1 realization)  [Q 5]
    #(31-34) CMIP6.HighResMIP.MOHC.HadGEM3-GC31-HM.hist-1950.r1i1p1f1.Omon.zos.gn (3 realizations) [Q 5]
    #(34-37) CMIP6.HighResMIP.MOHC.HadGEM3-GC31-MM.hist-1950.r1i1p1f1.Omon.zos.gn (3 realizations) [Q 5]
    #(37-41) CMIP6.CMIP.MOHC.HadGEM3-GC31-MM.historical.r1i1p1f3.Omon.zos.gn (4 realizations) [Q 5]
    #Original CMIP data have large size, so zos data is extracted along the bathometry B300 m.
    #Details about this step can be found under the folder “zos_data_extraction”
    zosMRaw=np.load('Input/zos_data_B300_ESMs43210.npy')
    print('zos ESMs data size along the two segments on the Bathymetry 300 {}'.format(zosMRaw.shape))
    print ('Number of members:', zosMRaw.shape[0])


    #Model info
    df=pd.read_csv('Input/zos_data_B300_ESMs_members.csv')
    if Display_Results==1:
        display(df)
    
    return zosMRaw,zosO,KB,df,ns,ne,ss,se,nm,m


#Code2
def prescreeningTables(zosMRaw,zosO,KB,df,ns,ne,ss,se,nm,NM,pd,np,predictos,Display_Results):
    
    #[1] Create prior ensemble
    zosM=[]
    zosMstd=[]
    dfinfo = pd.DataFrame(columns=['Institution_ID','Source_ID','ensemble_size'])
    for n in range(len(NM)):
        #Select an member
        Str=sum(NM[0:n])
        End=sum(NM[0:n])+NM[n]
        temp=zosMRaw[Str:End,:,:]
        temp[temp>1e3]=np.nan
        zosA=np.nanmean(temp, axis=0)
        zosAstd=np.nanstd(temp,axis=0)

        #Append info 
        dfinfo = dfinfo.append({'Institution_ID':df.loc[Str,'Institution_ID'], 'Source_ID':df.loc[Str,'Source_ID'], \
                                'ensemble_size':NM[n]}, ignore_index=True)

        #Append members
        zosM.append(zosA)
        zosMstd.append(zosAstd)  
    zosM= np.stack(zosM)
    zosMstd= np.stack(zosMstd)
    #print('Prior members',zosMRaw.shape, '-> Prior ensemble',zosM.shape,zosMstd.shape)
    

    #[2] Performance of each member 
    #(2.1)Create results dataframe
    members=['obs', *['Member{}'.format(n) for  n in range(len(NM))]]
    columns=['Institution_ID','Source_ID','e_size', \
             'KB','LCN','LCS','LCN_NB','LCN_B','LCS_NB','LCS_B','Err_KB', \
             'Match_LCN','Match_LCS','Match_Tot','Err_LCN','Err_LCS','Err_Tot','RMSE','Score']
    resm = pd.DataFrame(columns = columns,index=members)

    #(2.2) Create zos dataframe
    columns=['KB','obs', *['Member{}'.format(n) for  n in range(len(NM))]]
    Q=pd.date_range('1993-01-01', periods=44, freq='2Q',closed='left')
    dfzos = pd.DataFrame(columns=columns,index=Q)
    dfzos.KB=KB

    #(2.3) Observation data processing 
    DO=(np.nanmean(zosO[:,ns:ne], axis=1) - np.nanmean(zosO[:,ss:se], axis=1))
    LCO=DO.reshape((-1,nm),order='C').max(axis=1)
    member='obs'
    Institution_ID= 'CMEMS'
    Source_ID= 'phy-001-030'
    ensemble_size=1
    resm=predictos(np,resm,member,KB,LCO,LCO,Institution_ID,Source_ID,ensemble_size,Flag=1)
    dfzos.obs=LCO
    
    #(2.4) Model data processing 
    for n in range(len(NM)):
        #(MSXP) mean_segment(delta-north-south), max_period
        DM=(np.nanmean(zosM[n,:,ns:ne], axis=1) - np.nanmean(zosM[n,:,ss:se], axis=1))
        LCM=DM.reshape((-1,nm),order='C').max(axis=1)
        member='Member{}'.format(n)
        Institution_ID=dfinfo.loc[n,'Institution_ID']
        Source_ID=dfinfo.loc[n,'Source_ID']
        ensemble_size=dfinfo.loc[n,'ensemble_size']
        resm=predictos(np,resm,member,KB,LCO,LCM,Institution_ID,Source_ID,ensemble_size,Flag=1)
        dfzos['Member{}'.format(n)]=LCM
    
    #(2.4) Display results table
    if Display_Results==1:
        display(resm)
        display(dfzos)

    return resm,dfzos,LCO,LCM


#Code3
def predictos(np,resm,member,KB,LCO,LC,Institution_ID,Source_ID,ensemble_size,Flag):
    
    """Extract records about the topic you are interested in 
    Parameters:
    -----------
   topic :
    #### [1] Prescreening predictors 
    For Loop Current north (LC-N) and Loop Current south (LC-S) given 2Q (i.e., 6 month perid):
    (1) resolve observed physical phenomena (Yes / No) 
    (2) frequency of an oscillation(LC-N, LC-S)
    (3) temproal-match(LC-N, LC-S,Total) 
    (4) RMSE(Total) for each member, model, and group (Table 1-3)
          
    Return:
    --------
    """

    #Info
    if Flag==1:
        resm.loc[member,'Institution_ID']=Institution_ID
        resm.loc[member,'Source_ID']=Source_ID
        resm.loc[member,'e_size']=ensemble_size
    elif Flag==2:
        resm.loc[member,'e_size']=ensemble_size
    
    #KB Blooms and LC counts
    resm.loc[member,'KB']=(KB>0).sum()
    resm.loc[member,'LCN']=(LC>=0).sum()
    resm.loc[member,'LCS']=(LC<0).sum()
    resm.loc[member,'LCN_NB']=((LC>=0) & (KB==0)).sum()
    resm.loc[member,'LCN_B']=((LC>=0) & (KB>0)).sum()
    resm.loc[member,'LCS_NB']=((LC<0)  & (KB==0)).sum()
    resm.loc[member,'LCS_B']=((LC<0)  & (KB>0)).sum()
    resm.loc[member,'Err_KB']= np.round(resm.loc[member,'LCS_B']/resm.loc[member,'KB'],decimals=3)

    #Temporal match between observation and model
    resm.loc[member,'Match_LCN']=((LC>=0) & (LCO>=0)).sum()    
    resm.loc[member,'Match_LCS']=((LC<0) & (LCO<0)).sum()  
    resm.loc[member,'Match_Tot']=resm.loc[member,'Match_LCN']+resm.loc[member,'Match_LCS']

    #Temporal error between observation and model
    resm.loc[member,'Err_LCN']=0
    resm.loc[member,'Err_LCS']=0
    resm.loc[member,'Err_Tot']=0

    #Temporal error between re-analysis and model
    if member =='obs':
        resm.loc[member,'Err_LCN']=0
        resm.loc[member,'Err_LCS']=0
        resm.loc[member,'Err_Tot']=0
    else:
        resm.loc[member,'Err_LCN']=np.round((resm.loc['obs','LCN']-resm.loc[member,'Match_LCN'])/resm.loc['obs','LCN'],decimals=3)
        resm.loc[member,'Err_LCS']=np.round((resm.loc['obs','LCS']-resm.loc[member,'Match_LCS'])/resm.loc['obs','LCS'],decimals=3)
        resm.loc[member,'Err_Tot']=np.round((len(LCO)-resm.loc[member,'Match_Tot'])/len(LCO),decimals=3)

    #RMSE between re-analysis and model
    resm.loc[member,'RMSE']=np.round(np.sqrt(np.mean(np.square(LC-LCO)))*1e2,decimals=2)

    return resm


#Code4
def plot_zos(pd,plt,mdates,datetime,NM,dfzos,resm,MI,m,Display_Results,Show_Plot):
    
    #[0] Plot style 
    # for count,Plot in enumerate(['LCA','LCM','LCMW']):
    #     plot_zos(df,Plot,Period,count,fig)
    #Plot area/bar 
    Period='2Q'
    PlotType=2
    Score4=0
    members=['obs', *['Member{}'.format(n) for  n in range(len(NM))]]
    FigNum=['a','b','c','d','e','f','g','h','i','j','k','l']

    #[1] chart size 
    plt.rcParams['font.size'] = '12'
    fig=plt.figure(figsize=(15,15),dpi=100)
    pn=0
    for nn,Plot in enumerate(members): 
        pn+=1
        ax=fig.add_subplot(6,2,pn)
        #[2] Select data
        if PlotType==1:
            #[1] Data with colors for 
            y=dfzos.KB
            cc=['colors']*len(y)
            for n,y_i in enumerate(y):
                if y_i>0:
                    cc[n]='red'
                else:
                    cc[n]='green'    

            mask_N= [c == 'red' for c in cc]
            x1=df.index.copy()[mask_N]
            y1=df[Plot].copy()[mask_N]

            mask_S= [c == 'green' for c in cc]
            x2=df.index.copy()[mask_S]
            y2=df[Plot].copy()[mask_S]
        elif PlotType==2:
            x=dfzos.index.copy()
            y=dfzos[Plot]*100

        #[2] Member score
        #Score
        Score=0
        LCN=sum(y>=0)
        LCS=sum(y<0)

        #(1) Simulate Warm current
        if LCN>0:
            Score+=1

            #(2) Simulate warm and cool current
            if (LCN>0 and LCS>0):
                Score+=1

        #(3) frequency LC-N > LC-S
        if LCS>0:
            if LCN>=LCS:
                Score+=1

            #(4) Delta zos above threshold 
            if Score4==1:
                #SSH value
                if min(y)>-5:
                    Score+=1

        resm.loc[Plot,'Score']=Score

        #[3] Plot bar/area chart 
        if Period=='Q':
            BarW=92
        elif Period=='2Q':
            BarW=181

        if PlotType==1:
            ax.bar(x,y*100,width=BarW,facecolor='red',  alpha=1, label='Large Bloom')
            ax.bar(x,y*100,width=BarW,facecolor='green', alpha=1, label='No Bloom')
        elif PlotType==2:
            ax.fill_between(x, y, 0, where=y >= 0, facecolor='red', interpolate=True, alpha=1,label='LC-N')
            ax.fill_between(x, y, 0, where=y <= 0, facecolor='green', interpolate=True, alpha=1,label='LC-S')


        #[4] format the x-ticks and labels
        years = mdates.YearLocator(5)   # every year
        if Period=='Q':
            months = mdates.MonthLocator(bymonth=[1,4,7,10,13])  # every month
        elif Period=='2Q':
            months = mdates.MonthLocator(bymonth=[1,7,13])  # every month
        years_fmt = mdates.DateFormatter('%Y')
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(years_fmt)
        ax.xaxis.set_minor_locator(months)
        if pn<=10:
            ax.set_xticklabels([])


        # # Set tick font size
        # for label in (ax.get_xticklabels() + ax.get_yticklabels()):label.set_fontsize(12)


        #[5] x-axis limit
        Start=1993
        End=2015
        start = datetime(year=Start, month=1, day=1, hour=0)
        end   = datetime(year=End, month=1, day=1, hour=0)
        ax.set_xlim(start,end)

        if (pn != 2) and (pn != 6):
            ax.set_ylim(-10,10)

        #[6] Axis labels
        if (nn % 2) == 0:
            #ax.set_ylabel(' Δzos (cm)', alpha=1)
            ax.set_ylabel('zos anomaly (cm)', alpha=1)

        ax.tick_params(axis='x',direction='in')
        ax.tick_params(which='minor', direction='in')


        #[7] Legend
        if pn==1:
            ax.legend(loc='lower right')

        #[8] Grid
        if PlotType==1:
            ax.grid(which='major', axis='x')


        #[9] Title
        Institution_ID=resm.loc[Plot,'Institution_ID']
        Source_ID=resm.loc[Plot,'Source_ID']
        if nn==2:
            #IMS2: 'CMCC-CM2-(V)HR4'
            Source_ID='CMCC-CM2-(V)HR4'
        elif nn==9:
            #IMS9: 'GFDL-CM4/ESM4'
            Source_ID='GFDL-CM4/ESM4'
        elif nn==10:
            #IMS10: 'HadGEM3-GC31-HH/HM'
            #IMS10 'MOHC-NERC'
            Source_ID='HadGEM3-GC31-HH/HM'
            Institution_ID='MOHC-NERC'
        elif nn==11:
            #IMS11 MOHC-NERC
            Institution_ID='MOHC-NERC'

        if nn==0:
            Plot='Reanalysis data'
            Title='({}) {}: {} {}'.format(FigNum[nn],Plot,Institution_ID,Source_ID)
        else:
            Plot='IMS{:02d}'.format(nn)
            Title='({}) {}: {} {} (Score {})'.format(FigNum[nn],Plot,Institution_ID,Source_ID,Score)

        ax.set_title(Title,alpha=1,fontsize=14)

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)

    #[10] Display results
    resm.to_csv('Output/Table2_members_score_MI{}.csv'.format(MI))
    if Display_Results==1:
        display(resm)

    #[11] Save plot and table
    if Show_Plot==1:
        plt.savefig('Output/Figure5_Reanalysis_ESMs_MI{}.tif'.format(MI),bbox_inches='tight')
        plt.show()
    else:
        plt.close()


    return resm


#Code5
def Score_Members(df,resm,np,NM):
    for index, row in df.iterrows():
        Institution_ID=row['Institution_ID']
        Source_ID=row['Source_ID']
        Experiment_ID=row['Experiment_ID']
        score=resm.loc[resm['Source_ID']==Source_ID,'Score'].to_numpy()
        if Source_ID=='CMCC-CM2-VHR4':
            score=resm.loc[resm['Source_ID']=='CMCC-CM2-HR4','Score'].to_numpy()
        elif Source_ID=='GFDL-ESM4':
            score=resm.loc[resm['Source_ID']=='GFDL-CM4','Score'].to_numpy()      
        elif Source_ID=='HadGEM3-GC31-HM':
            score=resm.loc[resm['Source_ID']=='HadGEM3-GC31-HH','Score'].to_numpy()
        elif Source_ID=='phy-001-030':    
            score=df['Score'].max()

        if (Source_ID=='HadGEM3-GC31-MM' and Experiment_ID=='historical'):
            df.loc[index, 'Score']=score[0]
        elif (Source_ID=='HadGEM3-GC31-MM' and Experiment_ID=='hist-1950'):
            df.loc[index, 'Score']=score[0]
        else:
            df.loc[index, 'Score']=score

    #Member
    df['Member'] = np.nan  
    for n in range(len(NM)):
        Str=sum(NM[0:n])
        End=sum(NM[0:n])+NM[n]
        df.loc[Str:End,'Member']=n


    #Save and display 
    #df.to_csv('Output/zos_data_B300_ESMS_members_score.csv')
    #display(df)   
    return(df)


#Code6
def zos_data_processing(NME,ME, Score_Members,df,resm,np,NM,pd,KB,LCO,LCM,zosO,ns,ne,ss,se,nm,zosMRaw,m,MI,Display_Results):
    
    #(0) Score per realization for subset selection
    df=Score_Members(df,resm,np,NM)

    #(1) Ensembles 
    #NME=['3210',   '321X',     '32XX',      '3XXX',       'XXX0']
    #ME=[[3,2,1,0], [3,2,1,-1], [3,2,-1,-1], [3,-1,-1,-1], [-1,-1,-1,0]]
    # NME=['3XXX']
    # ME=[[3,-1,-1,-1]]
    #Disp=0


    #(2)Create results dataframe
    members=['obs', *[*NME]]
    columns=['e_size', 'KB','LCN','LCS','LCN_NB','LCN_B','LCS_NB','LCS_B','Err_KB', \
             'Match_LCN','Match_LCS','Match_Tot','Err_LCN','Err_LCS','Err_Tot','RMSE']
    resEN = pd.DataFrame(columns = columns,index=members)

    #(2.1) Dataframe for model data (zos)
    columns=['KB','obs', *NME]
    Q=pd.date_range('1993-01-01', periods=44, freq='2Q',closed='left')
    resMD=pd.DataFrame(columns=columns,index=Q)


    #(3) Create zos dataframe
    columns=['KB','obs', *[*NME]]
    Q=pd.date_range('1993-01-01', periods=44, freq='2Q',closed='left')
    dfzos = pd.DataFrame(columns=columns,index=Q)
    dfzos.KB=KB

    #(4) Observation data processing 
    DO=(np.nanmean(zosO[:,ns:ne], axis=1) - np.nanmean(zosO[:,ss:se], axis=1))
    LCO=DO.reshape((-1,nm),order='C').max(axis=1)
    member='obs'
    ensemble_size=1
    resEN=predictos(np,resEN,'obs',KB,LCO,LCO,Institution_ID='', Source_ID='', ensemble_size='', Flag=2)
    dfzos.obs=LCO

    #(4.1) Observation zos data
    resMD.KB=KB
    resMD.obs=LCO

    for nme,me in zip(NME,ME):    

        #[1] Step 1: Collect model runs data 
        #Initalize ensemble: zos data and info
        ZOS=[]
        df_ensemble = df[0:0]

        #(1.1)Ensemble data and info
        for index, row in df.iterrows():
            Score=row['Score']
            Institution_ID=row['Institution_ID']
            if Score==me[0] or Score==me[1] or Score==me[2] or Score==me[3]:
                if (Institution_ID != 'CMEMS'):
                    temp=zosMRaw[index,:,:]
                    temp[temp>1e3]=np.nan

                    ZOS.append(temp) 
                    df_ensemble.loc[index]=row
        ZOS= np.stack(ZOS)
        ZOSN=ZOS[:,:,ns:ne]
        ZOSS=ZOS[:,:,ss:se]
        print('Step 1: Collect zos data {} for north {} and south {} segments for all model runs for multi-model ensemble {}'.\
              format(ZOS.shape,ZOSN.shape,ZOSS.shape,nme))

        #(1.2) Save proccessed data 
        m['ZOS']=ZOS
        m['ZOSN']=ZOSN
        m['ZOSS']=ZOSS
        m['Member']=df_ensemble.loc[:,['Score','Member']].to_numpy()
        m['row']['Ensemble'][0,0][0]=nme
        #df_ensemble.to_csv('Output/zos_data_B300_ESMsProccessed_T{}.csv'.format(nme))

        #[2] Process ensemble (ensemble mean and std)
        #zosA=np.nanmean(ZOS, axis=0)
        #zosAstd=np.nanstd(ZOS,axis=0)
        zosAN=np.nanmean(ZOSN, axis=0)
        zosAS=np.nanmean(ZOSS, axis=0)

        #Display ensemble info and zos data size
        if nme=='XXX0':
            print('For each multi-model ensemble:')
            print('Step 2: Average zos data of all model runs for north segment {} and south segment {} '.format(zosAN.shape,zosAS.shape))
        if Display_Results>0:
            display(df_ensemble)
            print('zos data',nme,':',ZOS.shape,zosAN.shape,zosAS.shape)

        #[3] Data processing MSXP: mean_segment(delta-north-south), max_period

        #(3.1) Mean segment
        std=0
        if std==0:
            zosMN=zosAN
            zosMS=zosAS
        elif std==1:
            zosM=zosAstd
        #DMN=np.nanmean(zosM[:,ns:ne], axis=1)
        #DMS=np.nanmean(zosM[:,ss:se], axis=1)
        DMN=np.nanmean(zosMN, axis=1)
        DMS=np.nanmean(zosMS, axis=1)
        if nme=='XXX0':
            print('Step 3: Average zos data of north segment{} and south segment {}'.format(DMN.shape,DMS.shape))

        #(3.2) Delta north and south
        DM=DMN-DMS 
        if nme=='XXX0':
            print('Step 4: Subtract zos data of north segment from south segment {}'.format(DM.shape))

        #(3.3) Maximum delta zos per period 
        LCM=DM.reshape((-1,nm),order='C').max(axis=1)
        if nme=='XXX0':
            print('Step 5: Select maximum delta zos in the 6-month interval {} given 22-year study period'.format(LCM.shape))

        #(3.4) Collect data per model run
        dfzos.loc[:,nme]=LCM

        #(3.5) Save data for optimization
        resMD.loc[:,nme]=LCM
        #m['LCO']=LCO
        #m['LCM']=LCM
        #mfile='Output/zos_data_B300_ESMsProccessed_R{}_MI{}.mat'.format(nme,MI)
        #sio.savemat(mfile,m)

        #[4] Calculate predictors 
        ensemble_size=ZOS.shape[0]
        resEN=predictos(np,resEN,nme,KB,LCO,LCM,Institution_ID='', Source_ID='', ensemble_size=ensemble_size, Flag=2)


    #Display results table
    resm.iloc[0,0]=1
    if Display_Results>1:
        display(resEN)
        display(resMD)

    #Save table
    resm.to_csv('Output/Table3_Subset_selection_MI{}.csv'.format(MI))
    
    return resEN,resMD,NME


#Code7
def Plot_zos_RA_ESMs(pd,resMD,NME,plt,mdates,datetime,MI,Show_Plot):
    #[1] Create dataframe with KB,data,ESM and weight ESM data
    Q=pd.date_range('1993-01-01', periods=44, freq='2Q',closed='left')
    dfplot = pd.DataFrame({'KB':resMD.KB, \
                       'LCDM':resMD.obs, 'LCDW':resMD.obs, \
                       'LCM_3210':resMD['3210'],  \
                       'LCM_321X':resMD['321X'],  \
                       'LCM_32XX':resMD['32XX'],  \
                       'LCM_3XXX':resMD['3XXX'], },index=Q)
    DL=['LCDM','LCM_3210','LCM_321X','LCM_32XX','LCM_3XXX']

    #[2] Title of each subplot
    tsa = ['({}) SME{}'.format(fn,nme)   for fn,nme in zip(['b','c','d','e'],NME)]
    tsa.insert(0,'(a) Reanalysis data')
    Title  =tsa

    #[3] Create axes for subplots
    fig, axes = plt.subplots(5,1, figsize=(12,15), sharex=True,  dpi=80)

    #[4] Plot each axes
    for nax, ax in enumerate(axes.ravel()):

        #(1) Data with colors
        y=dfplot.KB
        cc=['colors']*len(y)
        for n,y_i in enumerate(y):
            if y_i>0:
                cc[n]='red'
            else:
                cc[n]='green'    

        mask_N= [c == 'red' for c in cc]
        x1=dfplot.index.copy()[mask_N]
        y1=dfplot[DL[nax]].copy()[mask_N]

        mask_S= [c == 'green' for c in cc]
        x2=dfplot.index.copy()[mask_S]
        y2=dfplot[DL[nax]].copy()[mask_S]

        #(2) Plot bar chart
        BarW=181
        ax.bar(x1,y1*100,width=BarW,facecolor='red',  alpha=0.7, label='Large Bloom')
        ax.bar(x2,y2*100,width=BarW,facecolor='green', alpha=0.7, label='No Bloom')

        #(3) format the x-ticks and labels
        #years = mdates.YearLocator()   # every year
        years = mdates.YearLocator(2)   # every 5 years
        months = mdates.MonthLocator(bymonth=[1,7,13])  # every month
        years_fmt = mdates.DateFormatter('%Y')
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(years_fmt)
        ax.xaxis.set_minor_locator(months)

        #(4) x-axis limit
        Start=1993
        End=2015
        start = datetime(year=Start, month=1, day=1, hour=0)
        end   = datetime(year=End, month=1, day=1, hour=0)
        ax.set_xlim(start,end)

        #(5) Axis labels
        if nax == 0:
            ax.set_ylabel('zos anomaly (cm)',fontsize=16)

        #(6) Legend
        if nax==0:
            ax.legend(fontsize=14,loc='best')

        #(7) Grid
        ax.grid(which='major', axis='x')
        ax.tick_params(axis='both', which='major', labelsize=16)

        #(8) Title
        ax.set_title(Title[nax],fontsize=16)


    # [5] Save and display plot 
    plt.tight_layout()
    plt.savefig('Output/Figure6_Data_ESMs_MI{}.tif'.format(MI),bbox_inches='tight')
    if Show_Plot==1:
        plt.show()
    else:
        plt.close()
    
    
#Code8
def summary_results(NME,resm,itertools,pd,plt,MI,Display_Results,Show_Plot):
    #[0] Select cases for both the two cases of weighting and simple average 
    #Case1='3210'  #Without prior knowledge 
    #Case2='321X'  #Without prescreening and subset selection 
    #Case3='32XX'  #With prescreening and subset selection 
    #Case4='3XXX'  #With prescreening and subset selection + parsimonious
    Present=2      #[1] Each case: SME/WME  [2] Four cases: SME/WME
    OEF=1          #[1] D4  [2] D4 Error

    #[1] Dataframe for summary reults of weighted ensemble mean
    #(1.1) rows
    if OEF==1:
        D4='Oscillating event frequency ($y_{4}$)' 
    elif OEF==2:
        D4='Oscillating event frequency error ($y_{4,err}$)'
    rows=['(Oscillating event realism ($y_{3}$)', D4, 'Temporal match error ($y_{5}$)', \
           'Karenia brevis error ($y_{6}$)', 'Relative RMSE ($y_{7}$)']

    #(1.2) columns
    Check='\u2713'
    Cross='\u2715'
    Dash='-'
    SME = ['SME{} : ({}) Prior information   ({}) Prescreening-based subset selection'.format(nme,pi,ps) \
           for nme,pi,ps in zip(NME,[Cross,Check,Check,Check],[Cross,Cross,Check,Check])]

    if Present==1:
        columns  = list(itertools.chain(*[list(x) for x in zip(SME,WME)]))
    elif Present==2:
        columns=[*SME]
    columns.insert(0,'Reanalysis data')

    #(1.3) Create dataframe
    SF = pd.DataFrame(columns = columns,index=rows)

    #[2] Process results

    #(2.1) Diagnostics
    MAX_RMSE=resm.loc['3210','RMSE']
    print('MAX_RMSE',MAX_RMSE)

    def DIG(nn,res,Case,MAX_RMSE):

        #Reproduce physical phenomena (D3)
        SF.iloc[0,nn+1]=1

        #Frequency of an event (D4) 
        FData=resm.loc['obs','LCS']/(resm.loc['obs','LCN']+resm.loc['obs','LCS'])
        FModel=res.loc[Case,'LCS']/(res.loc[Case,'LCN']+res.loc[Case,'LCS'])
        if OEF==1:
            SF.iloc[1,nn+1]=FModel
        elif OEF==2:
            SF.iloc[1,nn+1]=abs(FData-FModel)

        #Temporal match error (D5) 
        SF.iloc[2,nn+1]=res.loc[Case,'Err_Tot']

        #Karenia brevis error (D6) 
        SF.iloc[3,nn+1]=res.loc[Case,'Err_KB']

        #RMSE(D7)
        SF.iloc[4,nn+1]=res.loc[Case,'RMSE']/MAX_RMSE

        return SF

    #(2.2) Reanalysis data
    SF=DIG(-1,resm,'obs',MAX_RMSE)

    #(2.3) Ensmble model data
    if Present==1:
        EL=['3210','3210','321X','321X','32XX','32XX','3XXX','3XXX']
        for nn,Case in enumerate(EL):
            if (nn % 2) == 0:  #SME (even)
                SF=DIG(nn,resm,Case,MAX_RMSE)
            else:
                SF=DIG(nn,reswm,Case,MAX_RMSE)         
    elif Present==2:
        EL=['3210','321X','32XX','3XXX']
        for nn,Case in enumerate(EL):
            if nn<4:
                SF=DIG(nn,resm,Case,MAX_RMSE)


    #(2.5) Display data
    if Display_Results>0:
        display(SF)
    

    #[3] Select predictors and ensemble to plot
    NDS=1 #[0] D3
    NDE=5 #[6] AIC
    IDX=[0,1,2,4] #Select ensembles [0] Reanalysis data, [1] SME3210, ..., [8] WME3XXX
    if OEF==2:
        IDX=IDX[1:]
    data=SF.iloc[NDS:NDE,IDX]

    #[4] Plot summary results
    #(4.1) Create figure and subplots
    fig, ax = plt.subplots(1,1)

    #(4.2) Choose bar colors
    colors=['crimson','midnightblue','royalblue','deepskyblue','lightsteelblue','seagreen','mediumseagreen','lightgreen','darkseagreen']
    #colors=['crimson','lightsteelblue','deepskyblue','royalblue','midnightblue','darkseagreen','lightgreen','mediumseagreen','seagreen']
    colors = [colors[i] for i in IDX]

    #(4.3) Plot horizontal bar chart top to bottom
    data.plot.barh(ax=ax, width=0.85,color=colors)
    plt.gca().invert_yaxis()

    #(4.4) Remove all the ticks and label xticks
    #plt.tick_params(labelbottom='on')
    #plt.xticks([0,1], ['0', '1'])
    ax.tick_params(axis="x",direction='out')

    #(4.5) Set axis lim
    if NDE<5:
        plt.xlim(0, 0.4)
    else:
        plt.xlim(0, 1)

    #(4.6) Remove plot frame
    for n,spine in enumerate(plt.gca().spines.values()):
        if n==0:
            spine.set_visible(False)
        elif n==1:    
            spine.set_visible(False)
        elif n==3:
            spine.set_visible(False)

    #(4.7) Legend outside
    ax.legend(bbox_to_anchor=(1.25,-0.1), borderaxespad=0.,frameon=False)    #Left/Right , Up/down

    #(4.8) Save and show plot
    plt.savefig('Output/Figure7_Summary_MI{}.tif'.format(MI),bbox_inches='tight')
    
    if Show_Plot==1:
        plt.show()
    else:
        plt.close()
        
    return SF


