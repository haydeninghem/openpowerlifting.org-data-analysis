import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io 
# Read the CSV file into a DataFrame
whole_dataset = pd.read_csv('openpowerlifting-2023-06-17.csv')

#Filter dataset to show only USAPL Male
USAPL_MALE = whole_dataset[(whole_dataset['Federation'] == 'USAPL')
                                   & (whole_dataset['Equipment'] == 'Raw')
                                   & (whole_dataset['Sex'] == 'M')
                                   & (whole_dataset['Place'] != 'DD')
                                   & (whole_dataset['Place'] != 'DQ')
                                   ]

USAPL_FEMALE = whole_dataset[(whole_dataset['Federation'] == 'USAPL')
                                   & (whole_dataset['Equipment'] == 'Raw')
                                   & (whole_dataset['Sex'] == 'F')
                                   & (whole_dataset['Place'] != 'DD')
                                   & (whole_dataset['Place'] != 'DQ')
                                   ]
print("USAPL  PROCESSED")
IPF_MALE = whole_dataset[(whole_dataset['ParentFederation'] == 'IPF')
                                   & (whole_dataset['Federation'] != 'USAPL')
                                   & (whole_dataset['Equipment'] == 'Raw')
                                   & (whole_dataset['Sex'] == 'M')
                                   & (whole_dataset['Place'] != 'DD')
                                   & (whole_dataset['Place'] != 'DQ')
                                   ]


IPF_FEMALE = whole_dataset[(whole_dataset['ParentFederation'] == 'IPF')
                                   & (whole_dataset['Federation'] != 'USAPL')
                                   & (whole_dataset['Equipment'] == 'Raw')
                                   & (whole_dataset['Sex'] == 'F')
                                   & (whole_dataset['Place'] != 'DD')
                                   & (whole_dataset['Place'] != 'DQ')
                                   ]
print("IPF PROCESSED")

whole_dataset['Date'] = pd.to_datetime(whole_dataset['Date'])
                                       
UNTESTED_MALE = whole_dataset[(whole_dataset['Equipment'] == 'Raw')
                                   & (whole_dataset['Sex'] == 'M')
                                   & (whole_dataset['Tested'] != 'Yes')
                                   & (whole_dataset['Date'] >= pd.to_datetime('2013-01-01'))
                                   & (whole_dataset['Place'] != 'DQ')
                                   ]


UNTESTED_FEMALE = whole_dataset[(whole_dataset['Equipment'] == 'Raw')
                                   & (whole_dataset['Sex'] == 'F')
                                   & (whole_dataset['Tested'] != 'Yes')
                                   & (whole_dataset['Date'] >= pd.to_datetime('2013-01-01'))
                                   & (whole_dataset['Place'] != 'DQ')
                                   ]
print("UNTESTED  PROCESSED")

