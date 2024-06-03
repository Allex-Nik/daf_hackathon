import streamlit as st
import folium
from folium import PolyLine
from streamlit_folium import folium_static
import polyline



# Define the polyline string (replace with your actual polyline string)
polyline_str = 'mjm|HqdrY|JmGdE_Co@dFqKpIfA~CwK~RiNrNmGu@kIaJqZP{SrLgRcPfE{V~EwNkDmGmMvSyNbQuRnH}`@~CyOeCaJkIs`@gm@wTub@_YwUcLmUkBiV|g@cnClN{kDf`@cxLh`@ydCvXksBp`AmeG|\\eoBdIa_AY}}AoEahC_o@ieE_e@w_Bor@w~Ai|AsqBqb@aw@eS_nAnAoiBlJifEpBihAsNsdBqPayA[cuB?orDaH{lAyP}eAy^k{AeHg{@SyyAEa{@EqhAC{t@Zys@xHuw@nRkxArJi_AnSsiCxb@ylDpPijAnG{pA~J{tAdQstAxJcxAdBy\\yEwLeJyCmPbMgUpAe`@gOiW{Tu^wg@o\\qUe^iF}YwHgHm\\}@c`Ag@q|BaNwh@uYk^{O}a@aDuc@_IcdDyc@kvDc^i~C{MajCsk@qgCu]{vCsWiiCoSsl@_V{Ygx@{u@glAm`@mbA}_@ceAqiAgh@kMkoAz@_g@kWy}@_u@ahAan@sd@ke@}Zk_Aq~@ixD}m@kcCq[ai@eZeVidA_l@_lAof@wr@qYaw@ge@kj@{g@}b@_d@od@yu@wNer@{CwdA`JooB{AuaAir@elByQmqAwCw~DwKcsBcbB_{HoGwv@Q_hAmHekA}YoaBm_@i_A}q@mi@}MeTsM_g@mh@_oBkx@m`C_q@esAu]qqAut@moBqaAwgDkr@kdCg\\ed@af@{Vgv@c\\q[_YkSk_@ucA_~Box@}oBi[_}@gJqe@}nAwwCkaAqoBmTaq@aPagBoQevC{Hsw@aN_k@}`@{u@ep@if@cyAoz@gfD}hBkqAkp@kYuNed@wJ_e@Y_t@lB}oAfSusArSqoAdOme@kMq\\i]ug@yzAiXehB|@gsBlIsdCh]{vDhIq~@`EuiAeKyjCmb@wgDm`@k_Cs~@ueB}Wqk@mMmq@}JeaD`Bg\\hBhJoEp@gKiI{ToRc_@gKiq@~Asa@_Cur@p@yxAbu@ciAne@}o@`Nok@nA{^wAeYeJgj@e^_o@o[_`AsTedCsoBi|@mr@qw@}d@slAuu@{}@c_As`AemAu]eQqe@qL{mA\\sd@_DaaCkf@akCer@ka@yDgNgJ}CqUrGo{@tD_x@eAipA}GsnBwLo_Fi\\imBs\\k{A_d@{~A_o@kq@cPqReKuZ{SewAwv@uaG{Map@oToa@{e@aeAmlC_jIgLmbA_Lym@{Wyn@g_@il@_e@_k@ii@kYmiAol@gp@_^{QqN{CoR_FuLaQfc@oQda@`D`EbEpGuDrMoKzQwByC'

# Decode the polyline string
coordinates = polyline.decode(polyline_str)

# Create a Folium map centered around the midpoint of the coordinates
midpoint = len(coordinates) // 2
map_center = coordinates[midpoint]
map_ = folium.Map(location=map_center, zoom_start=10)

# Add the polyline to the map
polyline_layer = PolyLine(locations=coordinates, color='blue', weight=5)
map_.add_child(polyline_layer)

# Display the map in Streamlit
st.title("Route Map")
folium_static(map_)