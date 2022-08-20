# インタラクティブダッシュボードを作成する
import numpy as np
import pandas as pd
import streamlit as st
import pydeck as pdk    #３Dグラフ表示のために必要
import plotly.express as px
from pydeck.types import String
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import japanize_matplotlib
from math import pi


#　タイトルを設定する
st.title("chocolate_dashbord")

#  データを読み込み
df_choco_eval = pd.read_csv("./data/1.after_data_prep/20220813/choco_eval_prep_20220813.csv",encoding="utf_8")
df_choco_store = pd.read_csv("./data/1.after_data_prep/20220813/choco_store_prep_20220813.csv",encoding="utf_8")
df_choco_shop_address = pd.read_csv("./data/1.after_data_prep/try1_20220605091938/shop_info_osaka_after_prep.csv",encoding='utf_8')

df_choco_shop_address = df_choco_shop_address.rename(columns= {"緯度":"lon","経度":"lat","店名":"store_name","ジャンル":"genre","営業時間":"store_time"})

df_choco_shop_address = df_choco_shop_address[["lat","lon","store_name","store_time","genre"]]

# 大阪　北緯 34°41′11″ 東経 135°31′12″
osaka_lat = 135.3112
osaka_lon = 34.4111

# データを地図に渡す関数を作成する
def AreaMarker(df,m):
    for index, r in df.iterrows(): 
        popup=folium.Popup(r.store_name + "<br />" + str(r.genre) + "<br />" + str(r.store_time) ,max_width=200,show=True)
        
        # ピンをおく
        folium.Marker(
            location=[r.lon, r.lat],
            popup=popup,
        ).add_to(m)


        # 円を重ねる
        #folium.Circle(
            #radius=rad*1000,
            #location=[r.lon, r.lat],
            #popup=r.store_name,
            #color="yellow",
            #fill=True,
            #fill_opacity=0.07
        #).add_to(m)


# ------------------------画面作成------------------------

st.header("chocolate_shop map") # タイトル
#rad = st.slider('拠点を中心とした円の半径（km）',
                #value=40,min_value=5, max_value=50) # スライダーをつける
#st.subheader("各拠点からの距離{:,}km".format(rad)) # 半径の距離を表示
m = folium.Map(location=[osaka_lon,osaka_lat], zoom_start=10) # 地図の初期設定
AreaMarker(df_choco_shop_address,m) # データを地図渡す
folium_static(m) # 地図情報を表示

#チェックボックスがONの場合にデータを表示させる
show_df_choco_shop_address = st.checkbox("Show DataFrame")
if show_df_choco_shop_address == True:
    st.write(df_choco_shop_address)


# ---------チョコレートショップを選択させてレーダーチャートを表示させる-----
st.header("chocolate_store evaluation") # タイトル
#select box list
choco_store_list = df_choco_store["store_name"].unique()
option_choco_store = st.selectbox(
    "store_name",
    (choco_store_list)
)

#filter data 
df_choco_store_filterd = df_choco_store.loc[df_choco_store["store_name"]==option_choco_store]

# ------- PART 1: Create background
 
# number of variable
categories=list(df_choco_store_filterd)[4:9]
N = len(categories)
 
# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
 
# Initialise the spider plot
ax = plt.subplot(111, polar=True)
 
# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)
 
# Draw one axe per variable + add labels
plt.xticks(angles[:-1], categories)
 
# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([1,2,3,4], ["1","2","3","4"], color="grey", size=7)
plt.ylim(0,5)

# ------- PART 2: Add plots
 
# Plot each individual = each line of the data
# I don't make a loop, because plotting more than 3 groups makes the chart unreadable
 
# Ind1
values=df_choco_store_filterd.iloc[0].drop(['store_id','store_name','url','created_time','country','type']).tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label=df_choco_store_filterd.iloc[0]["store_name"])
ax.fill(angles, values, 'b', alpha=0.1)

# Add legend
plt.legend(loc='upper left', bbox_to_anchor=(0.7, 1))

# Show the graph
### plt.savefig("image/all.png")
st.pyplot(plt)