def main():
    df_list = []
    USAPL_MALE_DF = get_sbd_median_avg(USAPL_MALE,"MEDIAN_AVG_SBD_USAPL_MALE")
    USAPL_FEMALE_DF = get_sbd_median_avg(USAPL_FEMALE,"MEDIAN_AVG_SBD_USAPL_FEMALE")
    print("USAPL EXPORTED")
    
    IPF_MALE_DF = get_sbd_median_avg(IPF_MALE,"MEDIAN_AVG_SBD_IPF_MALE")
    IPF_FEMALE_DF = get_sbd_median_avg(IPF_FEMALE,"MEDIAN_AVG_SBD_IPF_FEMALE")
    print("IPF EXPORTED")
    

    
    UNTESTED_MALE_DF = get_sbd_median_avg(UNTESTED_MALE,"MEDIAN_AVG_SBD_UNTESTED_MALE")
    UNTESTED_FEMALE_DF = get_sbd_median_avg(UNTESTED_FEMALE,"MEDIAN_AVG_SBD_UNTESTED_FEMALE")

  
 
    print("UNTESTED EXPORTED")
    
    writer = pd.ExcelWriter('MEDIAN_AVG_SBD_COMBINED.xlsx', engine='xlsxwriter')
    
    USAPL_MALE_DF[0].to_excel(writer, sheet_name='USAPL_MALE_SUMMARY', index=True)
    USAPL_MALE_DF[1].to_excel(writer, sheet_name='USAPL_MALE_STAT', index=True)
    
    USAPL_FEMALE_DF[0].to_excel(writer, sheet_name='USAPL_FEMALE_SUMMARY', index=True)
    USAPL_FEMALE_DF[1].to_excel(writer, sheet_name='USAPL_FEMALE_STAT', index=True)
    
    IPF_MALE_DF[0].to_excel(writer, sheet_name='IPF_MALE_SUMMARY', index=True)
    IPF_MALE_DF[1].to_excel(writer, sheet_name='IPF_MALE_STAT', index=True)
    
    IPF_FEMALE_DF[0].to_excel(writer, sheet_name='IPF_FEMALE_SUMMARY', index=True)
    IPF_FEMALE_DF[1].to_excel(writer, sheet_name='IPF_FEMALE_STAT', index=True)
    
    UNTESTED_MALE_DF[0].to_excel(writer, sheet_name='UNTESTED_MALE_SUMMARY', index=True)
    UNTESTED_MALE_DF[1].to_excel(writer, sheet_name='UNTESTED_MALE_STAT', index=True)
    
    UNTESTED_FEMALE_DF[0].to_excel(writer, sheet_name='UNTESTED_FEMALE_SUMMARY', index=True)
    UNTESTED_FEMALE_DF[1].to_excel(writer, sheet_name='UNTESTED_FEMALE_STAT', index=True)
    
    sheet_to_table(writer,USAPL_MALE_DF[0],USAPL_MALE_DF[1])
    
    
    create_avg_sbd_chart(writer,USAPL_MALE_DF[0],'USAPL_MALE_SUMMARY')
    create_avg_total_chart(writer,USAPL_MALE_DF[0],'USAPL_MALE_SUMMARY')
    
    create_avg_total_chart(writer,USAPL_FEMALE_DF[0],'USAPL_FEMALE_SUMMARY')
    create_avg_sbd_chart(writer,USAPL_FEMALE_DF[0],'USAPL_FEMALE_SUMMARY')
    
    create_avg_total_chart(writer,IPF_MALE_DF[0],'IPF_MALE_SUMMARY')
    create_avg_sbd_chart(writer,IPF_MALE_DF[0],'IPF_MALE_SUMMARY')
    
    create_avg_total_chart(writer,IPF_FEMALE_DF[0],'IPF_FEMALE_SUMMARY')
    create_avg_sbd_chart(writer,IPF_FEMALE_DF[0],'IPF_FEMALE_SUMMARY')
    
    create_avg_total_chart(writer,UNTESTED_MALE_DF[0],'UNTESTED_MALE_SUMMARY')
    create_avg_sbd_chart(writer,UNTESTED_MALE_DF[0],'UNTESTED_MALE_SUMMARY')
    
    create_avg_total_chart(writer,UNTESTED_FEMALE_DF[0],'UNTESTED_FEMALE_SUMMARY')
    create_avg_sbd_chart(writer,UNTESTED_FEMALE_DF[0],'UNTESTED_FEMALE_SUMMARY')

    compare_sbd(writer,USAPL_MALE_DF[0],UNTESTED_MALE_DF[0],'USAPL','UNTESTED','USAPL_VS_UNTESTED_MALE')
    compare_sbd(writer,USAPL_MALE_DF[0],IPF_MALE_DF[0],'USAPL','IPF','USAPL_VS_IPF_MALE')
    
    compare_sbd(writer,USAPL_FEMALE_DF[0],UNTESTED_FEMALE_DF[0],'USAPL','UNTESTED','USAPL_VS_UNTESTED_FEMALE')
    compare_sbd(writer,USAPL_FEMALE_DF[0],IPF_FEMALE_DF[0],'USAPL','IPF','USAPL_VS_IPF_FEMALE')
    writer.close()
    print("completed")

