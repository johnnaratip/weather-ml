#=============================================
# Phase 1
#=============================================
import numpy as np
import pandas as pd
#1. กำหนดตัวเลขสุ่มเเบบคงที่เพื่อให้หน้าตาข้อมูลเหมือนกันทุกครั้ง
np.random.seed(42)
n_row = 100
dates = pd.date_range(start="2026-01-01",periods =n_row,freq="D")

#สุ่มข้อมูลสภาพอากาศจำลอง
temperature=np.random.normal(30,3,size=n_row) #อุณหภูมิเฉลี่ยประมาณ 30 ํ C
humidity = np.random.randint(40,95,size=n_row) # ความชื้นสัมพัทธ์ (40-95%)
wind_speed = np.random.randint(5,30,size=n_row)#ความเร็วลม (กม./ซม.)
rainfall = ((humidity*0.15 )+ np.random.normal(0,3,size=n_row)) #ปริมาณน้ำผน(มม.)
#2. รวมร่างเป็นตารางขอ้มูล(Data frame)
df_row = pd.DataFrame(
    {"Date" : dates,
     "Temperature" : temperature,
     "Humidity" : humidity,
     "Wind_speed" : wind_speed,
     "Rainfall" : rainfall}
    
)
#3. จงใจสร้าง "สกปรก" (ใส่ค่าว่าง NaN เเละข้อมูลเพี้ยน Outlier)
#สุ่มใส่ค่า NaN ในคอลัมน์ Humidity เเละ Rainfall อย่างละ 5 จุด 
df_row.loc[np.random.choice(n_row,5,replace=False),"humidity"] = np.nan
df_row.loc[np.random.choice(n_row,5,replace=False),"Rainfall"] = np.nan

#ใส่ข้อมูลผผิดปกติ (Outlier) เช่น ปริมาณฝนติดลบ หรือฝนพุ่งสูงเกินจริง
df_row.loc[15,"Rainfall"]= 999.0 #ฝนตกพันมิลลิเมตร เป็นไปไม่ได้!
df_row.loc[15,"Rainfall"]= -25.0 #ฝนตกติดลบ

#4. บันทึกเป็ฯไฟล์ CSV ดิบ
df_row.to_csv("raw_weather_data.csv")
print("สร้างเเละบันทึกไฟล์ raw_weather_data.csv สำเร็จเเล้ว!")
print("---ตัวอย่างข้อมูลดิบ 10 เเถวเเรก สังเกตความเละเเละค่า NaN ---")
print(df_row.head(10))
#=============================================
#phase 2 การทำความสะอาดข้อมูล (Dta Cleaning)
#=============================================
import pandas as pd
# 1. โหลดไฟล์ข้อมูลดิบที่เราเพิ่งเซฟไฟล์เข้ามา
df = pd.read_csv("raw_weather_data.csv")
print ("\n===เช็กจำนวนค่าว่าง  (์NaN) ในเเต่ละคอลัมน์ก่อนคลีน====")
print(df.isnull().sum())
#2. จัดการค่าว่าง (Missing Value) โดยที่เเทนด้วย "ค่าเฉลี่ย (mean)" ของคอมลัมน์นั้นๆ
df["Humidity"] = df["Humidity"].fillna(df["Humidity"].mean())
df["Rainfall"] = df["Rainfall"].fillna(df["Rainfall"].mean())
#3. กำจัดข้อมูลผิดปกติ (Outlier Remove)
#กรองเอาเฉพาะข้อมูลปริมาณน้ำฝนที่สมเหตุสมผล เช่น ไม่ติดลบ เเละไม่สูงเวอร์เกินไป (ตั้งไว้ระหวา่าง 0 ถึง 50 มม.)
df_clean = df[(df["Rainfall"] >= 0) & (df["Rainfall"]<=50)]

#4. ปัดเศษทศนิยมให้เหลือ 2 ตำเเหน่ง เพื่อความสวยงาม
df_clean["Temperature"] = df_clean["Temperature"].round(2)
df_clean["Humidity"] = df_clean["Humidity"].round(2)
df_clean["Wind_speed"] = df_clean["Wind_speed"].round(2)
df_clean["Rainfall"] = df_clean["Rainfall"].round(2)
#5. บันทึกข้อมูลที่สะอาดเเล้วเก็บไว้เป็นไฟล์ใหม่
df_clean.to_csv("raw_weather_data.csv", index=False)
print("\n===ทำความสะอาดข้อมูลเรียบร้อยเเล้ว!")
print(f"จำนวนข้อมูลเหลือหลังจากเคลียร์ขยะ : {len(df_clean)} เเถว (จากเดิม 100 แถว)")
print(df_clean.head(10))

#=====================================================
# Phase 3 & 4 : วิเคราะห์ความสัมพันธ์ เเละสร้างโมเดลทำนาย (predition & Visualization)
#=====================================================
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

#1. โหลดไฟล์ข้อมู ที่คลีนเสร็จเเล้ว
df_clean =pd.read_csv("raw_weather_data.csv")
#2. หาค่าความสัมพันธ์ (Correlation) ระหว่างความชื้น กับ ปริมาณน้ำฝน
correlation = df_clean["Humidity"].corr(df_clean["Rainfall"])
print(f"\n === วิเคราะห์สถิติเเละความสัมพันธ์(Correlatin)===")
print(f"ค่า Correlation ระหว่างความชื้นกับปริมาณน้ำฝน : {correlation}")

#3.สร้างโมเดล Linear Regression (หาเส้นตรงเเนวโน้ม)
slope,intercept,r_value,p_value,std_err = stats.linregress(
    df_clean["Humidity"],df_clean["Rainfall"]
)
print(f"สมการทำนายปริมาณฝน : Rainfall =({slope:.2f}*Humidity) + {intercept:.2f} ")

#4.ลองทดสอบทำนายปริมาณน้ำฝน เช่น ถ้าวันนี้มีความชื้นเท่ากับ 80% ฝนจะตกกี่มิลลิตรเมตร?
new_humidity = 80
predited_rainfall = (slope * new_humidity) + intercept
print(f"ทำนายปริมาณน้ำฝน เมื่อความชื้นเท่ากับ {new_humidity}%: {predited_rainfall:.2f} มิลลิตรเมตร")

#5. วาดกราฟเเสดงผล (Data Visualization)
plt.figure (figsize=(8,6))

#พล็อตจุดข้อมูลจริงที่เป็นระเบียบเเล้ว (Scatter Plot)
plt.scatter(df_clean["Humidity"],df_clean["Rainfall"],color="blue",alpha=0.7,label=" Cleaned Actual Data")
#วาดเส้รพยากรณ์เเนวโน้ม (Regression) ทับลงไป
plt.plot(df_clean["Humidity"],(slope * df_clean["Humidity"])+ intercept,
color="red",linestyle="--",linewidth=2,label="Regression Line")
#ตกเเต่งชื่อกราฟเเละป้ายกำกับแกน
plt.title(
    "Weather Project : Humidity VS Rainfall Prediction",
    fontsize=14,
    fontweight="bold"
)
plt.xlabel("Humidity (%)", fontsize=12)
plt.ylabel("Rainfall (mm)" , fontsize=12)
plt.legend()
plt.grid(True, linestyle=":",alpha=0.6)
#เเสดงหน้าต่างกราฟ
plt.show()