def compare_sbd(writer,df1,df2,df1_label,df2_label,sheet_name):
    
    if 'FEMALE' in sheet_name:
        min_row_count = min(len(df1), len(df2))
        df1 = df1.iloc[:min_row_count]
        df2 = df2.iloc[:min_row_count]
    weight_classes = df2.index.astype(str)
    num_classes = len(weight_classes)
    bar_width = 0.35

    fig, axs = plt.subplots(4, 1, figsize=(20, 30))
    
    df1_label = df1_label + ":" + "{:,}".format(df1['count'].sum())
    df2_label = df2_label + ":" + "{:,}".format(df2['count'].sum())
    
    for i, lift in enumerate(['avg_bench', 'avg_squat', 'avg_deadlift','avg_total']):
        ax = axs[i]
        index = np.arange(num_classes)

        df1_lift = df1[lift].tolist()
        df2_lift = df2[lift].tolist()

        rects1 = ax.bar(index, df1_lift, bar_width, label=df1_label)
        rects2 = ax.bar(index + bar_width, df2_lift, bar_width, label=df2_label)

        ax.set_xlabel('Weight Class (KG)')
        ax.set_ylabel(lift + " (LB)")
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(weight_classes)
        ax.legend(loc='upper left')
        
        # Add annotations for percentage difference
        for j in range(num_classes):
            percent_diff = (df2_lift[j] - df1_lift[j]) / ((df2_lift[j] + df1_lift[j]) / 2) * 100
            annotation_text = f'{percent_diff:.2f}%'
    
            # Determine the higher value
            higher_value = max(df2_lift[j], df1_lift[j])
    
            # Determine the index of the higher value
            if higher_value == df2_lift[j]:
                index_value = index[j]
            else:
                index_value = index[j] 
    
            ax.annotate(annotation_text, xy=(index_value, higher_value),
                xytext=(0, 0), textcoords='offset points',
                ha='center', va='bottom')
            
    
    axs[0].set_title('Avg Best Successful Bench  Percent Difference')
    axs[1].set_title('Avg Best Successful Squat Percent Difference')
    axs[2].set_title('Avg Best Successful Deadlift Percent Difference')
    axs[3].set_title('Avg Best Successful Total Percent Difference')
    plt.subplots_adjust(hspace=0.25)
    
    imgdata=io.BytesIO()
    plt.savefig(imgdata, format='png',bbox_inches='tight')
    workbook = writer.book
    worksheet = workbook.add_worksheet(sheet_name)
    worksheet.insert_image(0,0, '', {'image_data': imgdata})
    
def create_avg_sbd_chart(writer,df,sheet_name):
    weight_class = df.index.astype(str)    
    squat = df['avg_squat'].tolist()
    bench = df['avg_bench'].tolist()
    deadlift = df['avg_deadlift'].tolist()
    count = "{:,}".format(df['count'].sum())
    # Create the plot
    plt.figure(figsize=(20, 10))
    plt.xlabel('BODY WEIGHT (KG)')
    plt.ylabel('LIFT (LB)')
    
    plt.plot(weight_class, squat, label='Squat')
    plt.plot(weight_class, bench, label='Bench')
    plt.plot(weight_class, deadlift, label='Deadlift')
    
    plt.scatter(weight_class, squat)
    plt.scatter(weight_class, bench)
    plt.scatter(weight_class, deadlift)
    plt.legend(loc='upper left')
    plt.title('Average Best Successful SBD By Weightclass - ' + sheet_name + ", N = "+str(count))
    
    
            
    for i in range(0,len(weight_class)):
        squat_value = "{:.0f}".format(squat[i])
        bench_value = "{:.0f}".format(bench[i])
        deadlift_value = "{:.0f}".format(deadlift[i])
    
        plt.annotate(squat_value, (weight_class[i], squat[i]), xytext=(0, -5), textcoords='offset points',
                     bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round'), ha='center', va='bottom')
    
        plt.annotate(bench_value, (weight_class[i], bench[i]), xytext=(0, -5), textcoords='offset points',
                     bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round'), ha='center', va='bottom')
    
        plt.annotate(deadlift_value, (weight_class[i], deadlift[i]), xytext=(0, -5), textcoords='offset points',
                     bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round'), ha='center', va='bottom')
    
        plt.plot([weight_class[i], weight_class[i]], [squat[i], 0], color='gray', linestyle='dotted', alpha=0.5)
        plt.plot([weight_class[i], weight_class[i]], [bench[i], 0], color='gray', linestyle='dotted', alpha=0.5)
        plt.plot([weight_class[i], weight_class[i]], [deadlift[i], 0], color='gray', linestyle='dotted', alpha=0.5)
        
    imgdata=io.BytesIO()
    plt.savefig(imgdata, format='png',bbox_inches='tight')
    writer.sheets[sheet_name].insert_image(46,0, '', {'image_data': imgdata})    
    print("Done with " + sheet_name)
def create_avg_total_chart(writer,df,sheet_name):
    weight_class = df.index.astype(str)
    total = df['avg_total'].astype(float)
    count = "{:,}".format(df['count'].sum())
    plt.figure(figsize=(20, 6)) 
    # Create the plot
    plt.plot(weight_class, total)
    plt.xlabel('BODY WEIGHT (KG) ')
    plt.ylabel('TOTAL (LB) ')

    plt.scatter(weight_class, total)
    plt.title('Average Best Successful Total By Weightclass - ' + sheet_name + ", N = "+str(count))
    
    total_values = []
    for value in total:
        total_values.append(value)
   
    for i in range(len(total_values)):
        plt.annotate(int(total_values[i]), (weight_class[i], total_values[i]), xytext=(-3, 3), textcoords='offset points', ha='center', va='bottom')
        plt.plot([weight_class[i], weight_class[i]], [total_values[i], 0], color='gray', linestyle='dotted', alpha=0.5)

    
    imgdata=io.BytesIO()
    plt.savefig(imgdata, format='png',bbox_inches='tight')
    writer.sheets[sheet_name].insert_image(19,0, '', {'image_data': imgdata})
    print("Done with " + sheet_name)

def sheet_to_table(writer,df_sum,df_stat):
    
    sheet_names = writer.book.sheetnames
    
    sum_headers = []
    sum_headers.append({'header': 'adj_weightclass'})
    
    stat_headers = []
    stat_headers.append({'header': 'adj_weightclass'})
    
    for header in df_sum.columns:
        sum_headers.append({'header': header})
    for header in df_stat.columns:
        stat_headers.append({'header': header})
        

    for name in sheet_names:
        if "SUMMARY" in name:
            worksheet = writer.sheets[name]
            worksheet.add_table(0, 0, 18, 9, {'columns': sum_headers})
            worksheet.set_column(0, 9, 18)
        if "STAT" in name:
            worksheet = writer.sheets[name]
            worksheet.add_table(0, 0, 55, 9, {'columns': stat_headers})
            worksheet.set_column(0, 9, 18)
            
            

def get_sbd_median_avg(filtered_dataset,file_name):
    weightclass_columns = [0, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 250]
    squat_columns = ['Squat1Kg', 'Squat2Kg', 'Squat3Kg']
    bench_columns = ['Bench1Kg', 'Bench2Kg', 'Bench3Kg']
    deadlift_columns = ['Deadlift1Kg', 'Deadlift2Kg', 'Deadlift3Kg']
    
 
    filtered_dataset['adj_weightclass'] = pd.cut(x=filtered_dataset['BodyweightKg'], bins=weightclass_columns)
    
    
    # Max SBD for each meet
    max_squat = filtered_dataset[squat_columns].apply(max, axis=1)
    filtered_dataset['max_squat'] = max_squat

    max_bench = filtered_dataset[bench_columns].apply(max, axis=1)
    filtered_dataset['max_bench'] = max_bench

    max_deadlift = filtered_dataset[deadlift_columns].apply(max, axis=1)
    filtered_dataset['max_deadlift'] = max_deadlift
    
    
    # Max successful SBD per person per 10kg jump (adjusted weightclass).
    max_squat_per_person_per_weightclass = filtered_dataset[filtered_dataset['max_squat'] >= 0].groupby(['Name', 'adj_weightclass'])[
        'max_squat'].max().apply(
        lambda x: x * 2.20462)
    max_squat_per_person_per_weightclass.dropna(inplace=True)

    max_bench_per_person_per_weightclass = filtered_dataset[filtered_dataset['max_bench'] >= 0].groupby(['Name', 'adj_weightclass'])[
        'max_bench'].max().apply(
        lambda x: x * 2.20462)
    max_bench_per_person_per_weightclass.dropna(inplace=True)

    max_deadlift_per_person_per_weightclass = filtered_dataset[filtered_dataset['max_deadlift'] >= 0].groupby(['Name', 'adj_weightclass'])[
        'max_deadlift'].max().apply(
        lambda x: x * 2.20462)
    max_deadlift_per_person_per_weightclass.dropna(inplace=True)
    

    


    squat_stats = max_squat_per_person_per_weightclass.groupby('adj_weightclass').describe()
    bench_stats = max_bench_per_person_per_weightclass.groupby('adj_weightclass').describe()    
    deadlift_stats = max_deadlift_per_person_per_weightclass.groupby('adj_weightclass').describe()
    
    squat_stats['90%'] = max_squat_per_person_per_weightclass.groupby('adj_weightclass').quantile(0.9)
    bench_stats['90%'] = max_bench_per_person_per_weightclass.groupby('adj_weightclass').quantile(0.9)
    deadlift_stats['90%'] = max_deadlift_per_person_per_weightclass.groupby('adj_weightclass').quantile(0.9)
    
    squat_stats['type'] = "SQUAT"
    bench_stats['type'] = "BENCH"
    deadlift_stats['type'] = "DEADLIFT"

    
    reindex_order = ['type','25%','50%','75%','90%','max','std','mean','count']
    
    squat_stats = squat_stats.reindex(columns=reindex_order)
    bench_stats = bench_stats.reindex(columns=reindex_order)
    deadlift_stats = deadlift_stats.reindex(columns=reindex_order)
    
    combined_stats = pd.concat([squat_stats, bench_stats,deadlift_stats])
                           
    combined_stats.sort_index(inplace=True)

    
    # Median SBD by weightclass, KG -> LB
    median_squat_by_weightclass = max_squat_per_person_per_weightclass.groupby('adj_weightclass').median()
    median_bench_by_weightclass = max_bench_per_person_per_weightclass.groupby('adj_weightclass').median()
    median_deadlift_by_weightclass = max_deadlift_per_person_per_weightclass.groupby('adj_weightclass').median()

    # Average SBD by weightclass
    mean_squat_by_weightclass = max_squat_per_person_per_weightclass.groupby('adj_weightclass').mean()
    mean_bench_by_weightclass = max_bench_per_person_per_weightclass.groupby('adj_weightclass').mean()
    mean_deadlift_by_weightclass = max_deadlift_per_person_per_weightclass.groupby('adj_weightclass').mean()    

    # Merge SBD Median and avg on weightclass
    median_mean_sbd_by_weightclass = pd.merge(median_squat_by_weightclass, median_bench_by_weightclass,
                                              on='adj_weightclass')
    median_mean_sbd_by_weightclass = pd.merge(median_mean_sbd_by_weightclass, median_deadlift_by_weightclass,
                                              on='adj_weightclass')
    median_mean_sbd_by_weightclass = pd.merge(median_mean_sbd_by_weightclass, mean_squat_by_weightclass,
                                              on='adj_weightclass')
    median_mean_sbd_by_weightclass = pd.merge(median_mean_sbd_by_weightclass, mean_bench_by_weightclass,
                                              on='adj_weightclass')
    median_mean_sbd_by_weightclass = pd.merge(median_mean_sbd_by_weightclass, mean_deadlift_by_weightclass,
                                              on='adj_weightclass')


    median_mean_sbd_by_weightclass['avg_total'] = median_mean_sbd_by_weightclass['max_squat_y']+ median_mean_sbd_by_weightclass['max_bench_y'] + median_mean_sbd_by_weightclass['max_deadlift_y']
    median_mean_sbd_by_weightclass['count'] = filtered_dataset.groupby('adj_weightclass')['Name'].nunique()
    median_mean_sbd_by_weightclass['avg_age_best_attempt'] = filtered_dataset.groupby('adj_weightclass')['Age'].mean()
    
    
    median_mean_sbd_by_weightclass = median_mean_sbd_by_weightclass.rename(columns={
        'max_squat_x': 'median_squat',
        'max_bench_x': 'median_bench',
        'max_deadlift_x': 'median_deadlift',
        'max_squat_y': 'avg_squat',
        'max_bench_y': 'avg_bench',
        'max_deadlift_y': 'avg_deadlift'
    })
    median_mean_sbd_by_weightclass.to_csv(file_name +"_SUMMARY"+ ".CSV", index=True) #[0]
    combined_stats.to_csv(file_name +"_STATS"+ ".CSV", index=True) #[1]
    return [median_mean_sbd_by_weightclass,combined_stats]
main()
